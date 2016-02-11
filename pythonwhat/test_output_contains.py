from pythonwhat.Test import StringContainsTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

def test_output_contains(text,
					   	 pattern = True,
					     no_output_msg = None):
	state = State.active_state
	rep = Reporter.active_reporter

	if not no_output_msg:
		no_output_msg = "You did not output the correct things."

	student_output = state.raw_student_output

	rep.do_test(StringContainsTest(student_output, text, pattern, no_output_msg))
