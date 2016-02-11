from pythonwhat.Test import DefinedTest, EqualEnvironmentTest, EquivalentEnvironmentTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

def test_object(name, 
				eq_condition = "equal", 
				do_eval = True, 
				undefined_msg = None, 
				incorrect_msg = None):
	state = State.active_state
	rep = Reporter.active_reporter

	undefined_msg, incorrect_msg = build_strings(undefined_msg, incorrect_msg, name)
	tests = []
	eq_map = {"equal": EqualEnvironmentTest, "equivalent": EquivalentEnvironmentTest}
	student_env = state.student_env
	solution_env = state.solution_env

	if eq_condition not in eq_map:
		raise NameError("%r not a valid equality condition " % eq_condition)

	if name not in solution_env:
		raise NameError("%r not in solution environment " % name)

	rep.do_test(DefinedTest(name, student_env, undefined_msg))
	if (rep.failed_test):
		return

	if do_eval:
		rep.do_test(eq_map[eq_condition](name, student_env, solution_env, incorrect_msg))

def build_strings(undefined_msg, incorrect_msg, name):
	if not undefined_msg:
		undefined_msg = "Have you defined `"+name+"`?"

	if not incorrect_msg:
		incorrect_msg = "Are you sure you assigned the correct value to `"+ name+"`?"

	return(undefined_msg, incorrect_msg)