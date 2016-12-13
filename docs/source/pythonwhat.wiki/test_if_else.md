test_if_else
------------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_if_else.test_if_else
```

    test_if_else(index=1,
                 test=None,
                 body=None,
                 orelse=None,
                 expand_message=True)

`test_if_else()` allows you to robustly check `if` statements, optionally extended with `elif` and `else` components. For each of the components of an if-else construct `test_if_else()` takes several 'sub-SCTs'. These 'sub-SCTs', that you have to pass in the form of lambda functions or through a function that defines all tests, are executed on these separate parts of the submission.

### Example 1

Suppose an exercise asks the student to code up the following if-else construct:

    *** =solution
    ```{python}
    # a is set to 5
    a = 5

    # If a < 5, print out "It's small", else print out "It's big"
    if a < 5:

    else:
      print("It's big")
    ```

The `if-else` construct here consists of three parts:

- The condition to check: `a < 5`. The `test` argument of `test_if_else()` specifies the sub-SCT to test this.
- The body of the `if` statement: `print("It's small")`. The `body` argument of `test_if_else()` specifies the sub-SCT to test this.
- The else part: `print("It's big")`. The `orelse` argument of `test_if_else()` specifies the sub-SCT to ttest this.

You can thus write our SCT as follows. Notice that for the `test` argument a function is used to specify different tests; for the `body` and `orelse` arguments two lambda functions suffise.

    *** =sct
    ```{python}
    def sct_on_condition_test():
      test_expression_result({"a": 4})
      test_expression_result({"a": 5})
      test_expression_result({"a": 6})

    test_if_else(index = 1,
                 test = sct_on_condition_test,
                 body = lambda: test_function("print")
                 orelse = lambda: test_function("print"))
    ```

#### The `test` part

Have a look at the `sct_on_condition_test()`, that is used to specify the sub-SCT for the `test` part of the if-else-construct, so `a < 5`. It contains three calls of the `test_expression_result` function. These functions are executed in a 'narrow scope' that only considers the condition of the student code, and the condition of the solution code.

More specifically, `test_expression_result({"a": 5})` will check whether executing the `if` condition that the student coded when `a` equals 5 leads to the same result as executing the `if` condition that is coded in the solution when `a` equals 5. That way, you can robustly check the validity of the `if` test. There are three `test_expression_result()` calls to see if the condition makes sense for different inputs.

Suppose that the student incorrectly used the condition `a < 6` instead of `a < 5`. `test_expression_result({"a": 5})` will see what the result is of `a < 6` if `a` equals 5. The result is `True`. Next, it checks the result of `a < 5`, the `if` condition of the solution, which is `False`. There is a mismatch between the 'student result' and the 'solution result', and a meaningful feedback messages is generated.

#### The `body` and `orelse` parts

In a similar way, the functions that are used as lambda functions in both the `body` and `orelse` part, will also be executed in a 'narrow scope', where only the `body` and `orelse` part of the student's submission and the solution are used.

