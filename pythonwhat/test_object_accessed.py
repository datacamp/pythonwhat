from pythonwhat.State import State
from pythonwhat.Reporter import Reporter


def test_object_accessed(name,
                         not_accessed_msg=None):
    """Test if object accessed

    Checks whether an object, or the attribute of an object, are accessed

    Args:
        name (str): the name of the object that should be accessed; can contain dots (for attributes)
        not_accessed_msg (str): custom feedback message when the object was not accessed.

    Examples:


        Student code

        | ``import numpy as np``
        | ``arr = np.array([1, 2, 3])``
        | ``x = arr.shape``

        Solution code

        | ``import numpy as np``
        | ``arr = np.array([1, 2, 3])``
        | ``x = arr.shape``
        | ``t = arr.dtype``

        SCT

        | ``test_object_accessed("arr")``: pass.
        | ``test_object_accessed("arr.shape")``: pass.
        | ``test_object_accessed("arr.dtype")``: fail.
    """

    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_object_accessed")

    not_accessed_msg = build_strings(not_accessed_msg, name)

    state.extract_object_accesses()

    student_env = state.student_env
    solution_env = state.solution_env

    if name not in solution_env:
        raise NameError("%r not in solution environment " % name)

    rep.do_test(DefinedTest(name, student_env, undefined_msg))
    if (rep.failed_test):
        return

    ## CONTINUE HERE





def build_strings(not_called_msg, name):

    if not not_called_msg:
        incorrect_msg = "Still make meaningful message"

    return(undefined_msg, not_called_msg)
