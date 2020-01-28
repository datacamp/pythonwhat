import io
import os
import random
from pathlib import Path
from contextlib import redirect_stdout

from multiprocessing import Process, Queue
from protowhat.Reporter import Reporter

try:
    from pythonbackend.shell_utils import create
    from pythonbackend.tasks import TaskCaptureFullOutput

    BACKEND_AVAILABLE = True
except:
    BACKEND_AVAILABLE = False


class StubShell:
    def __init__(self, init_code=None):
        self.user_ns = {}
        if init_code:
            self.run_code(init_code)

    def run_code(self, code):
        exec(code, self.user_ns)


class StubProcess:
    def __init__(self, init_code=None, pid=None):
        self.shell = StubShell(init_code)
        self._identity = (pid,) if pid else (random.randint(0, 1e12),)

    def executeTask(self, task):
        return task(self.shell)


class TaskCaptureOutput:
    def __init__(self, code):
        self.code = code

    def __call__(self, shell):
        return run_code(shell.run_code, self.code)


class TaskKillProcess:
    def __call__(self, shell):
        return None


class CaptureErrors:
    def __init__(self, output):
        self.output = output

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exception, traceback):
        if exc_type is not None:
            self.output.append({"type": "backend-error", "payload": str(exception)})
            return True


class WorkerProcess(Process):
    instances = []

    def __init__(self, pid=None):
        Process.__init__(self)
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.daemon = (
            True
        )  # when parent process is killed, sub/childprocess get also killed
        self.instances.append(self)
        # used to detect single process exercise
        self._identity = (pid,) if pid else (random.randint(0, 1e12),)

    def get_shell(self):
        return create({})

    def run(self):
        shell = self.get_shell()
        while True:
            output = []
            with CaptureErrors(output):
                next_task = self.task_queue.get()
                answer = next_task(shell)
            if len(output) > 0:  # means backend error happened
                answer = output
            output = []
            with CaptureErrors(output):
                self.result_queue.put_nowait(answer)
            if len(output) > 0:  # means backend error happened
                self.result_queue.put_nowait(output)
            if isinstance(next_task, TaskKillProcess):
                break  # break while loop -> we do not wait upon new task
        return

    def executeTask(self, task):
        self.task_queue.put_nowait(task)
        return self.result_queue.get()  # wait and fetches next item in queue

    def kill(self):
        try:
            if self.is_alive():
                self.executeTask(TaskKillProcess())
                self.join(timeout=3.0)
                if self.is_alive():
                    self.terminate()
                    self.join(timeout=3.0)
            if self in self.instances:
                self.instances.remove(self)
        finally:
            pass
            # python 3.7:
            # self.close()

    @classmethod
    def kill_all(cls):
        for instance in list(cls.instances):
            instance.kill()


class SimpleProcess(WorkerProcess):
    def get_shell(self):
        return StubShell()


class ChDir(object):
    """
    Step into a directory temporarily.
    """

    def __init__(self, path):
        self.old_dir = os.getcwd()
        self.new_dir = str(path)

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        os.chdir(self.old_dir)


def run_code(executor, code):
    with io.StringIO() as output:
        try:
            with redirect_stdout(output):
                executor(code)
            raw_output = output.getvalue()
            error = None
        except BaseException as e:
            raw_output = ""
            error = str(e)
    return raw_output, error


def run_single_process(pec, code, pid=None, mode="simple"):
    if mode == "stub":
        # no isolation
        process = StubProcess(init_code=pec, pid=pid)
        raw_output, error = run_code(process.shell.run_code, code)

    elif mode == "simple":
        # no advanced functionality
        process = SimpleProcess(pid)
        process.start()
        _ = process.executeTask(TaskCaptureOutput(pec))
        raw_output, error = process.executeTask(TaskCaptureOutput(code))

    elif mode == "full" and BACKEND_AVAILABLE:
        # slow
        process = WorkerProcess(pid)
        process.start()
        _ = process.executeTask(
            TaskCaptureFullOutput((pec,), "<PEC>", None, silent=True)
        )
        output, raw_output = process.executeTask(
            TaskCaptureFullOutput((code,), "script.py", None, silent=True)
        )
        raw_output = raw_output["output_stream"]
        error = raw_output["error"]

    else:
        raise ValueError("Invalid mode")

    return process, raw_output, error


