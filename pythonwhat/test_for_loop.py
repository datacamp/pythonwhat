import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test

def test_for_loop(index = 1,
				 for_iter = None,
				 body = None,
				 orelse = None,
				 expand_message = True):
	state = State.active_state
	rep = Reporter.active_reporter

	index = index - 1

	student_env, solution_env = state.student_env, state.solution_env

	state.extract_for_calls()
	student_fors = state.student_for_calls
	solution_fors = state.solution_for_calls

	try:
		lineno_student, target_student, for_iter_student, body_student, orelse_student = student_fors[index]
	except:
		rep.do_test(Test("Define more `for` loops."))
		return

	lineno_solution, target_solution, for_iter_solution, body_solution, orelse_solution = solution_fors[index]

	def sub_test(closure, subtree_student, subtree_solution, incorrect_part):
		if closure:
			failed_before = rep.failed_test
			child = state.to_child_state(subtree_student, subtree_solution)
			child.context_student = target_student
			child.context_solution = target_solution
			closure()
			child.to_parent_state()
			if expand_message and (failed_before is not rep.failed_test):
				rep.feedback_msg = rep.feedback_msg + " in the " + incorrect_part + " of the `for` loop on line " + str(lineno_student) + "."

	sub_test(for_iter, for_iter_student, for_iter_solution, "sequence part")
	sub_test(body, body_student, body_solution, "body")
	sub_test(orelse, orelse_student, orelse_solution, "else part")