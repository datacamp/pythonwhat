import io
import random

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





def run_exercise(pec, sol_code, stu_code, pid=None):
    stu_process = StubProcess(init_code=pec, pid=pid)
    raw_stu_output, error = run_code(stu_process, stu_code)

    sol_process = StubProcess(init_code=pec, pid=pid)
    run_code(sol_process, sol_code)

    return sol_process, stu_process, raw_stu_output, error


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
