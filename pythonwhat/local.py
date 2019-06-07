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
    except Exception as e:
        raw_output = ""
        error = str(e)
    return raw_output, error


def run_single_process(pec, code, pid=None):
    process = StubProcess(init_code=pec, pid=pid)
    raw_stu_output, error = run_code(process, code)
    return process, raw_stu_output, error


def run_exercise(pec, sol_code, stu_code, pid=None, sol_wd=None, stu_wd=None):
    with ChDir(stu_wd or os.getcwd()):
        stu_process, raw_stu_output, error = run_single_process(pec, stu_code, pid=pid)

    with ChDir(sol_wd or os.getcwd()):
        sol_process, _, _ = run_single_process(pec, sol_code, pid=pid)

    return sol_process, stu_process, raw_stu_output, error


# TODO:
#  - test has_equal_value: has_equal_value (also with name and/or expr_code)
#    - check_object currently only works on root, this introduces a new 'root' for that purpose
#  - converge with pythonbackend, look at scalabackend
#    - support running with arbitrary wd + path + flags (now only wd)
#      e.g. `python -m project.run
#      allow setting env vars? e.g. PYTHONPATH, could help running more complex setup
def run(state, relative_workin_directory=""):
    sol_wd = Path(os.getcwd(), "solution", relative_workin_directory)
    os.makedirs(str(sol_wd), exist_ok=True)
    stu_wd = Path(os.getcwd(), relative_workin_directory)
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
