import io
import os
import random
from pathlib import Path

from pythonwhat.reporter import Reporter
from contextlib import redirect_stdout


class StubShell(object):
    def __init__(self, init_code=None):
        self.user_ns = {}
        if init_code:
            self.run_code(init_code)

    def run_code(self, code):
        exec(code, self.user_ns)


class StubProcess(object):
    def __init__(self, init_code=None, pid=None):
        self.shell = StubShell(init_code)
        self._identity = (pid,) if pid else (random.randint(0, 1e12),)

    def executeTask(self, task):
        return task(self.shell)


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


def run_code(process, code):
    output = io.StringIO()
    try:
        with redirect_stdout(output):
            process.shell.run_code(code)
        raw_output = output.getvalue()
        error = None
    except BaseException as e:
        raw_output = ""
        error = str(e)
    return raw_output, error


def run_single_process(pec, code, pid=None):
    process = StubProcess(init_code=pec, pid=pid)
    raw_stu_output, error = run_code(process, code)
    return process, raw_stu_output, error


def run_exercise(pec, sol_code, stu_code, pid=None, sol_wd=None, stu_wd=None):
    with ChDir(sol_wd or os.getcwd()):
        sol_process, _, _ = run_single_process(pec, sol_code, pid=pid)

    with ChDir(stu_wd or os.getcwd()):
        stu_process, raw_stu_output, error = run_single_process(pec, stu_code, pid=pid)

    return sol_process, stu_process, raw_stu_output, error


# todo:
#  converge with xbackend (pythonbackend + look at scalabackend)
#  move towards xwhat controlling all execution and xbackend providing the execution interface?
# running with arbitrary wd + path + flags (now only wd) needed?
#  e.g. `python -m project.run
#  allow setting env vars? e.g. PYTHONPATH, could help running more complex setup
#  allow prepending code? set_env? e.g. (automatically) setting __file__?
def run(state, relative_working_dir="", solution_dir="solution"):
    """Run the focused student and solution code in the specified location

    This function can be used after ``check_file`` to execute student and solution code.
    The arguments allow setting the correct context for execution.
    The ``solution_dir`` allows setting a different root of the solution context so solution side effects don't conflict with those of the student.

    This function does not execute the file itself,
    but this should only matter when using functionality depending on e.g. ``__file__`` and ``inspect``.

    Args:
        relative_working_dir (str): if specified, this relative path is the subdirectory
            inside the student and solution context in which the code is executed
        solution_dir (str): a relative path, ``solution`` by default,
            that sets the root of the solution context, relative to that of the student execution context
        state (State): state as passed by the SCT chain. Don't specify this explicitly.

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
    # todo: configure these arguments automatically based on check_file info?
    # once that is implemented, look into executing the file itself
    # and keeping the process alive to extract values
    sol_wd = Path(os.getcwd(), solution_dir, relative_working_dir)
    os.makedirs(str(sol_wd), exist_ok=True)
    stu_wd = Path(os.getcwd(), relative_working_dir)
    sol_process, stu_process, raw_stu_output, error = run_exercise(
        pec="",
        sol_code=state.solution_code or "",
        stu_code=state.student_code,
        pid=None,
        sol_wd=sol_wd,
        stu_wd=stu_wd,
    )
    return state.to_child(
        student_process=stu_process,
        solution_process=sol_process,
        raw_student_output=raw_stu_output,
        reporter=Reporter(state.reporter, errors=[error] if error else []),
    )
