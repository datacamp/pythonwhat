import ast
from pythonwhat.Test import Test, DefinedCollTest, EqualTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

NOT_IMPORTED_MSG = "__JINJA__:Did you import `{{pkg}}`?"
INCORRECT_AS_MSG = "__JINJA__:Did you import `{{pkg}}` as `{{alias}}`?"

def has_import(name,
                 same_as=True,
                 not_imported_msg=NOT_IMPORTED_MSG,
                 incorrect_as_msg=INCORRECT_AS_MSG,
                 state=None):
    """Check whether code has certain import statement.

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

            Ex().has_import("numpy")  # pass
            Ex().has_import("pandas") # fail
            Ex().has_import("pandas", same_as = False) # pass

    """
    rep = Reporter.active_reporter

    student_imports = state.student_imports
    solution_imports = state.solution_imports

    if name not in solution_imports:
        raise NameError("The package you specified is not in the solution imports itself. %r not in solution imports" % name)

    fmt_kwargs = { 'pkg': name, 'alias': solution_imports[name] }

    _msg = state.build_message(not_imported_msg, fmt_kwargs)
    rep.do_test(DefinedCollTest(name, student_imports, _msg))

    if (same_as):
        _msg = state.build_message(incorrect_as_msg, fmt_kwargs)
        rep.do_test(EqualTest(solution_imports[name], student_imports[name], _msg))

    return state

test_import = has_import