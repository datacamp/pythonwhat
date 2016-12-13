from pythonwhat.Reporter import Reporter
from pythonwhat.Test import TestFail
from pythonwhat.check_funcs import multi

def test_or(*tests, state=None):
    """Test whether at least one SCT passes."""

    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_or")

    success = False
    first_feedback = None
    for test in tests: 
        try: 
            multi(test, state=state)
            success = True
        except TestFail as e:
            if not first_feedback: first_feedback = rep.feedback
            rep.failed_test = False

        if success: 
            return
    
    rep.failed_test = True
    rep.feedback = first_feedback
    raise TestFail
