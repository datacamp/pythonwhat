import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, EquivalentTest

from pythonwhat import utils

import copy

def test_expression_result(extra_env = None,
							 context_vals = None,
						   incorrect_msg = None,
						   eq_condition = "equal",
						   expr_code = None,
						   pre_code = None,
						   keep_objs_in_env = None):
	state = State.active_state
	rep = Reporter.active_reporter

	eq_map = {"equal": EqualTest, "equivalent": EquivalentTest}

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
		if expr_code is None:
			eval_student = eval(compile(ast.Expression(student_expr), "<student>", "eval"), student_env)
		else:
			eval_student = eval(expr_code, student_env)
	except:
		eval_student = None

	if pre_code is not None:
		exec(pre_code, student_env)
	if expr_code is None:
		eval_solution = eval(compile(ast.Expression(solution_expr), "<solution>", "eval"), solution_env)
	else:
		eval_solution = eval(expr_code, solution_env)

	if incorrect_msg is not None:
		feedback_msg = incorrect_msg
	else:
		feedback_msg = "Unexpected expression: expected `%s`, got `%s` with values" + ((" "+str(extra_env)) if extra_env else ".")
		feedback_msg = feedback_msg % (utils.shorten_str(str(eval_solution)), utils.shorten_str(str(eval_student)))

	Reporter.active_reporter.do_test(eq_map[eq_condition](eval_solution, eval_student, feedback_msg))