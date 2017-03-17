from pythonwhat.Reporter import Reporter
from pythonwhat.tasks import getKeysInProcess
from pythonwhat.check_object import check_object, is_instance, has_equal_key, has_key

MSG_UNDEFINED = "FMT:Are you sure you defined the dictionary `{index}`?"
MSG_NOT_INSTANCE = "FMT:`{parent[index]}` is not a dictionary."
MSG_KEY_MISSING = "FMT:Have you specified a key `{key}` inside `{parent[index]}`?"
MSG_INCORRECT_VAL = "FMT:Have you specified the correct value for the key `{key}` inside `{parent[index]}`?"

def test_dictionary(name,
                    keys=None,
                    undefined_msg=None,
                    not_dictionary_msg=None,
                    key_missing_msg=None,
                    incorrect_value_msg=None,
                    state=None):
    """Test the contents of a dictionary.
    """

    rep = Reporter.active_reporter

    child = check_object(name, undefined_msg or MSG_UNDEFINED, expand_msg = "", state=state, typestr="dictionary")
    is_instance(dict, not_dictionary_msg or MSG_NOT_INSTANCE, state=child)   # test instance

    # set keys or check if manual keys are valid
    if not keys: 
        keys = getKeysInProcess(name, state.solution_process)

    for key in keys:
        # check if key in dictionary
        has_equal_key(key, incorrect_value_msg or MSG_INCORRECT_VAL, key_missing_msg or MSG_KEY_MISSING, state=child)


def check_dict(name, undefined_msg=MSG_UNDEFINED, not_instance_msg=MSG_NOT_INSTANCE, expand_msg="", state=None):

    # test defined
    child = check_object(name, undefined_msg, state=state, typestr="dictionary")
    is_instance(dict, not_instance_msg, state=child)   # test instance

    return child

