from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

def test_or(*tests):
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_or")

    if rep.failed_test:
        return

    success = False
    first_message = None

    rep.start_or_test()

    for test in tests:
        rep.do_test(test)

    rep.end_or_test()
