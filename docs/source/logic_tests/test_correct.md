test_correct
------------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_correct
    :members:
```

A wrapper function around `test_or()`, `test_correct()` allows you to add logic to your SCT. Normally, your SCT is simply a script with subsequent `pythonwhat` function calls, all of which have to pass. `test_correct()` allows you to bypass this: you can specify a "sub-SCT" in the `check` part, that should pass. If these tests pass, the "sub-SCT" in `diagnose` is not executed. If the tests don't pass, the "sub-SCT" in `diagnose` is run, typically to dive deeper into what the error might be and give more specific feedback.

To accomplish this, the SCT in `check` is executed silently, so that failure will not cause the SCT to stop and generate a feedback message. If the execution passes, all is good and `test_correct()` is abandoned. If it fails, `diagnose` is executed, not silently. If the `diagnose` part fails, the feedback message that it generates is presented to the student. If it passes, the `check` part is executed again, this time not silently, to make sure that a `test_correct()` that contains a failing `check` part leads to a failing SCT.

### Example 1

As an example, suppose you want the student to calculate the mean of a Numpy array `arr` and store it in `res`. A possible solution could be:

    *** =solution
    ```{python}
    # Import numpy and create array
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5, 6])

    # Calculate result
    result = np.mean(arr)
    ```

You want the SCT to pass when the student manages to store the correct value in the object `result`. How `result` was calculated, does not matter to you: as long as `result` is correct, the SCT should accept the submission. If something about `result` is not correct, you want to dig a little deeper and see if the student used the `np.mean()` function correctly. The following SCT will do just that:

    *** =sct
    ```{python}
    test_correct(test_object('result'),
                 test_function('numpy.mean'))
    success_msg("You own numpy!")
    ```

Let's go over what happens when the student submits different pieces of code:

- The student submits `result = np.mean(arr)`, exactly the same as the solution. 
  `test_correct()` runs `test_object('result')`. 
  This test passes, so `test_correct()` stops. 
  The SCT passes.
- The student submits `result = np.sum(arr) / arr.size`, which also leads to the correct value in `result`.
  `test_correct()` runs `test_object('result')`.
  This test passes, so `test_correct()` stops before running `test_function()`.
  The entire SCT passes even though `np.mean()` was not used.
- The student submits `result = np.mean(arr + 1)`.
  `test_correct()` runs `test_object('result')`.
  This test fails, so `test_correct()` continues with 'diagnose', running `test_function('numpy.mean')`.
  This function fails, since the argument passed to `numpy.mean()` in the student submission does not correspond to the argument passed in the solution.
  A meaningful, specific feedback message is presented to the student: you did not correctly specify the arguments inside `np.mean()`.
- The student submits `result = np.mean(arr) + 1`.
  `test_correct()` runs `test_object('result')`.
  This test fails, so `test_correct()` continues with'diagnose', running `test_function('numpy.mean').
  This function passes, because `np.mean()` is called in exactly the same way in the student code as in the solution.
  Because there is something wrong - `result` is not correct - the 'check' SCT, `test_object('result')` is executed again, and this time its feedback on failure is presented to the student.
  The student gets the message that `result` does not contain the correct value.


### Multiple functions in `diagnose` and `check`

You can also use `test_correct()` with entire 'sub-SCTs' that are composed of several SCT calls. In this case, you may put multiple tests inside `multi()`, as below..

    *** =sct
    ```{python}
    Ex().test_correct(
            multi(test_object('a'), test_object('b')),   # multiple check SCTs
            test_function('numpy.mean')
            )
    ```

### Why to use `test_correct()`

You will find that `test_correct()` is an extremely powerful function to allow for different ways of solving the same problem. You can use `test_correct()` to check the end result of a calculation. If the end result is correct, you can go ahead and accept the entire exercise. If the end result is incorrect, you can use the `diagnose` part of `test_correct()` to dig a little deeper.

It is also perfectly possible to use `test_correct()` inside another `test_correct()`.

### Wrapper around `test_or()`

`test_correct()` is a wrapper around `test_or()`. `test_correct(diagnose, check)` is equivalent with:

    def diagnose_and_check()
        diagnose()
        check()

    test_or(diagnose_and_check, check)

Note that in each of the `test_or` cases here, the submission has to pass the SCTs specified in `check`.
