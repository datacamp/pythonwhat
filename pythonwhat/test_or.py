from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.sub_test import sub_test
from pythonwhat.Test import TestFail

def test_or(*tests, state=None):
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_or")



    success = False
    first_message = None


    success = False
    first_message = None
    for test in tests: 
        try: 
            sub_test(state, rep, test, None, None)
            success = True
        except TestFail as e:
            if not first_message: first_message = rep.feedback.message 
            rep.failed_test = False

        if success: 
            return
    
    rep.failed_test = True
    rep.feedback.message = first_message
    raise TestFail
