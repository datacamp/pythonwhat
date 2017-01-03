test_student_typed
------------------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_student_typed
    :members:
```

    test_student_typed(text,
                       pattern=True,
                       not_typed_msg=None)

`test_student_typed()` will look through the student's submission to find a match with the string specified in `text`. With `pattern`, you can declare whether or not to use regular expressions.

Suppose the solution of an exercise looks like this:

    *** =solution
    ```{python}
    # Calculate the sum of all single digit numbers and assign the result to 's'
    s = sum(range(10))

    # Print the result to the shell
    print(s)
    ```

The following SCT tests whether the student typed `"sum(range("`:

    *** =sct
    ```{python}
    test_student_typed("sum(range(", pattern = False)
    success_msg("Great job!")
    ```

Notice that we set `pattern` to `False`, this will cause `test_student_typed()` to search for the pure string, no patterns are used. This SCT is not that robust though, it won't accept something like `sum(  range(10) )`. This is why we should almost always use [regular expressions](https://docs.python.org/3.5/library/re.html) in `test_student_typed`. For example:

    *** =sct
    ```{python}
    test_student_typed("sum\s*\(\s*range\s*\(", not_typed_msg="You didn't use `range()` inside `sum()`.")
    success_msg("Great job!")
    ```

We also used `not_typed_msg` here, which will control the feedback given to the student when `test_student_typed()` doesn't pass. Note that also `success_msg()` is used here, this is the message that is shown when the SCT has passed.

In general, **you should avoid using `test_student_typed()`**, as it imposes severe restrictions on how a student can solve an exercise. Often, there are different ways to solve an exercise. Unless you have a very advanced regular expression, `test_student_typed()` will not be able to accept all these different approaches. For the example above, `test_function()` would be more appropriate.
