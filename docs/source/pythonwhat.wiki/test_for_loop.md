test_for_loop
-------------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_for_loop
    :members:
```


    test_for_loop(index=1,
                  for_iter=None,
                  body=None,
                  orelse=None,
                  expand_message=True)

As the name suggesets, you can use `test_for_loop()` to test if a for loop was properly coded. Similar to how `test_if_else()` and `test_while_loop()` works, `test_for_loop()` parses the for loop in the student's submission and breaks it up into its composing parts. Next, it also parses the for loop in the solution solution, and compares the parts between student submission and solution. It does this through sub-SCTs that you specify in `cond_test` and `expr_test`.

### Example 1

Suppose you want the student to implement an algorithm that calculates fibonacci's row (until `n = 20`) using a simple for loop. The solution could look like this:

    *** =solution
    ```{python}
    # Initialise the row
    fib = [0, 1]

    # Update the row correctly each loop
    for n in range(2, 20):
        fib.append(fib[n-2] + fib[n-1])
    ```

An SCT to accompany this exercise could be the following:

    *** =sct
    ```{python}
    def test_for_iter():
        "You have to iterate over `range(2, 20)`"
        test_function("range",
                      not_called_msg=msg,
                      incorrect_msg=msg)

    def test_for_body():
        msg = "Make sure your row, `fib`, updates correctly"
        test_object_after_expression("fib",
                                     extra_env={ "fib": [0, 1, 1, 2] },
                                     context_vals=[4],
                                     undefined_msg=msg,
                                     incorrect_msg=msg)
    test_for_loop(index=1,
                  for_iter=test_for_iter,
                  body=test_for_body)
    ```


Notice that two self-defined functions, `test_for_iter()` and `test_for_body()` are used to specify the sub-SCTs for the different parts in the `for` loop. With `index = 1`, you tell `pythonwhat` that you want to check the first `for` loop you find in the student submission with the first `for` loop in the solution.


The `for_iter` part of `test_for_loop()` tests whether the loop with index 1 loops over the correct range. The tests in this sub-SCT are run on the sequence part of the loop, which in this case for the solution is `range(2, 20)`. With `test_function()`, we can test this. In other cases, you could use e.g. `test_expression_result()`, to test the result of the sequence part.

The `body` part of `test_for_loop()` tests whether `fib` is updated correctly. The tests in this sub-SCT are run on the body of the loop. The `test_object_after_expression()`. This function will test an object after the active expression is run in the student and solution process. In this case it will check if `fib` is updated the same in the student and solution process after one loop through the body of the `for`. Two important arguments for `test_object_after_expression()` are:

- `extra_env = { "fib": [0, 1, 1, 2] }`: when running the body of the for loop, the process will be updated with these extra environment variables. In this case this means that before the body is ran, `fib` will be initialised to `[0, 1, 1, 2]`.
- `context_vals = [4]`: this argument contains the values of the loop's variable. In the solution code, for example, there will be one: `n`. This means that `n` will be initialised to `4` in the solution process when the body of the for loop is run. The student can give any name to `n`, as long as the functionality remains the same.

You may have noticed that the helper functions that are used within `test_for_loop()` contain feedback messages as well. When they are used within a `test_for_loop()`, these messages will automatically be extended with "in the ___ of the for loop on line ___.". To avoid this extension, you could set the option `expand_message = False` in `test_for_loop()`.

Example 2: Multiple context vals

If you have multiple context vals, things largely work the same way. Suppose you want somebody to print out the keys and values of a dictionary as follows:

    *** =solution
    ```{python}
    my_dict = {'a': 1, 'b': 2, 'c': 3}
    for k, v in my_dict.items():
        print(k + ' - ' + str(v))
    ```

An appropriate SCT would be:

    *** =sct
    ```{python}
    test_object('my_dict')
    test_for_loop(index=1,
                  for_iter = lambda: test_expression_result(),
                  body = lambda: test_expression_output(context_vals = ['a', 1]))
    ```

In this case, when you're checking the output of the body of the `for` loop, you're telling `k` to be `'a'` and `v` to be `1`.
