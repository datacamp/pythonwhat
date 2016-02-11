from pythonwhat.Test import StringContainsTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

def test_student_typed(text,
					   pattern = True,
					   not_typed_msg = None):
	state = State.active_state
	rep = Reporter.active_reporter

	if not not_typed_msg:
		if pattern:
			not_typed_msg = "Could not find the correct pattern in your code."
		else:
			not_typed_msg = "Could not find the following text in your code: %r" % text

	student_code = state.student_code

	rep.do_test(StringContainsTest(student_code, text, pattern, not_typed_msg))
