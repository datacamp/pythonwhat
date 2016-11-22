Composite SCTs
==============

Several functions, such as `test_correct()`, `test_or()`, `test_function_definition()`, among others, also have arguments that expect another set of tests. This article will explain the different ways of specifying these 'sub-tests'.

Let's take the example of `test_correct()`; this function takes two sets of tests. The first set is executed, and if it's fine, the second set is left alone. If the first set of tests results in an error, the second set is executed and the feedback is logged.

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

The first part of the tests here would be to check `result`. If `result` is not correct, you want to check whether `np.mean()` has been called.

The most concise way to do this, is with lambda functions; you specify two sets of tests, that in this case consist of one test each:

    *** =sct
    ```{python}
    test_correct(lambda: test_object('result'),
                 lambda: test_function('numpy.mean'))
    success_msg("You own numpy!")
    ```

Another way to do this, is by specifying two separate function definitions, e.g. `check` and `diagnose`, and pass these function definitions to `test_correct()`, as shown below. Notice that you have to pass the actual function definition, so `check` and `diagnose` without parentheses:

    *** =sct
    ```{python}
    def check():
        test_object('result')

    def diagnose():
        test_function('numpy.mean')

    test_correct(check, diagnose)
    success_msg("You own numpy!")
    ```

Of course, you can also use a lambda function for one test set, and a function definition for the other:

    *** =sct
    ```{python}
    def check():
        test_object('result')

    test_correct(check,
                 lambda: test_function('numpy.mean'))
    success_msg("You own numpy!")
    ```


### Example 2

When writing SCTs for more complicated exercises, you'll probably want to pass along several tests to an argument.

Suppose that you expect the student to create an object `result` once more, but this time it's the sum of calling the `np.mean()` function twice; once on `arr1`, once on `arr2`:

    *** =solution
    ```{python}
    # Import numpy and create array
    import numpy as np
    arr1 = np.array([1, 2, 3, 4, 5, 6])
    arr2 = np.array([6, 5, 4, 3, 2, 1])

    # Calculate result
    result = np.mean(arr) + np.mean(arr)
    ```

Now, in the 'digging deeper' part of `test_correct()`, you want to check the `np.mean()` function twice. To do this, you'll want to use a function definition; lambda functions are not practical anymore:

    *** =sct
    ```{python}
    def diagnose():
        test_function('numpy.mean', index = 1)
        test_function('numpy.mean', index = 2)

    test_correct(lambda: test_object('result'),
                 diagnose)
    success_msg("You own numpy!")
    ```

### Example 3: custom feedback

To pass custom feedback feedback messages to these sub-SCTs, you should define the custom message inside the functions themselves, inside the function definition, or define it beforehand and pass it along as a default argument. Let's revisit the first example:

    *** =solution
    ```{python}
    # Import numpy and create array
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5, 6])

    # Calculate result
    result = np.mean(arr)
    ```

Here are the three different SCT options, this time with custom feedback:

    *** =sct
    ```{python}
    # OPTION 1
    msg1 = "Are you sure `result` is correct?"
    msg2 = "Your call of `np.mean()` isn't right."
    test_correct(lambda msg=msg1: test_object('result', incorrect_msg = msg),
                 lambda msg=msg2: test_function('numpy.mean', incorrect_msg = msg))
    success_msg("You own numpy!")

    # OPTION 2
    def check():
        test_object('result', incorrect_msg = "Are you sure `result` is correct?")

    def diagnose():
        test_function('numpy.mean', incorrect_msg = "Your call of `np.mean()` isn't right.")

    test_correct(check, diagnose)
    success_msg("You own numpy!")


    # OPTION 3
    def check():
        test_object('result', incorrect_msg = "Are you sure `result` is correct?")

    test_correct(check,
                 lambda: test_function('numpy.mean', incorrect_msg = "Your call of `np.mean()` isn't right."))
    success_msg("You own numpy!")
    ```
