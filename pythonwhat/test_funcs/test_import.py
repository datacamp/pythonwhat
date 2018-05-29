import ast
from pythonwhat.Test import Test, DefinedCollTest, EqualTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

def check_import(name,
                 same_as=True,
                 not_imported_msg=None,
                 incorrect_as_msg=None,
                 state=None):
    """Check import statements.

    Test whether an import statement is used the same in the student's environment as in the solution
    environment.

    Args:
        name (str): the name of the package that has to be checked.
        same_as (bool): if false, the alias of the package doesn't have to be the same. Defaults to True.
        not_imported_msg (str): feedback message when the package is not imported.
        incorrect_as_msg (str): feedback message if the alias is wrong.


    :Example:

        Student code::

            import numpy as np
            import pandas as pa

        Solution code::

            import numpy as np
            import pandas as pd

        SCT::

            Ex().check_imports("numpy")  # pass
            Ex().check_imports("pandas") # fail
            Ex().check_imports("pandas", same_as = False) # pass

    """
    rep = Reporter.active_reporter

    student_imports = state.student_imports
    solution_imports = state.solution_imports

    if name not in solution_imports:
        raise NameError("%r not in solution imports" % name)

    if not_imported_msg is None:
        not_imported_msg = "Did you import `%s`?" % name

    _msg = state.build_message(not_imported_msg)
    rep.do_test(DefinedCollTest(name, student_imports, _msg))

    if (same_as):
        if incorrect_as_msg is None:
            incorrect_as_msg = "Did you set the correct alias for `%s`?" % name

        _msg = state.build_message(incorrect_as_msg)
        rep.do_test(
            EqualTest(
                solution_imports[name],
                student_imports[name],
                _msg))

test_import = check_import