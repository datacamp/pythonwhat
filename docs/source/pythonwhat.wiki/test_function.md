test_function
-------------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_function.test_function
```

    test_function(name,
                  index=1,
                  args=None,
                  keywords=None,
                  eq_condition="equal",
                  do_eval=True,
                  not_called_msg=None,
                  incorrect_msg=None)

`test_function()` enables you to test whether the student called a function correctly. The function first tests if the specified function is actually called by the student, and then compares the call with calls of the function in the solution code. Next, it can compare the parameters passed to these functions. Because `test_function()` also uses the student and solution process, this can be done in a very concise way.

### Example 1

Suppose you want the student to call the `round()` function on pi, as follows:

    *** =solution
    ```{python}
    # This is pi
    pi = 3.14159

    # Round pi to 3 digits
    r_pi = round(pi, 3)
    ```

The following SCT tests whether the `round()` function is used correctly:

    *** =sct
    ```{python}
    test_function("round")
    success_msg("Great job!")
    ```

This is a very robust way to test whether `round()` is used, much more robust when comparing to `test_student_typed()`. `test_function()` tests whether the student has called the function `round()` and checks whether the values of the arguments are the same as in the solution. So in this case, it tests wether `round()` is used with its first argument equal to `3.14159` and the second argument equal to `3`. `test_function()` figures out the values of these arguments from the solution code and the solution processes that corresponds with it. The above SCT would accept all of the following student submissions:

- `round(3.14159, 3)`
- `pi = 3.14159; dig = 3; round(pi, dig)`
- `int_part = 3; dec_part = 0.14159; round(int_part + dec_part, 3)`

By default, `test_function()` tests all arguments that are specified in the solution code. It is also possible to check whether a function is used and only check specific positional arguments. For example,

    *** =sct
    ```{python}
    test_function("round", args=[0])
    success_msg("Great job!")
    ```

will only test whether the first argument's value is `3.14159`. A student submission that is `round(pi, 5)` would also pass this SCT.

With `args`, you can also control whether or not to actually check the values that were passed as parameters. Say you only want to check that the function `round()` was called:

    *** =sct
    ```{python}
    test_function("round", args=[])
    success_msg("Great job!")
    ```


`test_function()` will automatically generate meaningful feedback, but you can also override these messages with `not_called_msg` and `incorrect_msg`. The former controls the message that is thrown if the student didn't call the specified function in the first place. The latter is thrown if the student did not correctly set the arguments in the function call:

    *** =sct
    ```{python}
    test_function("round",
                  not_called_msg = "You did not call `round()` to round the irrational number, `pi`.",
                  incorrect_msg = "Be sure to round `pi` to `3` digits.`)
    success_msg("Great job!")
    ```



### Example 2: Multiple function calls

`index`, which is 1 by default, becomes important when there are several calls of the same function. Suppose that your exercise requires the student to call the `round()` function twice: once on `pi` and once on `e`, Euler's number. A possible solution could be the following:

    *** =solution
    ```{python}
    # Call round on pi
    round(3.14159, 3)

    # Call round on e
    round(2.71828, 3)
    ```

To test both these function calls, you'll need the following SCT:

    *** =sct
    ```{python}
    test_function("round", index=1)
    test_function("round", index=2)
    success_msg("Two in a row, great!")
    ```

The first `test_function()` call, where `index=1`, checks the solution code for the first function call of `round()`, finds it - `round(3.14159, 3)` - and then goes to look through the student code to find a function call of `round()` that matches the arguments. It is perfectly possible that there are 5 function calls of `round()` in the student's submission, and that only the fourth call matches the requirements for `test_function()`. As soon as a function call is found in the student code that passes all tests, `pythonwhat` heads over to the second `test_function()` call, where `index=2`. The same thing happens: the second call of `round()` is found from the solution code, and a match is sought for in the student code. This time, however, the function call that was matched before is now 'blacklisted'; it is not possible that the same function call in the student code causes both `test_function()` calls to pass.

This means that all of the following student submissions would be accepted:

  - `round(3.14159, 3); round(2.71828, 3)`
  - `round(2.71828, 3); round(3.14159, 3)`
  - `round(3.14159, 3); round(123.456); round(2.71828, 3)`
  - `round(2.71828, 3); round(123.456); round(3.14159, 3)`

Of course, you can also specify all other arguments to customize your test, such as `do_eval`, `args`, `not_called_msg` and `incorrect_msg`.

### Example 3: Custom feedback

By default `test_function()` checks all arguments and keywords that are specified in the solution; if you specify `incorrect_msg`, any error to one of these arguments will replaced by the same custom message. If you want to provide different custom error messages for different arguments, you can do so with multiple function calls. To, for example, provide different feedback for the first and second argument of the `round()` function:

    *** =sct
    ```{python}
    test_function("round", args = [0], index=1, incorrect_msg = 'first arg wrong!')
    test_function("round", args = [1], index=1, incorrect_msg = 'second arg wrong!')
    success_msg("Well done")
    ```

**NOTE**: currently, `test_function()` automatically checks all arguments and keywords that you specify in corresponding function call in the solution. Therefore, if you want to give specific feedback, make sure to select a single argument or a single keyword. To check the first argument, you can best use `args = [0], keywords = []`, to test a keyword named `check`, you'll want to use `args = [], keywords = ['check']`.

### Example 4: Methods

Python also features methods, i.e. functions that are called on objects. For testing such a thing, you can also use `test_function()`. Consider the following solution code, that creates a connection to an SQLite Database with `sqlalchemy`.

    *** =solution
    ```{python}
    from urllib.request import urlretrieve
    from sqlalchemy import create_engine, MetaData, Table
    engine = create_engine('sqlite:///census.sqlite')
    metadata = MetaData()
    connection = engine.connect()
    from sqlalchemy import select
    census = Table('census', metadata, autoload=True, autoload_with=engine)
    stmt = select([census])

    # execute the query and fetch the results.
    connection.execute(stmt).fetchall()
    ```

To test the last chained method calls, you can use the following SCT. Notice from the second `test_function()` call here that you have to describe the entire chain (leaving out the arguments that are passed to `execute()`). This way, you explicitly list the order in which the methods should be called.

    *** =sct
    ```
    test_function("connection.execute", do_eval = False)
    test_function("connection.execute.fetchall")
    ```

**NOTE**: currently, it is not possible to easily test the arguments inside chained method calls, methods inside arguments, etc. We are working on a massive update of `pythonwhat` to easily support this very customized testing, with virtually no limit to 'how deep you want the tests to go'. More on this later!

### `do_eval`

With `do_eval`, you can control how arguments are compared between student and solution code.

- If `do_eval` is `True`, the evaluated version of the arguments are compared;
- If `do_eval` is `False`, the 'string version' of the argumetns are compared;
- If `do_eval` is `None`, the arguments are not compared; in this case, `test_function()` simply checks if you specified the arguments, without further checks.


### Function calls in packages

If you're testing whether function calls of particular packages are used correctly, you should always refer to these functions with their 'full name'. Suppose you want to test whether the function `show` of `matplotlib.pyplot` was used correctly, you should use

    *** =sct
    ```{python}
    test_function("matplotlib.pyplot.show")
    ```

The `test_function()` call can handle it when a student used aliases for the python packages (all `import` and `import * from *` calls are supported). In case there is an error, `test_function()` will automatically generated a feedback message that uses the alias of the student.

**NOTE:** No matter how you import the function, you always have to refer to the function with its full name, e.g. `package.subpackage1.subpackage2.function`.

### Argument equality

Just like with `test_object()`, evaluated arguments are compared using the `==` operator (check out [the section about Object equality](https://github.com/datacamp/pythonwhat/wiki/test_object#object-equality)). For a lot of complex objects, the implementation of `==` causes the object instances to be compared... not their underlying meaning. For example when the solution is:

    *** =solution
    from urllib.request import urlretrieve
    fn1 = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite'
    urlretrieve(fn1, 'Chinook.sqlite')

    # Import packages
    from sqlalchemy import create_engine
    import pandas as pd

    # Create engine: engine
    engine = create_engine('sqlite:///Chinook.sqlite')

    # Execute query and store records in dataframe: df
    df = pd.read_sql_query("SELECT * FROM Album", engine)

And the SCT is:

    *** =sct
    test_function("pandas.read_sql_query")

The SCT will fail even if the student uses this exact solution code. The reason being that the `engine` object is compared in the solution and student process. The engine object is evaluated by `create_engine('sqlite:///Chinook.sqlite')`. As you can try out yourself, `create_engine('sqlite:///Chinook.sqlite') == create_engine('sqlite:///Chinook.sqlite')` will always be `False`, even though they are semantically exactly the same. A better way of testing this code would be:

    *** =sct
    test_correct(
        lambda: test_object("df"),
        lambda: test_function("pandas.read_sql_query", do_eval=False)
    )

This SCT will not do exactly the same, but it will test enough in practice 99% of the time. Check out [the section about Object equality](https://github.com/datacamp/pythonwhat/wiki/test_object#object-equality) for complex objects that do have a good equality implementation.

**NOTE**: Behind the scenes, `pythonwhat` has to fetch the value of objects from sub-processes. The required 'dilling' and 'undilling' can cause issues for exotic objects. For more information on this and possible errors that can occur, read the [Processes article](https://github.com/datacamp/pythonwhat/wiki/Processes).
