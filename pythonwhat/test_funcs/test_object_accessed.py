from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import BiggerTest
import pythonwhat.utils

def test_object_accessed(name,
                         times=1,
                         not_accessed_msg=None,
                         state=None):
    """Test if object accessed

    Checks whether an object, or the attribute of an object, are accessed

    Args:
        name (str): the name of the object that should be accessed; can contain dots (for attributes)
        times (int): how often the object specified in name should be accessed.
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

    rep = Reporter.active_reporter

    student_object_accesses = state.student_object_accesses
    student_mappings = state.student_oa_mappings

    if not not_accessed_msg:
        stud_name = name
        if "." in stud_name:
            for orig, full_name in student_mappings.items():
                if name.startswith(full_name): stud_name = name.replace(full_name, orig)

        add = " at least %s" % pythonwhat.utils.get_times(times) if times > 1 else ""
        not_accessed_msg = "Have you accessed `%s`%s?" % (stud_name, add)


    # name should be contained inside the student_object_accesses.
    # hack: add a dot and do a match on the name with the dot,
    # to make sure you're not matching substrings
    student_hits = [c for c in student_object_accesses if name + "." in c + "."]
    _msg = state.build_message(not_accessed_msg)
    rep.do_test(BiggerTest(len(student_hits) + 1, times, _msg))

