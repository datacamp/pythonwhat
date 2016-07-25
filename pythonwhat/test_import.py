import ast
from pythonwhat.Test import Test, DefinedTest, EqualTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

def test_import(name,
                same_as=True,
                not_imported_msg=None,
                incorrect_as_msg=None):
    """Test import.

    Test whether an import statement is used the same in the student's environment as in the solution
    environment.

    Args:
        name (str): the name of the package that has to be checked.
        same_as (bool): if false, the alias of the package doesn't have to be the same. Defaults to True.
        not_imported_msg (str): feedback message when the package is not imported.
        incorrect_as_msg (str): feedback message if the alias is wrong.


    Examples:
        Student code

        | ``import numpy as np``
        | ``import pandas as pa``

        Solution code

        | ``import numpy as np``
        | ``import pandas as pd``

        SCT

        | ``test_import("numpy")``: pass.
        | ``test_import("pandas")``: fail.
        | ``test_import("pandas", same_as = False)``: pass.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_import")

    state.extract_imports()

    student_imports = state.student_imports
    solution_imports = state.solution_imports

    if name not in solution_imports:
        raise NameError("%r not in solution imports " % name)

    if not_imported_msg is None:
        not_imported_msg = "Did you import `%s` in your code?" % name

    rep.do_test(DefinedTest(name, student_imports, not_imported_msg))

    if rep.failed_test:
        return

    if (same_as):
        if incorrect_as_msg is None:
            incorrect_as_msg = "Did you set the correct alias for `%s`" % name

        rep.do_test(
            EqualTest(
                solution_imports[name],
                student_imports[name],
                incorrect_as_msg))
