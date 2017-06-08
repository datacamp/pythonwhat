from pythonwhat.check_funcs import has_equal_value, check_part

def test_object_after_expression(name,
                                 extra_env=None,
                                 context_vals=None,
                                 undefined_msg=None,
                                 incorrect_msg=None,
                                 eq_condition="equal",
                                 expr_code=None,
                                 pre_code=None,
                                 keep_objs_in_env=None,
                                 state=None,
                                 **kwargs):
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
          only useful if you use the function in a test_for_loop or test_function_definition.
          It contains a list with the values of the bound variables.
        incorrect_msg (str): feedback message if the value of the object in the solution environment doesn't match
          the one in the student environment. This feedback message will be expanded if it is used in the context of
          another test function, like test_for_loop.
        eq_condition (str): how objects are compared. Currently, only "equal" is supported,
            meaning that the resulting objects in student and solution process should have exactly the same value.
        expr_code (str): if this variable is not None, the expression in the studeont/solution code will not
          be ran. Instead, the given piece of code will be ran in the student as well as the solution environment
          and the result will be compared.
        pre_code (str): the code in string form that should be executed before the expression is executed.
          This is the ideal place to set a random seed, for example.
        keep_obj_in_env (list()): a list of variable names that should be hold in the copied environment where
          the expression is evaluated. All primitive types are copied automatically, other objects have to
          be passed explicitely.
        kwargs: named arguments which are the same as those used by ``has_equal_value``.

    :Example:

        Student code::

            count = 1
            for i in range(100):
                count = count + i

        Solution code::

            count = 15
            for n in range(30):
                count = count + n

        SCT::

            test_for_loop(1,
                body = test_object_after_expression("count",
                        extra_env = { 'count': 20 },
                        contex_vals = [ 10 ])

        This SCT will pass as the value of `count` is updated identically in the body of the for loop in the
        student code and solution code.
    """

    if not undefined_msg:
        undefined_msg = "Have you defined `%s` without errors?" % name

    if not incorrect_msg:
        incorrect_msg = "Are you sure you assigned the correct value to `%s`?" % name

    ass_node = state.student_object_assignments.get(name, {}).get('highlight')

    has_equal_value(
            incorrect_msg = incorrect_msg,
            error_msg = undefined_msg,
            undefined_msg = undefined_msg,
            extra_env=extra_env,
            context_vals=context_vals,
            pre_code=pre_code,
            keep_objs_in_env=keep_objs_in_env,
            name = name,
            highlight = ass_node,
            expr_code = expr_code,
            state=state,
            **kwargs)
