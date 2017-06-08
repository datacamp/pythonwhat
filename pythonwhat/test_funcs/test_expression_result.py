import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, Test
from pythonwhat import utils
from pythonwhat.tasks import getResultInProcess, ReprFail
from pythonwhat.check_funcs import has_equal_value


def test_expression_result(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           eq_condition="equal",
                           expr_code=None,
                           pre_code=None,
                           keep_objs_in_env=None,
                           error_msg=None,
                           state=None,
                           **kwargs):
    """Test result of expression.

    The code of the student is ran in the active state and the result of the evaluation is
    compared with the result of the solution. This can be used in nested pythonwhat calls
    like test_if_else. In these kind of calls, the code of the active state is set to
    the code in a part of the sub statement (e.g. the condition of an if statement). It
    has various parameters to control the execution of the (sub)expression.

    Args:
        extra_env (dict): set variables to the extra environment. They will update the student
          and solution environment in the active state before the student/solution code in the active
          state is ran. This argument should contain a dictionary with the keys the names of
          the variables you want to set, and the values are the values of these variables.
        context_vals (list): set variables which are bound in a for loop to certain values. This argument is
          only useful if you use the function in a test_for_loop. It contains a list with the values
          of the bound variables.
        incorrect_msg (str): feedback message if the result of the expression in the solution doesn't match
          the one of the student. This feedback message will be expanded if it is used in the context of
          another test function, like test_if_else.
        eq_condition (str): how results are compared. Currently, only "equal" is supported,
          meaning that the result in student and solution process should have exactly the same value.
        expr_code (str): if this variable is not None, the expression in the studeont/solution code will not
          be ran. Instead, the given piece of code will be ran in the student as well as the solution environment
          and the result will be compared.
        pre_code (str): the code in string form that should be executed before the expression is executed.
          This is the ideal place to set a random seed, for example.
        keep_obj_in_env (list()): a list of variable names that should be hold in the copied environment where
          the expression is evaluated. All primitive types are copied automatically, other objects have to
          be passed explicitely.
        error_msg (str): Message to override the default error message that is thrown if the expression resulted in an error.
        kwargs: named arguments which are the same as those used by ``has_equal_value``.

    :Example:
        Student code::

            a = 12
            if a > 3:
                print('test %d' % a)

        Solution code::

            a = 4
            b = 5
            if (a + 1) > (b - 1):
                print('test %d' % a)

        SCT::

            test_if_else(1,
                test = test_expression_result(
                        extra_env = { 'a': 3 }
                        incorrect_msg = "Test if `a` > 3"))

        This SCT will pass as the condition in the student's code (:code:`a > 3`) will evaluate to the
        same value as the code in the solution code (:code:`(a + 1) > (b - 1)`), with value of :code:`a` set
        to :code:`3`.

    """

    error_msg = error_msg or "Running an expression in the student process caused an error"
    if incorrect_msg is not None:
        feedback_msg = incorrect_msg
    else:
        # need to double bracket extra_env, so doesn't mess up str templating
        feedback_msg = (
                "FMT:Unexpected expression: expected `{sol_eval}`, got `{stu_eval}` with values{extra_env}."
                )

    has_equal_value(feedback_msg,
                    error_msg,
                    extra_env = extra_env,
                    context_vals=context_vals,
                    expr_code=expr_code,
                    pre_code=pre_code,
                    keep_objs_in_env=keep_objs_in_env,
                    state = state, **kwargs)
