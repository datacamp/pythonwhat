import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedTest, EqualEnvironmentTest, EquivalentEnvironmentTest

from pythonwhat import utils

import copy


def test_object_after_expression(name,
                                 extra_env=None,
                                 context_vals=None,
                                 undefined_msg=None,
                                 incorrect_msg=None,
                                 eq_condition="equal",
                                 pre_code=None,
                                 keep_objs_in_env=None):
    """Test object after expression.

    The code of the student is ran in the active state and the the value of the given object is
    compared with the value of that object in the solution. This can be used in nested pythonwhat calls
    like test_for_loop. In these kind of calls, the code of the active state is set to 
    the code in a part of the sub statement (e.g. the body of a for loop). It has various
    parameters to control the execution of the (sub)expression. This test function is ideal to check if
    a value is updated correctly in the body of a for loop.

    Example:
      student_code
        | ``count = 1``
        | ``for i in range(100):``
        | ``    count = count + i``
      solution_code
        | ``count = 15``
        | ``for n in range(30):``
        | ``    count = count + n``
      sct
        | ``test_for_loop(1,``
        | ``              body = lambda: test_object_after_expression("count",``
        | ``                                                          extra_env = { 'count': 20 },``
        | ``                                                          contex_vals = [ 10 ])``
      This SCT will pass as the value of `count` is updated identically in the body of the for loop in the
      student code and solution code. 

    Args:
        name (str): the name of the object which value has to be checked after evaluation of the expression.
        extra_env (dict): set variables to the extra environment. They will update the student
          and solution environment in the active state before the student/solution code in the active 
          state is ran. This argument should contain a dictionary with the keys the names of 
          the variables you want to set, and the values are the values of these variables.
        context_vals (list): set variables which are bound in a for loop to certain values. This argument is
          only useful if you use the function in a test_for_loop. It contains a list with the values 
          of the bound variables.
        incorrect_msg (str): feedback message if the value of the object in the solution environment doesn't match
          the one in the student environment. This feedback message will be expanded if it is used in the context of
          another test function, like test_for_loop.
        eq_condition (str): the condition which is checked on the eval of the object. Can be "equal" -- 
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

    undefined_msg, incorrect_msg = build_strings(
        undefined_msg, incorrect_msg, name)

    eq_map = {"equal": EqualEnvironmentTest,
              "equivalent": EquivalentEnvironmentTest}

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
        exec(compile(student_expr, "<student>", "exec"), student_env)
    except:
        pass

    if pre_code is not None:
        exec(pre_code, solution_env)
    exec(compile(solution_expr, "<solution>", "exec"), solution_env)

    rep.do_test(DefinedTest(name, student_env, undefined_msg))
    if (rep.failed_test):
        return

    rep.do_test(
        eq_map[eq_condition](
            name,
            student_env,
            solution_env,
            incorrect_msg))


def build_strings(undefined_msg, incorrect_msg, name):
    if not undefined_msg:
        undefined_msg = "Have you defined `" + name + "`?"

    if not incorrect_msg:
        incorrect_msg = "Are you sure you assigned the correct value to `" + name + "`?"

    return(undefined_msg, incorrect_msg)
