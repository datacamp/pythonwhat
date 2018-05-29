from pythonwhat.parsing import ObjectAssignmentParser
from pythonwhat.Test import DefinedProcessTest, InstanceProcessTest, DefinedCollProcessTest, EqualValueProcessTest
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isDefinedInProcess, isInstanceInProcess, getValueInProcess, isDefinedCollInProcess, ReprFail
from pythonwhat.check_funcs import part_to_child, has_equal_value


MSG_PREPEND = "FMT:Check the variable `{index}`. "
MSG_UNDEFINED = "FMT:Are you sure you defined the {typestr}, `{index}`?"
MSG_INCORRECT_VAL = """FMT: Have you specified the correct value for "{key}" inside `{parent[sol_part][name]}`?"""
MSG_KEY_MISSING = "__JINJA__:There is no {{ 'column' if 'DataFrame' in parent.typestr else 'key' }} inside {{parent.index}}."

def check_object(index, missing_msg=MSG_UNDEFINED, expand_msg=MSG_PREPEND, state=None, typestr="variable"):
    """Check object existence (and equality)

    Check whether an object is defined in the student's environment, and zoom in on its value in both
    student and solution environment to inspect quality (with has_equal_value().

    Args:
        index (str): the name of the object which value has to be checked.
        missing_msg (str): feedback message when the object is not defined in the student's environment.
        expect_msg (str): prepending message to put in front.

    :Example:

        Student code::

            b = 1
            c = 3

        Solution code::

            a = 1
            b = 2
            c = 3

        SCT::

            Ex().check_object("a")                    # fail
            Ex().check_object("b")                    # pass
            Ex().check_object("b").has_equal_value()  # fail
            Ex().check_object("c").has_equal_value()  # pass

    """
    rep = Reporter.active_reporter

    if not isDefinedInProcess(index, state.solution_process):
        raise NameError("%r not in solution environment " % index)

    append_message = {'msg': expand_msg, 'kwargs': {'index': index, 'typestr': typestr}}

    # create child state, using either parser output, or create part from name
    fallback = lambda: ObjectAssignmentParser.get_part(index)
    stu_part = state.student_object_assignments.get(index, fallback())
    sol_part = state.solution_object_assignments.get(index, fallback())
    
    # test object exists
    _msg = state.build_message(missing_msg, append_message['kwargs'])
    rep.do_test(DefinedProcessTest(index, state.student_process, Feedback(_msg)))

    child = part_to_child(stu_part, sol_part, append_message, state)

    return child

def is_instance(inst, not_instance_msg="FMT:Is it a {inst.__name__}?", name=None, state=None):
    rep = Reporter.active_reporter

    sol_name = name or state.solution_parts.get('name')
    stu_name = name or state.student_parts.get('name')

    if not isInstanceInProcess(sol_name, inst, state.solution_process):
        raise ValueError("%r is not a %s in the solution environment" % (sol_name, type(inst)))

    _msg = state.build_message(not_instance_msg, {'inst': inst})
    feedback = Feedback(_msg, state.highlight)
    rep.do_test(InstanceProcessTest(stu_name, inst, state.student_process, feedback))

    return state

def has_key(key, key_missing_msg=MSG_KEY_MISSING, name = None, state=None):
    rep = Reporter.active_reporter

    sol_name = name or state.solution_parts.get('name')
    stu_name = name or state.student_parts.get('name')

    if not isDefinedCollInProcess(sol_name, key, state.solution_process):
        raise NameError("Not all keys you specified are actually keys in %s in the solution process" % sol_name)

    # check if key available
    _msg = state.build_message(key_missing_msg, {'key': key})
    rep.do_test(DefinedCollProcessTest(stu_name, key, state.student_process, 
                                       Feedback(_msg, state.highlight)))

    return state

def has_equal_key(key, incorrect_value_msg=MSG_INCORRECT_VAL, key_missing_msg=MSG_KEY_MISSING, name=None, state=None):
    rep = Reporter.active_reporter

    sol_name = name or state.solution_parts.get('name')
    stu_name = name or state.student_parts.get('name')

    has_key(key, key_missing_msg, state=state)

    sol_value, sol_str = getValueInProcess(sol_name, key, state.solution_process)
    if isinstance(sol_value, ReprFail):
        raise NameError("Value from %r can't be fetched from the solution process: %s" % c(sol_name, sol_value.info))

    # check if value ok
    _msg = state.build_message(incorrect_value_msg, {'key': key})
    rep.do_test(EqualValueProcessTest(stu_name, key, state.student_process, sol_value, Feedback(_msg, state.highlight)))

    return state
