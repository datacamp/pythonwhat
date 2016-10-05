from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

from pythonwhat.test_or import test_or

def test_correct(check, diagnose):
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_correct")

    def diagnose_and_check():
        diagnose()
        check()

    test_or(diagnose_and_check, check)
