from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.sub_test import sub_test

from .test_or import test_or

def test_correct(check, diagnose, state=None):
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_correct")

    def diagnose_and_check():
        sub_test(state, rep, diagnose, None, None)
        sub_test(state, rep, check, None, None)

    test_or(diagnose_and_check, check, state=state)
