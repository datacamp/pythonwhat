from pythonwhat.Test import StringContainsTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter


def check_code(text,
               pattern=True,
               not_typed_msg=None,
               state=None):
    """Test the student code.

    Tests if the student typed a (pattern of) text.

    Args:
        text (str): the text that is searched for
        pattern (bool): if True (the default), the text is treated as a pattern. If False, it is treated as plain text.
        not_typed_msg (str): feedback message to be displayed if the student did not type the text.
    """
    rep = Reporter.active_reporter

    if not not_typed_msg:
        if pattern:
            not_typed_msg = "Could not find the correct pattern in your code."
        else:
            not_typed_msg = "Could not find the following text in your code: %r" % text

    student_code = state.student_code

    _msg = state.build_message(not_typed_msg)
    rep.do_test(StringContainsTest(student_code, text, pattern, _msg))

test_student_typed = check_code
