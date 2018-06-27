import io
from pythonwhat.check_syntax import Ex
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from contextlib import redirect_stdout

class StubShell(object):
    
    def __init__(self, init_code = None):
        self.user_ns = {}
        if init_code:
            self.run_code(init_code)
            
    def run_code(self, code):
        exec(code, None, self.user_ns)

class StubProcess(object):

    def __init__(self, init_code = None):
        self.shell = StubShell(init_code)

    def executeTask(self, task):
        return task(self.shell)

def setup_state(stu_code = "", sol_code = "", pec = ""):

    stu_output = io.StringIO()
    with redirect_stdout(stu_output):
        stu_process = StubProcess(init_code =  "%s\n%s" % (pec, stu_code))

    sol_output = io.StringIO()
    with redirect_stdout(sol_output):
        sol_process = StubProcess(init_code =  "%s\n%s" % (pec, sol_code))

    rep = Reporter()
    Reporter.active_reporter = rep

    state = State(
        student_code = stu_code,
        solution_code = sol_code,
        pre_exercise_code = pec,
        student_process = stu_process,
        solution_process = sol_process,
        raw_student_output = stu_output.getvalue())

    State.root_state = state
    return(Ex(state))
