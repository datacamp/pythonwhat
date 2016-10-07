import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, Test
from pythonwhat import utils
from pythonwhat.tasks import getResultInProcess, ReprFail


def test_expression_result(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           eq_condition="equal",
                           expr_code=None,
                           pre_code=None,
                           keep_objs_in_env=None,
                           error_msg=None,
                           state=None):
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

    Examples:
        Student code

        | ``a = 12``
        | ``if a > 3:``
        |     ``print('test %d' % a)``

        Solution code

        | ``a = 4``
        | ``b = 5``
        | ``if (a + 1) > (b - 1):``
        |     ``print('test %d' % a)``

        SCT

        | ``test_if_else(1,``
        |     ``test = lambda: test_expression_result(extra_env = { 'a': 3 }``
        |         ``incorrect_msg = "Test if `a` > 3"))``

        This SCT will pass as the condition in the student's code (`a > 3`) will evaluate to the
        same value as the code in the solution code (`(a + 1) > (b - 1)`), with value of `a` set
        to `3`.

    """
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_expression_result")

    eq_map = {"equal": EqualTest}

    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)

    eval_solution, str_solution = getResultInProcess(tree = state.solution_tree,
                                                     process = state.solution_process,
                                                     extra_env = extra_env,
                                                     context = state.solution_context,
                                                     context_vals = context_vals,
                                                     pre_code = pre_code,
                                                     expr_code = expr_code,
                                                     keep_objs_in_env = keep_objs_in_env)

    if str_solution is None:
      raise ValueError("Running the expression in the solution process caused an error.")
    if isinstance(eval_solution, ReprFail):
      raise ValueError("The result of running the expression in the solution process couldn't be figured out: " + eval_solution.info)

    eval_student, str_student = getResultInProcess(tree = state.student_tree,
                                                   process = state.student_process,
                                                   extra_env = extra_env,
                                                   context = state.student_context,
                                                   context_vals = context_vals,
                                                   pre_code = pre_code,
                                                   expr_code = expr_code,
                                                   keep_objs_in_env = keep_objs_in_env)


    if str_student is None:
        rep.do_test(Test(error_msg or "Running an expression in the student process caused an error"))
        return

    if eval_student is None:
        rep.do_test(Test(error_msg or "Running an expression in the student process caused an error"))
        return

    if incorrect_msg is not None:
        feedback_msg = incorrect_msg
    else:
        feedback_msg = "Unexpected expression: expected `%s`, got `%s` with values" + \
            ((" " + str(extra_env)) if extra_env else ".")
        feedback_msg = feedback_msg % (utils.shorten_str(
            str_solution), utils.shorten_str(str_student))

    rep.do_test(
        eq_map[eq_condition](
            eval_solution,
            eval_student,
            feedback_msg))
