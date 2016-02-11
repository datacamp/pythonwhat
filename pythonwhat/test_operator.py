import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, EquivalentTest, CollectionContainsTest, BiggerTest

from pythonwhat import utils

def test_operator(index = 1,
				  eq_condition = "equal",
				  used = None,
				  do_eval = True,
				  not_found_msg = None,
				  incorrect_op_msg = None,
				  incorrect_result_msg = None):
	state = State.active_state
	rep = Reporter.active_reporter
		
	index = index - 1
	eq_map = {"equal": EqualTest, "equivalent": EquivalentTest}
	student_env, solution_env = state.student_env, state.solution_env

	if eq_condition not in eq_map:
		raise NameError("%r not a valid equality condition " % eq_condition)

	state.extract_operators()
	student_ops = state.student_operators
	solution_ops = state.solution_operators

	rep.do_test(BiggerTest(len(student_ops), index, (not_found_msg if not_found_msg else "You didn't define enough operations in your code.")))
	if (rep.failed_test):
		return

	lineno_student, expr_student, used_student = student_ops[index]

	if index > len(solution_ops)+1:
		raise IndexError("index not found in solution: %d" % index)

	lineno_solution, expr_solution, used_solution = solution_ops[index]

	build_incorrect_msg = "Your operation at line " + str(lineno_student)

	used_student = set(used_student)
	used_solution = set(used_solution)
	if used != None:
		used = set(used)
	else:
		used = used_solution

	for op in used:
		Reporter.active_reporter.do_test(CollectionContainsTest(op, used_student, 
			(incorrect_op_msg if incorrect_op_msg else (build_incorrect_msg + " is missing a `%s` operation." % op))))


	if (do_eval):
		try:
			eval_student = str(eval(compile(ast.Expression(expr_student), "<student>", "eval"), student_env))
		except:
			eval_student = None

		eval_solution = str(eval(compile(ast.Expression(expr_solution), "<solution>", "eval"), solution_env))

		rep.do_test(eq_map[eq_condition](eval_student, eval_solution, 
			(incorrect_result_msg if incorrect_result_msg else (build_incorrect_msg + " evaluates to `%s`, should be `%s`." % (utils.shorten_str(str(eval_student)), utils.shorten_str(str(eval_solution)))))))
