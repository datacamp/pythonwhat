import ast

from pythonwhat.Test import Test, DefinedTest, EqualTest, EquivalentTest, BiggerTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.feedback import FeedbackMessage

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])


def test_function(name, 
				  index = 1, 
				  args = None, 
				  keywords = None,
				  eq_condition = "equal", 
				  do_eval = True, 
				  not_called_msg = None, 
				  incorrect_msg = None):
	state = State.active_state
	rep = Reporter.active_reporter

	index = index - 1
	eq_map = {"equal": EqualTest, "equivalent": EquivalentTest}
	student_env, solution_env = state.student_env, state.solution_env

	if eq_condition not in eq_map:
		raise NameError("%r not a valid equality condition " % eq_condition)

	state.extract_function_calls()
	solution_calls = state.solution_function_calls
	student_calls = state.student_function_calls

	if not name in state.used_student_function:
		state.used_student_function[name] = 0

	nb_call = state.used_student_function[name] + 1


	if not(not_called_msg):
		if nb_call > 1:
			not_called_msg = FeedbackMessage("Don't forget the "+ordinal(nb_call)+" call of `${name}()`.")
		else:
			not_called_msg = FeedbackMessage("Make sure you call `${name}()`.")

		not_called_msg.add_information("name", name)
	else: 
		not_called_msg = FeedbackMessage(not_called_msg)

	if name not in solution_calls:
		raise NameError("%r not in solution environment " % name)

	rep.do_test(DefinedTest(name, student_calls, not_called_msg))
	if rep.failed_test:
		return

	rep.do_test(BiggerTest(len(student_calls[name]), 0, not_called_msg))
	if rep.failed_test:
		return

	lineno_solution, args_solution, keyw_solution = solution_calls[name][index]
	keyw_solution = {keyword.arg: keyword.value for keyword in keyw_solution}

	if args is None:
		args = range(0,len(args_solution))
	else:
		args = [i - 1 for i in args]

	if keywords is None:
		keywords = keyw_solution

	def eval_arg(arg_student, arg_solution, feedback):
		if do_eval:
			try:
				eval_student = eval(compile(ast.Expression(arg_student), "<student>", "eval"), student_env)
			except:
				eval_student = None

			eval_solution = eval(compile(ast.Expression(arg_solution), "<solution>", "eval"), solution_env)
		else:
			eval_student = arg_student
			eval_solution = arg_solution

		feedback.set_information("result", eval_student)
		feedback.set_information("expected", eval_solution)

		return(eq_map[eq_condition](eval_student, eval_solution, feedback))

	success = None
	incorrect_msg = (FeedbackMessage(incorrect_msg) if incorrect_msg else None)

	for call in range(len(student_calls[name])):
		lineno_student, args_student, keyw_student = student_calls[name][call]
		keyw_student = {keyword.arg: keyword.value for keyword in keyw_student}

		if len(args) > len(args_student):
			continue

		if len(set(keywords)) > 0 and not set(keywords.keys()).issubset(set(keyw_student.keys())):
			continue
		

		feedback = construct_incorrect_msg(nb_call)
		feedback.set_information("name", name)
		feedback.set_information("line", lineno_student)

		success = True
		for arg in args:
			arg_student = args_student[arg]
			arg_solution = args_solution[arg]

			feedback.set_information("argument", arg + 1)

			test = eval_arg(arg_student, arg_solution, feedback)

			test.test()

			if not test.result:
				success = False
				break


		if success:
			feedback.remove_information("argument")
			for key in keywords:
				key_student = keyw_student[key]
				key_solution = keyw_solution[key]

				feedback.set_information("keyword", key)

				test = eval_arg(key_student, key_solution, feedback)

				test.test()

				if not test.result:
					success = False
					break

		if success:
			state.used_student_function[name] += 1
			del state.student_function_calls[name][call]
			break
		elif incorrect_msg is None:
			incorrect_msg = feedback


	if not success:
		if not incorrect_msg:
			incorrect_msg = construct_incorrect_msg(nb_call)
			incorrect_msg.set_information("name", name)

		rep.do_test(Test(incorrect_msg))

def construct_incorrect_msg(nb_call):
	if nb_call > 1:
		feedback = FeedbackMessage("Did you call `${name}()` with the correct arguments the "+ordinal(nb_call)+" time?")
	else:
		feedback = FeedbackMessage("Did you call `${name}()` with the correct arguments?")

	feedback.cond_append("line", "Call on line ${line} has wrong arguments.")
	feedback.cond_append("argument", "Argument ${argument} seems to be incorrect.")
	feedback.cond_append("keyword", "Keyword `${keyword}` seems to be incorrect.")
	feedback.cond_append("expected", "Expected `${expected}`, got `${result}`.")
	return(feedback)