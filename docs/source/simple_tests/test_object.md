test_object
-----------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_object.test_object
```

    test_object(name,
                eq_condition="equal",
                do_eval=True,
                undefined_msg=None,
                incorrect_msg=None)

`test_object()` enables you to test whether a student correctly defined an object.

As explained on the [docs home](/Home.md), both the student's submission as well as the solution code are executed, in separate processes. `test_object()` looks at these processes and checks if the object specified in `name` is available in the student process. Next, it checks whether the object in the student and solution process correspond. In case of a failure along the way, `test_object()` will generate a meaningful feedback message that you can override.

### Example 1

Suppose we have the following solution:

    *** =solution
    ```{python}
    # Create a variable x, equal to 3 * 5
    x = 3 * 15
    ```

To test this we simply use:

    *** =sct
    ```{python}
    test_object("x")
    success_msg("Great job!")
    ```

This SCT will test if the variable `x` is defined, and has the same ending value in the student process as in the solution process. All of the following student submissions would be accepted by `test_object()`:

- `x = 15`
- `x = 12 + 3`
- `x = 3; x += 12`

How the object `x` came about in the student's submission, does not matter: only the end result, the actual content of `x`, matters.

`do_eval=True` by default; if you set it to `False`, only the existence of an object `x` will be checked; its contents will not be compared to the object `x` that's in the solution process.

### Object equality

When comparing more complex objects in Python, chances are they don't use the equality operation you desire. Python objects are compared using the `==` operator, and objects can overwrite its implementation to fit the object's needs. Internally, `test_object()` uses the `==` operation to compare objects, this means you could encounter undesirable behaviour. Sometimes `==` just compares the actual object instances, and objects which are semantically alike wont be according to `test_object()`.

Say, for example, that you have the following solution:

    *** =solution
    from urllib.request import urlretrieve
    fn1 = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite'
    urlretrieve(fn1, 'Chinook.sqlite')

    # Import packages
    from sqlalchemy import create_engine
    import pandas as pd

    # Create engine: engine
    engine = create_engine('sqlite:///Chinook.sqlite')

    # Open engine connection
    con = engine.connect()

An SCT for this exercise could be the following:

    *** =sct
    test_object("engine")
    test_object("con")

Now, if the student enters the exact same code as the solution, the SCT will still fail. How? Well if you try this out: `create_engine('sqlite:///Chinook.sqlite') == create_engine('sqlite:///Chinook.sqlite')` you will notice that it returns `False`. This means the exact same execution doesn't lead to the the exact same object (although they might be semantically equal). We can't use `test_object` like that here. There are several ways to solve this:

#### Workaround

    *** =sct
    test_object("engine", do_eval=False)
    test_function("create_engine")
    test_object("con", do_eval=False)
    test_function("engine.connect")

This will check whether the objects `engine` and `con` are declared, without checking for it's value. With `test_function()` we check whether they used the correct functions. This will not test the exact same thing as the first SCT, but it's effective 99% of the time.

#### Equality operations hardcoded in `pythonwhat`

A side note here, complex objects that are used a lot have an custom implementation of equality built for them in `pythonwhat`. These objects can be tested with a regular `test_object(...)`, without having to use `do_eval=False`. At the moment, the more complex classes that can be tested are:

- `numpy.ndarray`
- `pandas.DataFrame`
- `pandas.Series`

Of course primitive classes like `str`, `int`, `list`, `dict`, ... can be tested without any problems too, as well as objects of which the class has a semantically correct implementation of the `==` operator.

#### Manually define a converter

As explained in the [Processes article](../expression_tests.md), objects are extracted from their respected processes by 'dilling' and 'undilling' them. However, you can manually set a 'converter' with the `set_converter()` function. This will override the default dilling and undilling behavior, and enables you to make simplified representations of custom objects, testing only exactly what you want to test.

**NOTE**: Behind the scenes, `pythonwhat` has to fetch the value of objects from sub-processes. The required 'dilling' and 'undilling' can cause issues for exotic objects. For more information on this and possible errors that can occur, read the [Processes article](../expression_tests.md).
