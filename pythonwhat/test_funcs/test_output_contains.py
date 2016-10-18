from pythonwhat.Test import StringContainsTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter


def test_output_contains(text,
                         pattern=True,
                         no_output_msg=None,
                         state=None):
    """Test the output.

    Tests if the output contains a (pattern of) text.

    Args:
        text (str): the text that is searched for
        pattern (bool): if True, the text is treated as a pattern. If False, it is treated as plain text.
          Defaults to False.
        no_output_msg (str): feedback message to be displayed if the output is not found.
    """
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_output_contains")

    if not no_output_msg:
        no_output_msg = "You did not output the correct things."

    student_output = state.raw_student_output

    rep.do_test(
        StringContainsTest(
            student_output,
            text,
            pattern,
            no_output_msg))
