from pythonwhat.Test import StringContainsTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter


def has_output(text,
               pattern=True,
               no_output_msg=None,
               state=None):
    """Search student output.

    Checks if the output contains a (pattern of) text.

    Args:
        text (str): the text that is searched for
        pattern (bool): if True (default), the text is treated as a pattern. If False, it is treated as plain text.
        no_output_msg (str): feedback message to be displayed if the output is not found.

    :Example:

        SCT::

            Ex().has_output(r'[H|h]i,*\\s+there!')

        Submissions::

            print("Hi, there!")     # pass
            print("hi  there!")     # pass
            print("Hello there")    # fail
    """
    rep = Reporter.active_reporter

    if not no_output_msg:
        no_output_msg = "You did not output the correct things."

    student_output = state.raw_student_output

    _msg = state.build_message(no_output_msg)
    rep.do_test(
        StringContainsTest(
            student_output,
            text,
            pattern,
            _msg))

    return state

test_output_contains = has_output