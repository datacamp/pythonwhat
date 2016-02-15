
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest

MC_VAR_NAME = "selected_option"

def test_mc(correct, msgs):
	if not issubclass(type(correct), int):
		raise ValueError("correct should be an integer")

	state = State.active_state
	student_env = state.student_env
	rep = Reporter.active_reporter

	if not MC_VAR_NAME in student_env:
		raise NameError("%r not set in the student environment" % MC_VAR_NAME)
	else:
		selected_option = student_env[MC_VAR_NAME]
		if not issubclass(type(selected_option), int):
			raise ValueError("selected_option should be an integer")

		if selected_option < 1 or correct < 1:
			raise ValueError("selected_option and correct should be greater than zero")

		if selected_option > len(msgs) or correct > len(msgs):
			raise ValueError("there are not enough feedback messages defined")

		feedback_msg = msgs[selected_option-1]

		rep.set_success_msg(msgs[correct-1])

		rep.do_test(EqualTest(selected_option, correct, feedback_msg))

