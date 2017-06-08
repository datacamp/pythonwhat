from pythonwhat.check_funcs import has_equal_output

def test_expression_output(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           eq_condition="equal",
                           expr_code=None,
                           pre_code=None,
                           keep_objs_in_env=None,
                           state=None,
                           **kwargs):
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
        kwargs: named arguments which are the same as those used by ``has_equal_value``.

    :Example:
        Student code::

            a = 12
            if a > 3:
                print('test %d' % a)

        Soltuion code::

            a = 4
            if a > 3:
                print('test %d' % a)

        SCT::

            test_if_else(1,
                body = test_expression_output(
                        extra_env = { 'a': 5 },
                        incorrect_msg = "Print out the correct things"))

        This SCT will set :code:`a` to five, and run the body in both environments (:code:`print('test %d' %a)` in both cases).
        Since the they print the same output, the test will pass.
    """

    if incorrect_msg is not None:
        feedback_msg = incorrect_msg
    else:
        if expr_code is not None:
            prestring = "FMT:When running %s e" % expr_code
        else:
            prestring = "FMT:E"
        feedback_msg = "%sxpected output `{sol_eval}`, instead got `{stu_eval}`" % (prestring)
        if extra_env:
            # need double brackets to not screw up string formatting
            feedback_msg += "for values %s." % str(extra_env).replace('{','{{').replace('}','}}')
        else:
            feedback_msg += "."

    has_equal_output(incorrect_msg = feedback_msg,
                     error_msg = feedback_msg,
                     extra_env = extra_env,
                     context_vals=context_vals,
                     expr_code=expr_code,
                     pre_code=pre_code,
                     keep_objs_in_env=keep_objs_in_env,
                     state = state,
                     **kwargs)
