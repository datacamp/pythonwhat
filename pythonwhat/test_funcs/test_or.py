from pythonwhat.Reporter import Reporter
from pythonwhat.Test import TestFail, Test
from pythonwhat.check_funcs import multi

def test_or(*tests, state=None):
    """Test whether at least one SCT passes."""

    rep = Reporter.active_reporter

    success = False
    first_feedback = None
    for test in tests: 
        try: 
            multi(test, state=state)
            success = True
        except TestFail as e:
            if not first_feedback: first_feedback = e.feedback
        if success: 
            return
    
    rep.do_test(Test(first_feedback))
