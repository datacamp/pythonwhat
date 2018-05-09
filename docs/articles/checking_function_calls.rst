Checking function calls
-----------------------

Testing functions is probably one of the most common things you'll do when writing SCTs.
The functions in ``pythonwhat`` related to testing functions allow you to test whether students correctly called particular functions,
with the correct arguments and whether these arguments are correct.
To assess all of these aspects, ``pythonwhat`` goes through the solution code to see which functions were called there and how,
and also checks the solution process to see what the value of the parameters is. This makes the comparison of function calls concise yet robust.

Example 1: Basic
================

Suppose you want the student to call the ``round()`` function on ``2.718282``, as follows:

.. code::

    # round 2.718282 to 3 digits
    round(2.718282, 3)

The following SCT tests whether the ``round()`` function is used correctly:

.. code::

    Ex().check_function("round").multi(
        check_args("number").has_equal_value(),
        check_args("ndigits").has_equal_value()
    )

When a student submits his code and SCT is executed, `check_function()` tests whether the student has called the function `round()`.
Next, `check_args()` checks whether each argument was specified (you can also refer to positional arguments by passing an integer).
Finally, `has_equal_value()` checks whether the values of the argument are the same as in the solution.
So in this case, it tests whether `round()` is used with the `number` argument equal to `pi` and the second argument equal to `3`.
The above SCT would accept all of the following submissions:

- `round(2.718282, 3)`
- `round(number=2.718282, 3)`
- `round(number=2.718282, ndigits=3)`
- `round(ndigits=3, number=2.718282)`
- `val=2.718282; dig=3; round(val, dig)`
- `val=2.718282; dig=3; round(number=val, dig)`
- `int_part = 2; dec_part = 0.718282; round(int_part + dec_part, 3)`

.. note::
    
    To find out which arguments you have to specify in `check_args()`, you can check out the reference documentation of the function you're trying to check.

Customizations
~~~~~~~~~~~~~~

If you only want to check the ``number`` parameter, just don't include a second chain with `check_args("ndigits")`:

.. code::

    Ex().check_function("round").check_args("number").has_equal_value()

If you just want to check whether the function was called, but you don't want to check any arguments, don't use `check_args()` in the first place:

.. code::

    Ex().check_function("round")

If you want to compare the 'string versions' of arguments instead of the actual values of the arguments after evaluating them, use ``has_equal_ast()`` instead of ``has_equal_value()``.

.. code:

    Ex().check_function("round").multi(
        check_args("number").has_equal_ast(),
        check_args("ndigits").has_equal_value()
    )

Now, the following submissions would fail:

- `val=2.718282; dig=3; round(val, dig)` -- the string representation of ``val`` in the student code is compared to ``2.718282`` in the solution code.
- `val=2.718282; dig=3; round(number=val, dig)` -- same
- `int_part = 2; dec_part = 0.718282; round(int_part + dec_part, 3)` -- the string representation of ``int_part + dec_part`` in the student code is compered to ``2.718282`` in the solution code.

As you can see, doing exact string comparison of arguments is not a good idea, as it is very inflexible.
There are cases, however, where it makes sense to use this, e.g. when there are very big objects passed to functions,
and you don't want to spend the processing power to fetch these objects from the coding processes.

Example 2: Multiple function calls
==================================

Inside ``check_function()`` the ``index`` argument (``0`` by default), becomes important when there are several calls of the same function.
Suppose that your exercise requires the student to call the ``round()`` function twice: once on ``pi`` and once on Euler's number:

.. code::

    # Call round on pi
    round(3.14159, 3)

    # Call round on e
    round(2.71828, 3)

To test both these function calls, you'll need the following SCT:

.. code::

    Ex().check_function("round", 0).multi(
        check_args("number").has_equal_value()
        check_args("ndigits").has_equal_value()
    )
    Ex().check_function("round", 1).multi(
        check_args("number").has_equal_value()
        check_args("ndigits").has_equal_value()
    )

The first ``check_function()`` chain, where ``index=0``, checks the solution code for the first function call of ``round()``, finds it - ``round(3.14159, 3)`` - and then goes to look through the student code to find a function call of ``round()`` that matches the arguments.
It is perfectly possible that there are 5 function calls of ``round()`` in the student's submission, and that only the fourth call matches the requirements for ``test_function_v2()``.
As soon as a function call is found in the student code that passes all tests, ``pythonwhat`` heads over to the second ``test_function_v2()`` call, where ``index=2``.
The same thing happens: the second call of ``round()`` is found from the solution code, and a match is sought for in the student code.

This means that all of the following student submissions would be accepted:

  - `round(3.14159, 3); round(2.71828, 3)`
  - `round(2.71828, 3); round(3.14159, 3)`
  - `round(number=3.14159, ndigts=3); round(number=2.71828, 3)`
  - `round(number=2.71828, 3); round(number=3.14159, 3)`
  - `round(3.14159, 3); round(123.456); round(2.71828, 3)`
  - `round(2.71828, 3); round(123.456); round(3.14159, 3)`

Example 3: Functions in packages
================================

If you're testing whether function calls of particular packages are used correctly, you should always refer to these functions with their 'full name'.
Suppose you want to test whether the function ``show`` of ``matplotlib.pyplot`` was called, use this SCT:

.. code::

    Ex().check_function("matplotlib.pyplot.show")

``check_function()`` can handle it when a student used aliases for the python packages (all ``import`` and ``import * from *`` calls are supported).
If the student did not properly call the function, ``check_function()`` will automatically generate a feedback message that corresponds to how the student imported the modules/functions.

.. note:

    No matter how you import the function, you always have to refer to the function with its full name, e.g. ``package.subpackage1.subpackage2.function``.

