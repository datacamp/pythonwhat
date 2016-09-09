import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest

from pythonwhat import utils

from pythonwhat.tasks import getOutputInProcess

def test_expression_output(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           eq_condition="equal",
                           expr_code=None,
                           pre_code=None,
                           keep_objs_in_env=None):
    """Test output of expression.

    The code of the student is ran in the active state and the output it generates is
    compared with the code of the solution. This can be used in nested pythonwhat calls
    like test_if_else. In these kind of calls, the code of the active state is set to
    the code in a part of the sub statement (e.g. the body of an if statement). It
    has various parameters to control the execution of the (sub)expression.

    Args:
        extra_env (dict): set variables to the extra environment. They will update the student
          and solution environment in the active state before the student/solution code in the active
          state is ran. This argument should contain a dictionary with the keys the names of
          the variables you want to set, and the values are the values of these variables.
        context_vals (list): set variables which are bound in a for loop to certain values. This argument is
          only useful if you use the function in a test_for_loop. It contains a list with the values
          of the bound variables.
        incorrect_msg (str): feedback message if the output of the expression in the solution doesn't match
          the one of the student. This feedback message will be expanded if it is used in the context of
          another test function, like test_if_else.
        eq_condition (str): how objects are compared. Currently, only "equal" is supported,
          meaning that the result in student and solution process should have exactly the same value.
        expr_code (str): if this variable is not None, the expression in the student/solution code will not
          be ran. Instead, the given piece of code will be ran in the student as well as the solution environment
          and the result will be compared.
        pre_code (str): the code in string form that should be executed before the expression is executed.
          This is the ideal place to set a random seed, for example.
        keep_obj_in_env (list()): a list of variable names that should be hold in the copied environment where
          the expression is evaluated. All primitive types are copied automatically, other objects have to
          be passed explicitely.

    Examples:
        Student code

        |    ``a = 12``
        |    ``if a > 3:``
        |        ``print('test %d' % a)``

        Soltuion code

        |   ``a = 4``
        |   ``if a > 3:``
        |       ``print('test %d' % a)``

        SCT

        |   ``test_if_else(1,``
        |       ``body = lambda: test_expression_output(extra_env = { 'a': 5 },``
        |           ``incorrect_msg = "Print out the correct things"))``

        This SCT will pass as the subexpression will output 'test 5' in both student as solution environment,
        since the extra environment sets `a` to 5.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_expression_output")

    eq_map = {"equal": EqualTest}

    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)

    out_student = getOutputInProcess(tree = state.student_tree,
                                     process = state.student_process,
                                     extra_env = extra_env,
                                     context = state.student_context,
                                     context_vals = context_vals,
                                     pre_code = pre_code,
                                     expr_code = expr_code,
                                     keep_objs_in_env = keep_objs_in_env)

    out_solution = getOutputInProcess(tree = state.solution_tree,
                                      process = state.solution_process,
                                      extra_env = extra_env,
                                      context = state.solution_context,
                                      context_vals = context_vals,
                                      pre_code = pre_code,
                                      expr_code = expr_code,
                                      keep_objs_in_env = keep_objs_in_env)

    if out_solution is None:
        raise ValueError("test_expression_output raised error in solution process")

    out_student = out_student or "Error"

    if incorrect_msg is not None:
        feedback_msg = incorrect_msg
    else:
        if expr_code is not None:
            prestring = "When running %s e" % expr_code
        else:
            prestring = "E"
        feedback_msg = "%sxpected output `%s`, instead got `%s`" % \
            (prestring, utils.shorten_str(str(out_solution)), utils.shorten_str(str(out_student)))
        if extra_env:
            feedback_msg += "for values %s." % str(extra_env)
        else:
            feedback_msg += "."

    Reporter.active_reporter.do_test(
        eq_map[eq_condition](
            out_solution,
            out_student,
            feedback_msg))
