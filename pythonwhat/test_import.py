import ast
from pythonwhat.Test import Test, DefinedTest, EqualTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.feedback import FeedbackMessage


def test_import(name,
                same_as=True,
                not_imported_msg=None,
                incorrect_as_msg=None):
    """Test import.

    Test whether an import statement is used the same in the student's environment as in the solution
    environment.

    Example:
      student_code
        | ``import numpy as np``
        | ``import pandas as pa``
      solution_code
        | ``import numpy as np``
        | ``import pandas as pd``
      sct
        | ``test_import("numpy")``: passes
        | ``test_import("pandas")``: fails
        | ``test_import("pandas", same_as = False)``: passes

    Args:
        name (str): the name of the package that has to be checked.
        same_as (bool): if false, the alias of the package doesn't have to be the same. Defaults to True.
        not_imported_msg (str): feedback message when the package is not imported.
        incorrect_as_msg (str): feedback message if the alias is wrong.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_import")

    state.extract_imports()

    student_imports = state.student_imports
    solution_imports = state.solution_imports

    if name not in solution_imports:
        raise NameError("%r not in solution imports " % name)

    not_imported_msg = (FeedbackMessage(not_imported_msg) if not_imported_msg else FeedbackMessage(
        "Did you import `${name}` in your code?"))

    not_imported_msg.set_information("name", name)

    rep.do_test(DefinedTest(name, student_imports, not_imported_msg))

    if rep.failed_test:
        return

    if (same_as):
        incorrect_as_msg = (FeedbackMessage(incorrect_as_msg) if incorrect_as_msg else FeedbackMessage(
            "Did you set the correct alias for `${name}`?"))

        incorrect_as_msg.set_information("name", name)

        rep.do_test(
            EqualTest(
                solution_imports[name],
                student_imports[name],
                incorrect_as_msg))
