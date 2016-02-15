import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedTest, EqualEnvironmentTest, EquivalentEnvironmentTest

from pythonwhat import utils

import copy

def test_object_after_expression(name,
							 extra_env = None,
							 context_vals = None,
							 undefined_msg = None,
						   incorrect_msg = None,
						   eq_condition = "equal",
						   pre_code = None,
						   keep_objs_in_env = None):
	state = State.active_state
	rep = Reporter.active_reporter

	undefined_msg, incorrect_msg = build_strings(undefined_msg, incorrect_msg, name)

	eq_map = {"equal": EqualEnvironmentTest, "equivalent": EquivalentEnvironmentTest}

	if eq_condition not in eq_map:
		raise NameError("%r not a valid equality condition " % eq_condition)

	student_expr = state.student_tree
	solution_expr = state.solution_tree

	student_env = utils.copy_env(state.student_env, keep_objs_in_env)
	solution_env = utils.copy_env(state.solution_env, keep_objs_in_env)

	if extra_env:
		student_env.update(copy.deepcopy(extra_env))
		solution_env.update(copy.deepcopy(extra_env))

	if context_vals is not None:
		if len(state.context_student) > 1:
			student_env.update({key: value for (key,value) in zip(state.context_student, context_vals)})
		else:
			student_env.update({state.context_student[0]: (context_vals[0] if len(context_vals) == 1 else context_vals)})

		if len(state.context_solution) > 1:
			solution_env.update({key: value for (key,value) in zip(state.context_solution, context_vals)})
		else:
			solution_env.update({state.context_solution[0]: (context_vals[0] if len(context_vals) == 1 else context_vals)})

	try:
		if pre_code is not None:
			exec(pre_code, student_env)
		exec(compile(student_expr, "<student>", "exec"), student_env)
	except:
		pass

	if pre_code is not None:
		exec(pre_code, solution_env)
	exec(compile(solution_expr, "<solution>", "exec"), solution_env)

	rep.do_test(DefinedTest(name, student_env, undefined_msg))
	if (rep.failed_test):
		return

	rep.do_test(eq_map[eq_condition](name, student_env, solution_env, incorrect_msg))

def build_strings(undefined_msg, incorrect_msg, name):
	if not undefined_msg:
		undefined_msg = "Have you defined `"+name+"`?"

	if not incorrect_msg:
		incorrect_msg = "Are you sure you assigned the correct value to `"+ name+"`?"

	return(undefined_msg, incorrect_msg)
