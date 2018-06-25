from pythonwhat.check_funcs import has_equal_value, has_equal_output

def test_expression_result(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           expr_code=None,
                           pre_code=None,
                           error_msg=None,
                           state=None,
                           **kwargs):
    """Test result of expression.

    Use the new ``has_equal_value()`` function instead.
    """

    has_equal_value(incorrect_msg=incorrect_msg,
                    error_msg=error_msg,
                    extra_env = extra_env,
                    context_vals=context_vals,
                    expr_code=expr_code,
                    pre_code=pre_code,
                    state = state, **kwargs)


def test_expression_output(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           eq_condition="equal",
                           expr_code=None,
                           pre_code=None,
                           state=None,
                           **kwargs):
    """Test output of expression.

    Use `has_equal_output()` instead.
    """

    has_equal_output(incorrect_msg = incorrect_msg,
                     extra_env = extra_env,
                     context_vals=context_vals,
                     expr_code=expr_code,
                     pre_code=pre_code,
                     state = state,
                     **kwargs)

def test_object_after_expression(name,
                                 extra_env=None,
                                 context_vals=None,
                                 undefined_msg=None,
                                 incorrect_msg=None,
                                 expr_code=None,
                                 pre_code=None,
                                 state=None,
                                 **kwargs):
    """Test object after running an expression.

    Use ``has_equal_value()`` with the ``name`` argument instead.
    """

    state.highlight = state.student_object_assignments.get(name, {}).get('highlight')

    has_equal_value(
            incorrect_msg = incorrect_msg,
            error_msg = undefined_msg,
            undefined_msg = undefined_msg,
            extra_env=extra_env,
            context_vals=context_vals,
            pre_code=pre_code,
            name = name,
            expr_code = expr_code,
            state=state,
            **kwargs)
