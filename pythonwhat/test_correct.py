from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

def test_or(check, diagnose):
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_correct")

    if rep.failed_test:
        return

    def diagnose_and_check():
        diagnose()
        check()

    test_or(check, diagnose_and_check)
