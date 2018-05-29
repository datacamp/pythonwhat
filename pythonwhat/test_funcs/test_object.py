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

    child = check_object(name, undefined_msg or MSG_UNDEFINED, expand_msg = "", state=state)

    if do_eval:
        has_equal_value(incorrect_msg or MSG_INCORRECT, state=child)
