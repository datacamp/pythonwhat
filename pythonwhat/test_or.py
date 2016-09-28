from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.sub_test import sub_test

def test_or(*tests, state=None):
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_or")

    if rep.failed_test:
        return

    success = False
    first_message = None

    for test in tests:
        sub_test(state, rep, test, None, None)
        if not rep.failed_test:
            success = True
            break
        else:
            first_message = first_message or rep.feedback.message
            rep.failed_test = False

    if not success:
        rep.fail(first_message)