def run_exercise(pec, sol_code, stu_code, sol_wd=None, stu_wd=None, **kwargs):
    with ChDir(sol_wd or os.getcwd()):
        sol_process, _, _ = run_single_process(pec, sol_code, **kwargs)

    with ChDir(stu_wd or os.getcwd()):
        stu_process, raw_stu_output, error = run_single_process(pec, stu_code, **kwargs)

    return sol_process, stu_process, raw_stu_output, error


# todo:
#  imports from local modules (solution needs to be materialised somewhere)
#  converge with xbackend (pythonbackend + look at scalabackend)
#  move towards xwhat controlling all execution and xbackend providing the execution interface?
# running with arbitrary wd + path + flags (now only wd) needed?
#  e.g. `python -m project.run
#  allow setting env vars? e.g. PYTHONPATH, could help running more complex setup
#  allow prepending code? set_env? e.g. (automatically) setting __file__?
def run(state, relative_working_dir=None, solution_dir="../solution", run_solution=True):
    """Run the focused student and solution code in the specified location

    This function can be used after ``check_file`` to execute student and solution code.
    The arguments allow configuring the correct context for execution.

    SCT functions chained after this one that execute pieces of code (custom expressions or the focused part of a file)
    execute in the same student and solution locations as the file.

    .. note::

        This function does not execute the file itself, but code in memory.
        This can have an impact when:

        - the solution code imports from a different file in the expected solution (code that is not installed)
        - using functionality depending on e.g. ``__file__`` and ``inspect``

        When the expected code has imports from a different file that is part of the exercise,
        it can only work if the solution code provided earlier does not have these imports but instead
        has all that functionality inlined.

    Args:
        relative_working_dir (str): if specified, this relative path is the subdirectory
            inside the student and solution context in which the code is executed
        solution_dir (str): a relative path, ``solution`` by default,
            that sets the root of the solution context, relative to that of the student execution context
        state (State): state as passed by the SCT chain. Don't specify this explicitly.

    If ``relative_working_dir`` is not set, it will be the directory the file was loaded from by ``check_file``
    and fall back to the root of the student execution context (the working directory pythonwhat runs in).

    The ``solution_dir`` helps to prevent solution side effects from conflicting with those of the student.
    If the set or derived value of ``relative_working_dir`` is an absolute path,
    ``relative_working_dir`` will not be used to form the solution execution working directory:
    the solution code will be executed in the root of the solution execution context.

    :Example:

        Suppose the student and solution have a file ``script.py`` in ``/home/repl/``::

            if True:
                a = 1

            print("Hi!")

        We can check it with this SCT (with ``file_content`` containing the expected file content)::

            Ex().check_file(
                "script.py",
                solution_code=file_content
            ).run().multi(
                check_object("a").has_equal_value(),
                has_printout(0)
            )
    """
    # todo:
    # look into executing the file itself
    # and keeping the process alive to extract values
    if relative_working_dir is None:
        if getattr(state, "path", False):
            relative_working_dir = state.path.parent
        else:
            relative_working_dir = ""

    if not os.path.isabs(str(relative_working_dir)):
        sol_wd = Path(os.getcwd(), solution_dir, relative_working_dir)
    else:
        sol_wd = Path(os.getcwd(), solution_dir)

    os.makedirs(str(sol_wd), exist_ok=True)
    stu_wd = Path(os.getcwd(), relative_working_dir)
    sol_code = state.solution_code or "" if run_solution else ""

    sol_process, stu_process, raw_stu_output, error = run_exercise(
        pec="",
        sol_code=sol_code,
        stu_code=state.student_code,
        sol_wd=sol_wd,
        stu_wd=stu_wd,
    )
    return state.to_child(
        student_process=stu_process,
        solution_process=sol_process,
        raw_student_output=raw_stu_output,
        reporter=Reporter(state.reporter, errors=[error] if error else []),
    )
