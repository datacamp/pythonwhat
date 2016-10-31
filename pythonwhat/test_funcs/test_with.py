from pythonwhat.Feedback import Feedback
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, Test
from pythonwhat import utils
from pythonwhat.tasks import setUpNewEnvInProcess, breakDownNewEnvInProcess
from pythonwhat.check_funcs import check_node, check_part, check_part_index, multi, quiet, has_equal_part

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

        solution_res = setUpNewEnvInProcess(process = body_state.solution_process,
                                            context = child.solution_parts['context'])
        if isinstance(solution_res, Exception):
            raise Exception("error in the solution, running test_with() on with %d: %s" % (index - 1, str(solution_res)))

        student_res = setUpNewEnvInProcess(process = state.student_process,
                                           context = child.student_parts['context'])
        if isinstance(student_res, AttributeError):
            rep.do_test(Test(Feedback("In your %s `with` statement, you're not using a correct context manager." % (utils.get_ord(index)), child.student_tree)))

        if isinstance(student_res, (AssertionError, ValueError, TypeError)):
            rep.do_test(Test(Feedback("In your %s `with` statement, the number of values in your context manager " + \
                "doesn't correspond to the number of variables you're trying to assign it to." % (utils.get_ord(index)), child.student_tree)))

        try:
            multi(body, state=body_state)
        finally:
            if breakDownNewEnvInProcess(process = state.solution_process):
                raise Exception("error in the solution, closing the %s with fails with: %s" %
                    (utils.get_ord(index), close_solution_context))

            if breakDownNewEnvInProcess(process = state.student_process):

                rep.do_test(Test(Feedback("Your %s `with` statement can not be closed off correctly, you're " + \
                                "not using the context manager correctly." % (utils.get_ord(index)), child.student_tree)),
                            fallback_ast = body_state.student_tree)
