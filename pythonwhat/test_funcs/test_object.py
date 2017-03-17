from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import part_to_child, has_equal_value
from pythonwhat.check_object import check_object, MSG_UNDEFINED

MSG_UNDEFINED = "FMT:Have you defined `{index}`?"
MSG_INCORRECT = "FMT:The contents of `{parent[index]}` aren't correct."

def test_object(name,
                eq_condition="equal",
                eq_fun=None,
                do_eval=True,
                undefined_msg=None,
                incorrect_msg=None,
                state=None):
    """Test object.

    The value of an object in the ending environment is compared in the student's environment and the
    solution environment.

    Args:
        name (str): the name of the object which value has to be checked.
        eq_condition (str): how objects are compared. Currently, only "equal" is supported,
          meaning that the object in student and solution process should have exactly the same value.
        do_eval (bool): if False, the object will only be checked for existence. Defaults to True.
        undefined_msg (str): feedback message when the object is not defined
        incorrect_msg (str): feedback message if the value of the object in the solution environment doesn't match
          the one in the student environment.

    :Example:

        Student code::

            a = 1
            b = 5

        Solution code::

            a = 1
            b = 2

        SCT::

            test_object("a") # pass
            test_object("b") # fail

        Note that the student code below would fail both tests::

            a = 1
            b = 2
            a = 3 # incorrect final value of a

    """
    rep = Reporter.active_reporter

    child = check_object(name, undefined_msg or MSG_UNDEFINED, expand_msg = "", state=state)

    if do_eval:

        has_equal_value(incorrect_msg or MSG_INCORRECT, state=child)
