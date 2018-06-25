from pythonwhat.Feedback import Feedback
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, Test
from pythonwhat import utils
from pythonwhat.check_funcs import check_node, check_part, check_part_index, multi, quiet, has_equal_part, with_context, has_equal_part_len
from pythonwhat.check_has_context import has_context

from functools import partial

MSG_MISSING = "Define more `with` statements."
MSG_PREPEND = "FMT:Check the {typestr}. "
MSG_NUM_CTXT = "Make sure to use the correct number of context variables. It seems you defined too many."
MSG_NUM_CTXT2 = "Make sure to use the correct number of context variables. It seems you defined too little."
MSG_CTXT_NAMES = "FMT:Make sure to use the correct context variable names. Was expecting `{sol_vars}` but got `{stu_vars}`."


def test_with(index,
              context_vals=False, # whether to check number of context vals
              context_tests=None, # check on context expressions
              body=None,
              undefined_msg=None,
              context_vals_len_msg=None,
              context_vals_msg=None,
              expand_message=True,
              state=None):
    """Test a with statement.
with open_file('...') as bla:

    [ open_file('...').__enter__() ]


with open_file('...') as file:
    [ ]

    """

    check_with = partial(check_node, 'withs', index-1, "{ordinal} `with` statement", MSG_MISSING, state=state)

    child =  check_with(MSG_PREPEND if expand_message else "")
    child2 = check_with(MSG_PREPEND if expand_message else "")

    if context_vals:
        # test context var names ----
        has_context(incorrect_msg=context_vals_msg or MSG_CTXT_NAMES, exact_names = True, state=child)

        # test num context vars ----
        has_equal_part_len('context', MSG_NUM_CTXT, state=child)
        
    
    # Context sub tests ----
    if context_tests and not isinstance(context_tests, list): context_tests = [context_tests]

    expand_msg = None if expand_message else ""
    for i, context_test in enumerate(context_tests or []):
        # partial the substate check, because the function uses two prepended messages
        check_context = partial(check_part_index, 'context', i, "%s context"%utils.get_ord(i+1), missing_msg=MSG_NUM_CTXT2, expand_msg=expand_msg)

        check_context(state=child)                   # test exist

        ctxt_state = check_context(state=child2)     # sub tests
        multi(context_test, state=ctxt_state)
    
    # Body sub tests ----
    if body is not None:
        body_state = check_part('body', 'body', expand_msg=expand_msg, state=child2)

        with_context(body, state=body_state)