Example 4: Manual signatures
============================

To implement resilience against different ways of specify function parameters, the ``inspect`` module is used, that is part of Python's basic distribution.
Through ``inspect.signature()`` a function's parameters can be inferred, and then 'bound' to the arguments that the student specified.
However, this signature is not available for all of Python's functions. More specifically, Python's built-in functions that are implemented in C don't allow a signature to be extracted from them.
``pythonwhat`` already includes manually specified signatures for functions such as ``print()``, ``str()``, ``hasattr()``, etc, but it's still possible that some signatures are missing.

That's why ``check_function()`` features a ``signature`` parameter, that is ``None`` by default.
If ``pythonwhat`` can't retrieve a signature for the function you want to test,
you can pass an object of the class ``inspect.Signature`` to the ``signature`` parameter.

Suppose, for the sake of example, that ``check_function()`` can't find a signature for the ``round()`` function.
In a real situation, you will be informed about a missing signature through a backend error.
To be able to implement this SCT, you can use the ``sig_from_params()`` function:

.. code::

    sig = sig_from_params(param("number", param.POSITIONAL_OR_KEYWORD),
                          param("ndigits", param.POSITIONAL_OR_KEYWORD, default=0))
    Ex().check_function("round", signature=sig).multi(
        check_args("number").has_equal_value(),
        check_args("ndigits").has_equal_value()
    )

You can pass ``sig_from_params()`` as many parameters as you want.

``param`` is an alias of the ``Parameter`` class that's inside the ``inspect`` module.
- The first argument of ``param()`` should be the name of the parameter,
- The second argument should be the 'kind' of parameter. ``param.POSITIONAL_OR_KEYWORD`` tells ``test_function_v2`` that the parameter can be specified either through a positional argument or through a keyword argument.
Other common possibilities are ``param.POSITIONAL_ONLY`` and ``param.KEYWORD_ONLY`` (for a full list, refer to the `docs <https://docs.python.org/3.4/library/inspect.html#inspect.Parameter>`_).
- The third optional argument allows you to specify a default value for the parameter.  


.. note:: 

    If you find vital Python functions that are used very often and that are not included in ``pythonwhat`` by default, you can `let us know <mailto:content-engineering@datacamp.com>`_ and we'll add the function to our `list of manual signatures <https://github.com/datacamp/pythonwhat/blob/master/pythonwhat/signatures.py>`_.

Example 5: Methods
==================

Python also features methods, i.e. functions that are called on objects. For testing this, you can also use ``check_function()``. Consider the following solution code, that creates a connection to an SQLite Database with ``sqlalchemy``.

.. code::

    # prep
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

To test the last chained method calls, you can use the following SCT.
Notice from the second ``check_function()`` call here that you have to describe the entire chain (leaving out the arguments that are passed to ``execute()``).
This way, you explicitly list the order in which the methods should have been called.

.. code::

    Ex().check_function("connection.execute").check_args("object")
    Ex().check_function("connection.execute.fetchall")


Example 6: Signatures for methods
=================================

In the previous example, you might have noticed that ``check_function()`` was capable to infer that ``connection`` is a ``Connection`` object, and that ``execute()`` is a method of the ``Connection`` class.
For checking method calls that aren't chained, this is possible, but for chained method calls, such as ``connection.execute.fetchall``, this is not possible.
In those cases you'll have to manually specify a signature. With ``sig_from_obj()`` you can specify the function from which to extract a signature.

The following full example shows how it's done:

.. code::

    `@pre_exercise_code`
    ```{python}
    class Test():
        def __init__(self, a):
            self.a = a

        def set_a(self, value):
            self.a = value
            return(self)
    x = Test(123)
    ```

    `@solution`
    ```{python}
    x.set_a(843).set_a(102)
    ```

    `@sct`
    ```{python}
    sig = sig_from_obj('x.set_a')
    Ex().check_function('x.set_a.set_a', params=['value'], signature=sig)
    ```

.. note::

    You can also use the ``sig_from_params()`` function to manually build the signature from scratch,
    but this this more work than simply specifying the function object as a string from which to extract the signature.

Example 7: Exotic Argument equality
===================================

Just as for objects, evaluated arguments are compared using the ``==`` operator. For a lot of complex objects, the implementation of ``==`` causes the object instances to be compared instead of their underlying meaning. Take this solution, for example:

.. code::

    from urllib.request import urlretrieve
    fn1 = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite'
    urlretrieve(fn1, 'Chinook.sqlite')
    from sqlalchemy import create_engine
    import pandas as pd
    engine = create_engine('sqlite:///Chinook.sqlite')

    # Execute query and store records in dataframe: df
    df = pd.read_sql_query("SELECT * FROM Album", engine)

With the following SCT:

.. code::

    Ex().check_function("pandas.read_sql_query").multi(
        check_args("sql").has_equal_value(),
        check_args("con").has_equal_ast()
    )

Notice that we needed to use ``has_equal_ast()`` to comparse the `engine` objects in student and solution code. As explained in `this subsection of the checking objects article <checking_objects.html#example-3-exotic-objects>`_, engine objects can not be properly compared.
You can work around this by manually defining a so-called converter. To learn more about this, visit the `Processes article <processes.html>`_.


Example 8: Deeper argument testing
==================================

Suppose you want to test whether a list comprehension was used to call the ``sum()`` function was used:

.. code::

    # call sum on a list comp
    sum([i for i in range(10)])

This SCT verifies that the first argument passed to sum is a list comprehension.

.. code::

   Ex().check_function('sum').check_args(0).check_list_comp(0).has_equal_ast()

