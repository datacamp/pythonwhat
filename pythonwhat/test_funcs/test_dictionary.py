from pythonwhat.Reporter import Reporter
from pythonwhat.Test import InstanceProcessTest, DefinedCollProcessTest, EqualValueProcessTest
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isInstanceInProcess, getKeysInProcess, getValueInProcess, isDefinedCollInProcess, ReprFail
from .test_object import check_object

MSG_UNDEFINED = "Are you sure you defined the dictionary `{parent[sol_part][name]}`?"
MSG_NOT_INSTANCE = "`{parent[sol_part][name]}` is not a dictionary."
MSG_KEY_MISSING = "Have you specified a key `{key}` inside `{parent[sol_part][name]}`?"
MSG_INCORRECT_VAL = "Have you specified the correct value for the key `{key}` inside `{parent[sol_part][name]}`?"

def test_dictionary(name,
                    keys=None,
                    undefined_msg=MSG_UNDEFINED,
                    not_dictionary_msg=MSG_NOT_INSTANCE,
                    key_missing_msg=MSG_KEY_MISSING,
                    incorrect_value_msg=MSG_INCORRECT_VAL,
                    state=None):
    """Test the contents of a dictionary.
    """

    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_dictionary")

    child = check_dict(name, undefined_msg or MSG_UNDEFINED, not_dictionary_msg or MSG_NOT_INSTANCE, state=state)

    # set keys or check if manual keys are valid
    if not keys: 
        keys = getKeysInProcess(name, state.solution_process)

    for key in keys:
        # check if key in dictionary
        test_key(name, key, incorrect_value_msg or MSG_INCORRECT_VAL, key_missing_msg or MSG_KEY_MISSING, state=child)

# Check functions -------------------------------------------------------------

def check_dict(name, undefined_msg=MSG_UNDEFINED, not_instance_msg=MSG_NOT_INSTANCE, state=None):

    child = check_object(name, undefined_msg, state=state)   # test defined
    is_instance(name, dict, not_instance_msg, state=child)   # test instance

    return child

def is_instance(name, inst, not_instance_msg, state=None):
    rep = Reporter.active_reporter

    if not isInstanceInProcess(name, inst, state.solution_process):
        raise ValueError("%r is not a %s in the solution environment" % (name, type(inst)))

    _msg = state.build_message(not_instance_msg)
    feedback = Feedback(_msg, state.highlight)
    rep.do_test(InstanceProcessTest(name, inst, state.student_process, feedback))

def has_key(name, key, key_missing_msg, state=None):
    rep = Reporter.active_reporter

    if not isDefinedCollInProcess(name, key, state.solution_process):
        raise NameError("Not all keys you specified are actually keys in %s in the solution process" % name)

    # check if key available
    _msg = state.build_message(key_missing_msg, {'key': key})
    rep.do_test(DefinedCollProcessTest(name, key, state.student_process, 
                                       Feedback(_msg, state.highlight)))

def test_key(name, key, incorrect_value_msg, key_missing_msg, state=None):
    rep = Reporter.active_reporter

    has_key(name, key, key_missing_msg, state=state)

    sol_value, sol_str = getValueInProcess(name, key, state.solution_process)
    if isinstance(sol_value, ReprFail):
        raise NameError("Value from %r can't be fetched from the solution process: %s" % c(name, sol_value.info))

    # check if value ok
    _msg = state.build_message(incorrect_value_msg, {'key': key})
    rep.do_test(EqualValueProcessTest(name, key, state.student_process, sol_value, Feedback(_msg, state.highlight)))
