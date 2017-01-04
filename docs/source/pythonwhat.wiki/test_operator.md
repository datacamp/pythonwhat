test_operator
-------------

**THIS FUNCTION IS DEPRECATED AND WILL BE REMOVED IN A FUTURE RELEASE**

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_operator
    :members:

```

    def test_operator(index=1,
                      eq_condition="equal",
                      used=None,
                      do_eval=True,
                      not_found_msg=None,
                      incorrect_op_msg=None,
                      incorrect_result_msg=None)

Suppose you want the student to do some very basic operations using the `*` and the `**` operator. You could just ask the student to do some calculations and assign the result to a variable, `result` for example, and check that variable using `test_object()`. However this won't allow you to give the student very tailored feedback. Suppose you want to check if the student uses `**` and tell him/her if he/she doesn't! `test_object()` won't allow you to check this kind of specifics as it only checks resulting objects in both processes. Luckily, you can use another helper function, `test_operator()`.

Say you want the student to calculate the future value of \$100 after 6 years. The interest rate 6% and you are using compound interest. This means the result has to be `100 * 1.06 ** 6`, so the solution code would be.

    *** =solution
    ```{python}
    # Calculate the future value of 100 dollar: result
    result = 100 * 1.06 ** 6

    # Print out the result
    print(result)
    ```

The SCT might look something like this,

    *** =sct
    ```{python}
    test_operator(index=1)
    test_object("result")
    test_function("print")
    success_msg("Great!")
    ```

You can learn about `test_object()` and `test_function()` in the other articles, so those won't be deatiled here. Let's focus on `test_operator()` instead. This function will extract the first operator group from the solution code (`100 * 1.06 ** 6`), run it in the solution process, and compare the result with the result from running the first operator in the student code in the student process. In total, three steps will be tested:

- Did the student define enough operations?
- Does the student use the same operators as the solution?
- Is the result of the operation for the student the same as the one in the solution?

`test_operator()` takes some additional arguments for further customization and tailored feedback messages. For example, you can use it as follows to just check whether the student used the `**` operator in his/her first operation and give custom feedback:

    *** =sct
    ```{python}
    test_operator(index=1, used=["**"], do_eval=False,
                  incorrect_op_msg="A little tip: you should use `**` to do this calculation.")
    test_object("result")
    test_function("print")
    success_msg("Great!")
    ```

This SCT will be more forgiving, but the result is still checked with `test_object()` so the student will still have to calculate the correct value. This time, however, it is not checked by `test_operator()` because `do_eval = False`. `used = ["**"]` is used to tell the system to only check on the `**` operator for the first operation group.

**NOTE**: Behind the scenes, `pythonwhat` has to fetch the value of objects from sub-processes. The required 'dilling' and 'undilling' can cause issues for exotic objects. For more information on this and possible errors that can occur, read the [Processes article](../expression_tests.md).
