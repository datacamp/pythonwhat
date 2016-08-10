import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, EquivalentTest

from pythonwhat.test_object import get_assignment_node
from pythonwhat.Feedback import Feedback
from pythonwhat import utils

from pythonwhat.tasks import getObjectAfterExpressionInProcess


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

    Examples:
      Student code

        | ``count = 1``
        | ``for i in range(100):``
        |     ``count = count + i``

        Solution code

        | ``count = 15``
        | ``for n in range(30):``
        |     ``count = count + n``

        SCT

        | ``test_for_loop(1,``
        |     ``body = lambda: test_object_after_expression("count",``
        |         ``extra_env = { 'count': 20 },``
        |         ``contex_vals = [ 10 ])``

        This SCT will pass as the value of `count` is updated identically in the body of the for loop in the
        student code and solution code.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_object_after_expression")

    state.extract_object_assignments()
    student_obj_ass = state.student_object_assignments

    if not undefined_msg:
        undefined_msg = "Have you defined `%s` without errors?" % name

    if not incorrect_msg:
        incorrect_msg = "Are you sure you assigned the correct value to `%s`?" % name

    eq_map = {"equal": EqualTest,
              "equivalent": EquivalentTest}

    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)


    eval_student, str_student = getObjectAfterExpressionInProcess(tree = state.student_tree,
                                                                  name = name,
                                                                  process = state.student_process,
                                                                  extra_env = extra_env,
                                                                  context = state.context_student,
                                                                  context_vals = context_vals,
                                                                  pre_code = pre_code,
                                                                  keep_objs_in_env = keep_objs_in_env)

    eval_solution, str_solution = getObjectAfterExpressionInProcess(tree = state.solution_tree,
                                                                    name = name,
                                                                    process = state.solution_process,
                                                                    extra_env = extra_env,
                                                                    context = state.context_solution,
                                                                    context_vals = context_vals,
                                                                    pre_code = pre_code,
                                                                    keep_objs_in_env = keep_objs_in_env)

    if str_solution is None:
        raise ValueError("Running the expression in the solution environment caused an error.")

    if str_student == "undefined" or str_student is None:
        rep.do_test(Test(undefined_msg))
        return

    ass_node = get_assignment_node(student_obj_ass, name)
    rep.do_test(eq_map[eq_condition](eval_student,
                                     eval_solution,
                                     Feedback(incorrect_msg, ass_node)))

