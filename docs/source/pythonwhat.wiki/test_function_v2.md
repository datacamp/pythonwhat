test_function_v2
----------------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_function.test_function_v2
```

    test_function_v2(name,
                  index=1,
                  params=None,
                  signature=None,
                  eq_condition="equal",
                  do_eval=True,
                  not_called_msg=None,
                  params_not_matched_msg=None,
                  params_not_specified_msg=None,
                  incorrect_msg=None)

`test_function_v2()` enables you to test whether the student called a function correctly. The function first tests if the specified function is actually called by the student, and then compares the call with calls of the function in the solution code. Next, it can compare the arguments passed to these functions. Because `test_function_v2()` also uses the student and solution process, this can be done in a very concise way. `test_function_v2()` is an improved version of [`test_function()`](test_function.md), where:

- there is resilience against different ways of calling a function (arguments vs keywords),
- you have to be specific about which parameters you want to check,
- you can specify parameter-specific evaluation forms (`do_eval` can be a list),
- you can specify parameter-specific custom messages (`params_not_matched_msg` and `params_not_specified_msg` can be lists),
- you have more control over messaging in general.

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
    test_function_v2("round", params=["number", "ndigits"])
    success_msg("Great job!")
    ```

`test_function_v2()` tests whether the student has called the function `round()` and checks whether the values of the arguments are the same as in the solution. So in this case, it tests whether `round()` is used and the `number` and `ndigits` parameters, that `round()` expects, are specified correctly, i.e. equal to `3.14159` and `3` respectively. `test_function_v2()` figures out the values of these arguments from the solution code and the solution process that corresponds with it. The above SCT would accept all of the following student submissions:

- `round(3.14159, 3)`
- `round(number=3.14159, 3)`
- `round(number=3.14159, ndigits=3)`
- `round(ndigits=3, number=3.14159)`
- `pi=3.14159; dig=3; round(pi, dig)`
- `pi=3.14159; dig=3; round(number=pi, dig)`
- `int_part = 3; dec_part = 0.14159; round(int_part + dec_part, 3)`

In `params`, you have to explicitly list all the parameters that you want to test. If you only want to check the `number` parameter, for example, you can use:

    *** =sct
    ```{python}
    test_function_v2("round", params=["number"])
    success_msg("Great job!")
    ```

This SCT will only test whether the `number` parameter was specified to be `3.14159`. If a student submits `round(pi, 5)`, this would also pass this SCT.

If you specify `params` to be an empty list, which is the default, you are simply checking whether the `round()` function was called in the first place:

    *** =sct
    ```{python}
    test_function_v2("round") # same as test_function_v2("round", params=[])
    success_msg("Great job!")
    ```

`test_function_v2()` will automatically generate meaningful feedback, but you can also override these messages through the different `*_msg` parameters that `test_function_v2()` features:

