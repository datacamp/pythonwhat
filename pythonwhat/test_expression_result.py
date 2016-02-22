import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, EquivalentTest

from pythonwhat import utils

import copy


def test_expression_result(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           eq_condition="equal",
                           expr_code=None,
                           pre_code=None,
                           keep_objs_in_env=None):
    """Test result of expression.

    The code of the student is ran in the active state and the result of the evaluation is
    compared with the result of the solution. This can be used in nested pythonwhat calls
    like test_if_else. In these kind of calls, the code of the active state is set to 
    the code in a part of the sub statement (e.g. the condition of an if statement). It 
    has various parameters to control the execution of the (sub)expression.

    Example:
      student_code
        | ``a = 12``
        | ``if a > 3:``
        | ``    print('test %d' % a)``
      solution_code
        | ``a = 4``
        | ``b = 5``
        | ``if (a + 1) > (b - 1):``
        | ``    print('test %d' % a)``
      sct
        | ``test_if_else(1,``
        | ``             test = lambda: test_expression_result(extra_env = { 'a': 3 }``
        | ``                                                   incorrect_msg = "Test if `a` > 3"))``
      This SCT will pass as the condition in the student's code (`a > 3`) will evaluate to the
      same value as the code in the solution code (`(a + 1) > (b - 1)`), with value of `a` set
      to `3`. 

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
        eq_condition (str): the condition which is checked on the eval of the group. Can be "equal" -- 
          meaning that the operators have to evaluate to exactly the same value, or "equivalent" -- which
          can be used when you expect an integer and the result can differ slightly. Defaults to "equal".
        expr_code (str): if this variable is not None, the expression in the studeont/solution code will not
          be ran. Instead, the given piece of code will be ran in the student as well as the solution environment
          and the result will be compared.
        pre_code (str): the code in string form that should be executed before the expression is executed.
          This is the ideal place to set a random seed, for example.
        keep_obj_in_env (list()): a list of variable names that should be hold in the copied environment where
          the expression is evaluated. All primitive types are copied automatically, other objects have to 
          be passed explicitely.
    """
    state = State.active_state
    rep = Reporter.active_reporter

    eq_map = {"equal": EqualTest, "equivalent": EquivalentTest}

    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)

    student_expr = state.student_tree
    solution_expr = state.solution_tree

    student_env = utils.copy_env(state.student_env, keep_objs_in_env)
    solution_env = utils.copy_env(state.solution_env, keep_objs_in_env)

    if extra_env:
        student_env.update(copy.deepcopy(extra_env))
        solution_env.update(copy.deepcopy(extra_env))

    if context_vals is not None:
        if len(state.context_student) > 1:
            student_env.update({key: value for (key, value) in zip(
                state.context_student, context_vals)})
        else:
            student_env.update({state.context_student[0]: (
                context_vals[0] if len(context_vals) == 1 else context_vals)})

        if len(state.context_solution) > 1:
            solution_env.update({key: value for (key, value) in zip(
                state.context_solution, context_vals)})
        else:
            solution_env.update({state.context_solution[0]: (
                context_vals[0] if len(context_vals) == 1 else context_vals)})

    try:
        if pre_code is not None:
            exec(pre_code, student_env)
        if expr_code is None:
            eval_student = eval(
                compile(
                    ast.Expression(student_expr),
                    "<student>",
                    "eval"),
                student_env)
        else:
            eval_student = eval(expr_code, student_env)
    except:
        eval_student = None

    if pre_code is not None:
        exec(pre_code, student_env)
    if expr_code is None:
        eval_solution = eval(
            compile(
                ast.Expression(solution_expr),
                "<solution>",
                "eval"),
            solution_env)
    else:
        eval_solution = eval(expr_code, solution_env)

    if incorrect_msg is not None:
        feedback_msg = incorrect_msg
    else:
        feedback_msg = "Unexpected expression: expected `%s`, got `%s` with values" + \
            ((" " + str(extra_env)) if extra_env else ".")
        feedback_msg = feedback_msg % (utils.shorten_str(
            str(eval_solution)), utils.shorten_str(str(eval_student)))

    Reporter.active_reporter.do_test(
        eq_map[eq_condition](
            eval_solution,
            eval_student,
            feedback_msg))
