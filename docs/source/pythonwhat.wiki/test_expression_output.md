test_expression_output
----------------------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_expression_output.test_expression_output
```

    def test_expression_output(extra_env=None,
                               context_vals=None,
                               incorrect_msg=None,
                               eq_condition="equal",
                               expr_code=None,
                               pre_code=None,
                               keep_objs_in_env=None)


`test_expression_output()` is similar to `test_expression_result()`, but instead of checking the result, it checks the output that a single or a set of expressions generates. Typically, this function is used as a sub-test inside other test functions, such as `test_for_loop()` and `test_with()`.

By default, the `test_expression_output()` will execute the 'active expression(s)'; if it's used as a top-level SCT function, that is the entire student submission. If it's used inside the `body` of the `test_for_loop()` function, for example, the entire for loop's body will executed and the output will be compared to the solution. With `expr_code`, you can override this default expression tree. With `pre_code`, you can prepend the execution of the default expression tree with some extra code, for example to set some variables.

Oftentimes, the expression you want to check the output for does not have all variables to its disposal that it requires. Remember that the process in which the expression is evaluated only contains the variables that are available in the global scope. If you're for example running the body of a function definition, this means that the local variables, that are for example passed into the function as arguments, are not all available during execution. To make these variables available, you can set the `extra_env` and `context_vals` arguments. The former is to specify extra variables, with a dictionary. The latter is to specify so called context values; the objects you specify here should not be named; this is to make function definition arguments, iterators in for loops, context variables in `with` constructs, etc, name-independent.

### Example 1

Suppose we want the student to define a function, that loops over the elements in a dictionary, and prints out each key and value, as follows:

    *** =solution
    ```{python}
    def print_dict(my_dict):
        for key, value in my_dict.items():
            print(key + " - " + str(value))
    ```

An appropriate SCT for this exercise could be the following (for clarity, we're not using any default messages):

    *** =sct
    ```{python}
    def fun_body_test():
        def for_iter_test():
            example_dict = {'a': 2, 'b': 3}
            test_expression_result(context_vals = [example_dict])
        def for_body_test():
            test_expression_output(context_vals = ['c', 3])
        test_for_loop(for_iter = for_iter_test, body = for_body_test)

    test_function_definition('print_dict', body = fun_body_test)
    ```

Assuming the student coded the function in the exact same way as the solution, the following things happen:

- `test_function_definition()` is run first: it checks whether `print_dict` is defined, whether the arguments are correctly named and with the correct defaults. Next, it checks the function definition body: it extracts the body of both the student and the solution code, sets the context values for this 'substate', i.e. `"my_dict"`, and then runs `fun_body_test()`.
- Inside `fun_body_test()`, `test_for_loop()` is executed. This function will find the for loop in the function definition body of both student and solution code, and will then run different tests:
    - First, the `for_iter` test is run, which is specified with `for_iter_test()` in this SCT. The `for_iter` part of the `for` loop is extracted, which is `my_dict.items()` in the case of the solution. The context values are still `"my_dict"`. Inside `test_expression_result()`, the context vals are specified, so through `context_vals = [example_dict]`, the variable `my_dict` will now have the value `{'a': 2, 'b':3}` inside the student and solution processes. Next, the currently active expression (`my_dict.items()`) is executed. The result of calling this expression in both student and solution process is compared.
    - Second, the `body` test is run, which is specified iwth `for_body_test()` in this SCT. The `body` part of the `for` loop is extracted, which is `print(key + " - " + str(value))` in the case of the solution. Now, the context values are set to the iterator variables of the `for` loop, so `"key"` and `"value"`. Inside `test_expression_output()`, the context vals are specified: `key` is set to be `'c'`, `value` is set to be `3`. Next, the currently active expression (`print(key + " - " + str(value))`) is executed, and the output it generates is fetched. The output of calling this expression in both student and solution process is compared.

### Example 2

Suppose now that inside the `for` loop of `print_dict()` from the previous example, you each time want to print out the length of the entire dictionary:

    *** =solution
    ```{python}
    def print_dict(my_dict):
        for key, value in my_dict.items():
            print("total length: " + str(len(my_dict)))
            print(key + " - " + str(value))
    ```

The SCT from before won't work out of the box, because now you also need a value for `my_dict` inside `test_expression_output()`, the test of the body of the `for` loop, but this value is not available. You cannot specify this value through `context_vals`, because the context variables are already updated to be `"key"` and `"value"`. To be able to test this appropriately, you'll have to set `extra_env` inside `test_expression_output()`:

    *** =sct
    ```{python}
    def fun_body_test():
        def for_iter_test():
            example_dict = {'a': 2, 'b': 3}
            test_expression_result(context_vals = [example_dict])
        def for_body_test():
            example_dict = {'a': 2, 'b': 3}
            test_expression_output(context_vals = ['c', 3], extra_env = {'my_dict': example_dict})

        test_for_loop(for_iter = for_iter_test, body = for_body_test)

    test_function_definition('print_dict', body = fun_body_test)
    ```

With this update of the SCT, the exercise will still run fine.

