from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedProcessTest, EqualTest
from pythonwhat.Feedback import Feedback

def test_dictionary(name,
                    keys=None,
                    undefined_msg=None,
                    not_dictionary_msg=None,
                    key_missing_msg=None,
                    incorrect_value_msg=None):
    """Test the contents of a dictionary.
    """

    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_dictionary")

    solution_env = state.solution_env
    student_env = state.student_env

    try:
        solution_dict = solution_env[name]
        assert isinstance(solution_dict, dict)
    except KeyError:
        raise NameError("%r not in solution environment" % name)
    except AssertionError:
        raise ValueError("%r is not a dictionary in the solution environment" % name)

    # Check if defined
    if not undefined_msg:
        undefined_msg = "Are you sure you defined the dictionary `%s`?" % name
    rep.do_test(DefinedTest(name, student_env, Feedback(undefined_msg)))
    if rep.failed_test:
        return

    student_dict = student_env[name]

    # Check if it's a dictionary
    if not not_dictionary_msg:
        not_dictionary_msg = "`%s` is not a dictionary." % name
    rep.do_test(EqualTest(student_dict.__class__, dict, Feedback(not_dictionary_msg)))
    if rep.failed_test:
        return

    keys = keys or list(solution_dict.keys())


    # Check if keys and values ok
    for key in keys:

        try:
            solution_value = solution_dict[key]
        except KeyError:
            raise NameError("%r is not a key of the %r dictionary in the solution environment" % (str(key), name))

        # check if key available
        if not key_missing_msg:
            msg = "Have you specified a key `%s` inside `%s`?" % (str(key), name)
        else:
            msg = key_missing_msg
        rep.do_test(DefinedTest(key, student_dict, Feedback(msg)))
        if rep.failed_test:
            return

        # check if value ok
        if not incorrect_value_msg:
            msg = "Have you specified the correct value for the key `%s` inside `%s`?" % (str(key), name)
        else:
            msg = incorrect_value_msg
        rep.do_test(EqualTest(student_dict[key], solution_value, Feedback(msg)))
        if rep.failed_test:
            return
