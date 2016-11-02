from pythonwhat.Feedback import Feedback
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, Test
from pythonwhat import utils
from pythonwhat.tasks import setUpNewEnvInProcess, breakDownNewEnvInProcess
from pythonwhat.check_funcs import check_node, check_part, check_part_index, multi, quiet, has_equal_part, with_context

from functools import partial

MSG_MISSING = "Define more `with` statements."
MSG_PREPEND = "In your {ordinal} {typestr}, "
MSG_PREPEND2 = "Check the {child[part]} in the {ordinal} `with` statement. "
MSG_NUM_CTXT = "make sure to use the correct number of context variables. It seems you defined too many."
MSG_NUM_CTXT2 = "make sure to use the correct number of context variables. It seems you defined too little."
MSG_CTXT_NAMES = "make sure to use the correct context variable names. Was expecting `{sol_part[target_vars]}` but got `{stu_part[target_vars]}`."


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
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_with")

    child = check_node('withs', index-1, "`with` statement", MSG_MISSING, MSG_PREPEND, state = state)
    child2 = check_node('withs', index-1, "`with` statement", MSG_MISSING, MSG_PREPEND2, state = state)
    quiet_child = quiet(1, child)

    if context_vals:
        # test num context vars ----
        too_many = len(child.student_parts['context']) > len(child.solution_parts['context'])
        if too_many:
            _msg = child.build_message(MSG_NUM_CTXT)
            rep.do_test(Test(Feedback(_msg, child.student_tree)))

        # test context var names ----
        for i in range(len(child.solution_parts['context'])):
            ctxt_state = check_part_index('context', i, "", state=child)
            has_equal_part('target_vars', MSG_CTXT_NAMES, state=ctxt_state)

    
    # Context sub tests ----
    if context_tests and not isinstance(context_tests, list): context_tests = [context_tests]

    for i, context_test in enumerate(context_tests or []):
        # partial the substate check, because the function uses two prepended messages
        check_context = partial(check_part_index, 'context', i, "%s context"%utils.get_ord(i+1), MSG_NUM_CTXT2)

        check_context(state=child)                   # test exist

        ctxt_state = check_context(state=child2)     # sub tests
        multi(context_test, state=ctxt_state)
    
    # Body sub tests ----
    if body is not None:
        body_state = check_part('body', 'body', state=child2)

        with_context(body, state=body_state)
