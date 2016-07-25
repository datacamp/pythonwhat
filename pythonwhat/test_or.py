from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

def test_or(*tests):
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_or")

    if rep.failed_test:
        return

    success = False
    first_message = None

    for test in tests:
        test()
        if not rep.failed_test:
            success = True
            break
        else:
            first_message = first_message or rep.feedback.message
            rep.failed_test = False

    if not success:
        rep.fail(first_message)

