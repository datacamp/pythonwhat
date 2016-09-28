from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedProcessTest, InstanceProcessTest, DefinedCollProcessTest, EqualValueProcessTest
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isDefinedInProcess, isInstanceInProcess, getKeysInProcess, getValueInProcess, ReprFail

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
    rep.set_tag("fun", "test_dictionary")

    solution_process = state.solution_process
    student_process = state.student_process

    if not isDefinedInProcess(name, solution_process):
        raise NameError("%r not in solution environment" % name)

    if  not isInstanceInProcess(name, dict, solution_process):
        raise ValueError("%r is not a dictionary in the solution environment" % name)

    # Check if defined
    if not undefined_msg:
        undefined_msg = "Are you sure you defined the dictionary `%s`?" % name
    rep.do_test(DefinedProcessTest(name, student_process, Feedback(undefined_msg)))
    if rep.failed_test:
        return

    if not not_dictionary_msg:
        not_dictionary_msg = "`%s` is not a dictionary." % name
    rep.do_test(InstanceProcessTest(name, dict, student_process, Feedback(not_dictionary_msg)))
    if rep.failed_test:
        return

    sol_keys = getKeysInProcess(name, solution_process)
    if sol_keys is None:
        raise ValueError("Something went wrong in figuring out the keys for %s in the solution process" % name)

    # set keys or check if manual keys are valid
    if keys is None:
        keys = sol_keys
    elif set(keys) > set(sol_keys):
        raise NameError("Not all keys you specified are actually keys in %s in the solution process" % name)

    # Check if keys and values ok
    for key in keys:

        # check if key available
        if not key_missing_msg:
            msg = "Have you specified a key `%s` inside `%s`?" % (str(key), name)
        else:
            msg = key_missing_msg
        rep.do_test(DefinedCollProcessTest(name, key, student_process, Feedback(msg)))
        if rep.failed_test:
            return


        sol_value = getValueInProcess(name, key, solution_process)
        if isinstance(sol_value, ReprFail):
            raise NameError("Value from %r can't be fetched from the solution process: %s" % c(name, sol_value.info))

        # check if value ok
        if not incorrect_value_msg:
            msg = "Have you specified the correct value for the key `%s` inside `%s`?" % (str(key), name)
        else:
            msg = incorrect_value_msg
        rep.do_test(EqualValueProcessTest(name, key, student_process, sol_value, Feedback(msg)))
        if rep.failed_test:
            return
