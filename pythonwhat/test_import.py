import ast
from pythonwhat.Test import Test, DefinedTest, EqualTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.feedback import FeedbackMessage

def test_import(name, 
				same_as = True,
				not_imported_msg = None,
				incorrect_as_msg = None):
	state = State.active_state
	rep = Reporter.active_reporter

	state.extract_imports()

	student_imports = state.student_imports
	solution_imports = state.solution_imports

	if name not in solution_imports:
		raise NameError("%r not in solution imports " % name)

	not_imported_msg = (FeedbackMessage(not_imported_msg) if not_imported_msg else FeedbackMessage("Did you import `${name}` in your code?"))

	not_imported_msg.set_information("name", name)

	rep.do_test(DefinedTest(name, student_imports, not_imported_msg))

	if rep.failed_test:
		return

	if (same_as):
		incorrect_as_msg = (FeedbackMessage(incorrect_as_msg) if incorrect_as_msg else FeedbackMessage("Did you set the correct alias for `${name}`?"))
		
		incorrect_as_msg.set_information("name", name)

		rep.do_test(EqualTest(solution_imports[name], student_imports[name], incorrect_as_msg))
