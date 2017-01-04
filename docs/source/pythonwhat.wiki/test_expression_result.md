test_expression_result
----------------------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_expression_result.test_expression_result
```

    def test_expression_result(extra_env=None,
                               context_vals=None,
                               incorrect_msg=None,
                               eq_condition="equal",
                               expr_code=None,
                               pre_code=None,
                               keep_objs_in_env=None,
                               error_msg=None)

`test_expression_result()` works pretty much the same as `test_expression_output()` and takes the same arguments. However, in this case, the expression should be a single expression and can't be a 'tree of expressions', such as the entire body of a function definition for example. Currently, the only places where `test_expression_result()` is used, is inside inherently 'single expression parts' of your code, such as the sequence specification of a `for` loop, the expression of a lambda function, etc.

The example in the [`test_expression_output()` article](test_expression_output.md) also explains the use of `test_expression_result()`.