- `not_called_msg`: message if the student didn't call the specified function or didn't call the specified function often enough (if you're testing multiple calls of the same function in the same submission).
- `params_not_matched_msg`: message if the function call of the student was invalid, i.e. if the way of specifying the different parameters was invalid.
- `params_not_specified_msg`: message if the student did not specify all parameters that are specified inside `params`. This argument can either be a string, to give the same message for each parameter that is missing, or a list of strings with the same length as `params`. In case of a missing parameter, `test_function_v2()` will present the corresponding message.
- `incorrect_msg`: message if the student did not specify all parameters correctly, so when his or her specifications don't correspond with the solution. This argument can again be a single string, or a list of parameter-specific feedback messages.

Below is an example of an SCT that specified all feedback messages. This is not required, though; you can depend on the automatic feedback messages for the `not_called_msg`, `params_not_specified_msg` and `incorrect_msg` and only manually specify the `params_not_matched_msg`, for example.

    *** =sct
    ```{python}
    test_function_v2("round", params=["number", "ndigits"]
                     not_called_msg="You did not call `round()` to round the irrational number, `pi`.",
                     params_not_matched_msg="Are you sure you correctly called the `round()` function?",
                     params_not_specified_msg="Make sure to specify both the `number` and `ndigits` parameter!",
                     incorrect_msg=["Make sure to correctly specify `number`; it should be `pi`, or `3.14159`.",
                                    "Have you specified `ndigits` so that `pi` is rounded to 3 digits?"])
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
    test_function_v2("round", params=["number","ndigits"], index=1)
    test_function_v2("round", params=["number","ndigits"], index=2)
    success_msg("Two in a row, great!")
    ```

The first `test_function_v2()` call, where `index=1`, checks the solution code for the first function call of `round()`, finds it - `round(3.14159, 3)` - and then goes to look through the student code to find a function call of `round()` that matches the arguments. It is perfectly possible that there are 5 function calls of `round()` in the student's submission, and that only the fourth call matches the requirements for `test_function_v2()`. As soon as a function call is found in the student code that passes all tests, `pythonwhat` heads over to the second `test_function_v2()` call, where `index=2`. The same thing happens: the second call of `round()` is found from the solution code, and a match is sought for in the student code. This time, however, the function call that was matched before is now 'blacklisted'; it is not possible that the same function call in the student code causes both `test_function_v2()` calls to pass.

This means that all of the following student submissions would be accepted:

  - `round(3.14159, 3); round(2.71828, 3)`
  - `round(2.71828, 3); round(3.14159, 3)`
  - `round(number=3.14159, ndigts=3); round(number=2.71828, 3)`
  - `round(number=2.71828, 3); round(number=3.14159, 3)`
  - `round(3.14159, 3); round(123.456); round(2.71828, 3)`
  - `round(2.71828, 3); round(123.456); round(3.14159, 3)`

Of course, you can also specify all other arguments to customize your test to perfection, such as custom messages and `do_eval` (example 3).

### Example 3: `do_eval`

With `do_eval`, you can control how parameter specifications are compared between student and solution code. There are two ways to specify `do_eval`: you can specify a single value, that will be used for comparing all `params` that you specified. However, you can also specify a list of values, with the same length as `params`; the way in which parameter specifications are compared becomes parameter specific. In both cases, there are three valid values:

- `True`, where the evaluated version of the student and solution arguments is compared.
- `False`, where the 'string version' of the arguments is compared;
- `None`, in which case the arguments are not compared; `test_function_v2` simply checks if the parameter(s) in question has/have been specified.

Say, for example, you want to check if a student called the `round()` function and specified the parameters `number` and `ndigits`. You want to test the actual equality of `number`, but you don't care about the value of `ndigits`, you just want to make sure the student specified it, nothing more.

The following solution and SCT implement this train of thought (custom feedback messages have not been specified, although this is perfectly possible):

    *** =solution
    ```{python}
    # This is pi
    pi = 3.14159

    # Round pi to 3 digits
    r_pi = round(pi, 3)
    ```

    *** =sct
    ```{python}
    test_function_v2("round",
                     params=["number", "ndigits"],
                     do_eval=[True, None])
    success_msg("Great job!")
    ```

All of the following submissions would be accepted by this SCT:

- `round(pi, 3)`
- `round(number=pi, ndigits=3)`
- `round(number=pi, ndigits=4)`
- `round(pi, 4)`
- `round(pi, 0)`

### Example 4: Function calls in packages

If you're testing whether function calls of particular packages are used correctly, you should always refer to these functions with their 'full name'. Suppose you want to test whether the function `show` of `matplotlib.pyplot` was used correctly, you should use

    *** =sct
    ```{python}
    test_function_v2("matplotlib.pyplot.show")
    ```

The `test_function_v2()` call can handle it when a student used aliases for the python packages (all `import` and `import * from *` calls are supported). In case there is an error, `test_function_v2()` will automatically generated a feedback message that uses the alias that the student used.

**NOTE:** No matter how you import the function, you always have to refer to the function with its full name, e.g. `package.subpackage1.subpackage2.function`.

### Example 5: Manual signatures

To implement resilience against different ways of specify function parameters, the `inspect` module is used, that is part of Python's basic distribution. Through `inspect.signature()` a function's parameters can be inferred, and then 'bound' to the arguments that the student specified. However, this signature is not available for all of Python's functions. More specifically, Python's built-in functions that are implemented in C don't allow a signature to be extracted from them. `pythonwhat` already includes manually specified signatures for functions such as `print()`, `str()`, `hasattr()`, etc, but it's still possible that some signatures are missing.

That's why `test_function_v2()` features a `signature` parameter, that is `None` by default. If `pythonwhat` can't retrieve a signature for the function you want to test, you can pass an object of the class `inspect.Signature` to the `signature` parameter.

Suppose, for the sake of example, that `test_function_v2()` can't find a signature for the `round()` function (you will be informed by this through automated testing; running the solution against an SCT that depends on a signature that is not found will throw a backend error). To be able to implement this function test, you can use the `sig_from_params()` function:

    *** =sct
    ```{python}
    sig = sig_from_params(param("number", param.POSITIONAL_OR_KEYWORD),
                          param("ndigits", param.POSITIONAL_OR_KEYWORD, default=0))
    test_function_v2("round", params=["number", "ndigits"], signature=sig)
    ```

`param` is an alias of the `Parameter` class that's inside the `inspect` module. You can pass `sig_from_params()` as many parameters as you want. The first argument of `param()` should be the name of the parameter, the second argument should be the 'kind' of parameter. `param.POSITIONAL_OR_KEYWORD` tells `test_function_v2` that the parameter can be specified either through a positional argument or through a keyword argument. Other common possibilities are `param.POSITIONAL_ONLY` and `param.KEYWORD_ONLY` (for a full list, refer to the [Python docs on `inspect`](https://docs.python.org/3.4/library/inspect.html#inspect.Parameter)). The third, optional argument, allows you to specify a default value for the parameter.

**NOTE:** If you find vital Python functions that are used very often and that are not included in `pythonwhat` by default, you can [let us know](mailto:content-engineering@datacamp.com) and we'll add the function to our [list of manual signatures](https://github.com/datacamp/pythonwhat/blob/master/pythonwhat/signatures.py).

### Example 6: Methods

Python also features methods, i.e. functions that are called on objects. For testing such a thing, you can also use `test_function_v2()`. Consider the following solution code, that creates a connection to an SQLite Database with `sqlalchemy`.

    *** =solution
    ```{python}
    # Prepare everything
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

To test the last chained method calls, you can use the following SCT. Notice from the second `test_function_v2()` call here that you have to describe the entire chain (leaving out the arguments that are passed to `execute()`). This way, you explicitly list the order in which the methods should be called.

    *** =sct
    ```{python}
    test_function_v2("connection.execute", params = ["object"], do_eval = False)
    test_function_v2("connection.execute.fetchall")
    ```

**NOTE**: currently, it is not possible to easily test the arguments inside chained method calls, methods inside arguments, etc. We are working on a massive update of `pythonwhat` to easily support this very customized testing, with virtually no limit to 'how deep you want the tests to go'. More on this later!

### Example 7: Signatures for methods

In the previous example, you might have noticed that `test_funtion_v2()` was capable to infer that `connection` is a `Connection` object, and that `execute()` is a method of the `Connection` class. For checking method calls that aren't chained, this is possible, but for chained method calls, such as `connection.execute.fetchall`, this is not possible. In those cases you'll have to manually specify a signature. With `sig_from_obj()` you can specify the function from which to extract a signature.

The following full example shows how it's done:

    *** =pre_exercise_code
    ```{python}
    class Test():
        def __init__(self, a):
            self.a = a

        def set_a(self, value):
            self.a = value
            return(self)
    x = Test(123)
    ```

    *** =solution
    ```{python}
    x.set_a(843).set_a(102)
    ```

    *** =sct
    ```{python}
    sig = sig_from_obj('x.set_a')
    test_function_v2('x.set_a.set_a', params=['value'], signature=sig)
    ```

**NOTE**: You can also use the `sig_from_params()` function to manually build the signature from scratch, but this this more work than simply specifying the function object as a string from which to extract the signature.


### Extra: Argument equality

Just like with `test_object()`, evaluated arguments are compared using the `==` operator (check out [the section about Object equality](test_object.md#object-equality)). For a lot of complex objects, the implementation of `==` causes the object instances to be compared... not their underlying meaning. For example when the solution is:

    *** =solution
    ```
    from urllib.request import urlretrieve
    fn1 = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite'
    urlretrieve(fn1, 'Chinook.sqlite')
    from sqlalchemy import create_engine
    import pandas as pd
    engine = create_engine('sqlite:///Chinook.sqlite')

    # Execute query and store records in dataframe: df
    df = pd.read_sql_query("SELECT * FROM Album", engine)
    ```

And the SCT is:

    *** =sct
    ```
    test_function_v2("pandas.read_sql_query", params = ['sql', 'con'], do_eval = [True, False])
    ```

The SCT will fail even if the student uses this exact solution code. The reason being that the `engine` object is compared in the solution and student process. The engine object is evaluated by `create_engine('sqlite:///Chinook.sqlite')`. As you can try out yourself, `create_engine('sqlite:///Chinook.sqlite') == create_engine('sqlite:///Chinook.sqlite')` will always be `False`, even though they are semantically exactly the same. A better way of testing this code would be:

    *** =sct
    test_correct(
        lambda: test_object("df"),
        lambda: test_function_v2("pandas.read_sql_query", do_eval=False)
    )

This SCT will not do exactly the same, but it will test enough in practice 99% of the time. Check out [the section about Object equality](test_object.md#object-equality) for complex objects that DO have a good equality implementation.

**NOTE**: Behind the scenes, `pythonwhat` has to fetch the value of objects from sub-processes. The required 'dilling' and 'undilling' can cause issues for exotic objects. For more information on this and possible errors that can occur, read the [Processes article](../expression_tests.md).
