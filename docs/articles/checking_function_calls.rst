Checking function calls
-----------------------

Basic functionality
===================

Take the following example that checks whether a student used the ``round()`` function correctly:

.. code::

    # solution
    round(2.718282, ndigits = 3)

    # sct
    Ex().check_function("round").multi(
        check_args("number").has_equal_value(),
        check_args("ndigits").has_equal_value()
    )

    # submissions that pass:
    round(2.718282, 3)
    round(2.718282, ndigits = 3
    round(number=2.718282, ndigits=3)
    round(ndigits=3, number=2.718282)
    val=2.718282; dig=3; round(val, dig)
    val=2.718282; dig=3; round(number=val, dig)
    int_part = 2; dec_part = 0.718282; round(int_part + dec_part, 3)


- `check_function()` checks whether ``round()`` is called by the student, and parses all the arguments.
- ``check_args()`` checks whether a certain argument was specified, and zooms in on the expression used to specify that argument.
- ``has_equal_value()`` will rerun the expressions used to specify the arguments in both student and solution process, and compare the results.

.. note::

    In ``check_args()`` you can refer to the argument of a function call both by argument name and by position.

Customizations
~~~~~~~~~~~~~~

If you only want to check the ``number`` parameter, just don't include a second chain with ``check_args("ndigits")``:

.. code::

    Ex().check_function("round").check_args("number").has_equal_value()

If you only want to check whether the ``number`` parameter was specified, but not that it was specified correctly, drop ``has_equal_value()``:

.. code::

    Ex().check_function("round").check_args("number")

If you just want to check whether the function was called, drop ``check_args()``:

.. code::

    Ex().check_function("round")

If you want to compare the 'string versions' of the expressions used to set the arguments instead of the evaluated result of these expressions,
you can use ``has_equal_ast()`` instead of ``has_equal_value()``:

.. code:

    Ex().check_function("round").multi(
        check_args("number").has_equal_ast(),
        check_args("ndigits").has_equal_value()
    )

Now, the following submissions would fail:

- ``val=2.718282; dig=3; round(val, dig)`` -- the string representation of ``val`` in the student code is compared to ``2.718282`` in the solution code.
- ``val=2.718282; dig=3; round(number=val, dig)`` -- same
- ``int_part = 2; dec_part = 0.718282; round(int_part + dec_part, 3)`` -- the string representation of ``int_part + dec_part`` in the student code is compered to ``2.718282`` in the solution code.

As you can see, doing exact string comparison of arguments is not a good idea here, as it is very inflexible.
There are cases, however, where it makes sense to use this, e.g. when there are very big objects passed to functions,
and you don't want to spend the processing power to fetch these objects from the student and solution processes.

Functions in packages
=====================

If you're testing whether function calls of particular packages are used correctly, you should always refer to these functions with their 'full name'.
Suppose you want to test whether the function ``show`` of ``matplotlib.pyplot`` was called, use this SCT:

.. code::

    Ex().check_function("matplotlib.pyplot.show")

``check_function()`` can handle it when a student used aliases for the python packages (all ``import`` and ``import * from *`` calls are supported).
If the student did not properly call the function, ``check_function()`` will automatically generate a feedback message that corresponds to how the student imported the modules/functions.

.. note:

    No matter how you import the function, you always have to refer to the function with its full name, e.g. ``package.subpackage1.subpackage2.function``.

has_equal_value? has_equal_ast?
===============================

In the customizations section above, you could already notice the difference between ``has_equal_value()`` and ``has_equal_ast()`` for checking
whether arguments are correct. The former **reruns** the expression used to specify the argument in both student and solution process
and compares their results, while the latter simply compares the expression's AST representations. Clearly, the former is more robust, but there
are some cases in which ``has_equal_ast()`` can be useful:

- For better feedback. When using ``has_equal_ast()``, the 'expected x got y' message that is automatically generated when the arguments
  don't match up will use the actual expressions used. ``has_equal_value()`` will use string representations of the evaluations of the expressions,
  if they make sense, and this is typically less useful.
- To avoid very expensive object comparisons. If you are 100% sure that the object people have to pass as an argument is already correct (because
  you checked it earlier in the SCT or because it was already specified in the pre exercise code) and doing an equality check on this object between
  student and solution project is likely going to be expensive, then you can safely use ``has_equal_ast()`` to speed things up.
- If you want to save yourself the trouble of building exotic contexts. You'll often find yourself checking function calls in e.g. a for loop.
  Typically, these function calls will use objects that were generated inside the loop. To easily unit test the body of a for loop, you'll typically
  have to use ``set_context()`` and ``set_env()``. For exotic for loops, this can become tricky, and it might be a quick fix to be a little more
  specific about the object names people should use, and just use ``has_equal_ast()`` for the argument comparison. That way, you're bypassing the need
  to build up a context in the student/solution process and do object comparisions.


Signatures
==========

The ``round()`` example earlier in this article showed that a student can call the function in a multitude of ways,
specifying arguments by position, by keyword or a mix of those. To be robust against this, pythonwhat uses the concept of argument binding.

More specifically, each function has a function signature. Given this signature and the way the function was called,
argument binding can map each parameter you specified to an argument. This small demo fetches the signature of the ``open`` function and tries to
bind arguments that have been specified in two different ways. Notice how the resulting bound arguments are the same:

.. code::

    >>> import inspect

    >>> sig = inspect.signature(open)

    >>> sig
    <Signature (file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)>

    >>> sig.bind('my_file.txt', mode = 'r')
    <BoundArguments (file='my_file.txt', mode='r')>

    >>> sig.bind(file = 'my_file.txt', mode = 'r')
    <BoundArguments (file='my_file.txt', mode='r')>


When you're using ``check_args()`` you are actually selecting these bound arguments.
This works fine for functions like ``round()`` and ``open()`` that have a list of named arguments,
but things get tricky when dealing with functions that take ``*args`` and ``*kwargs``.

``*args`` example
~~~~~~~~~~~~~~~~~

Python allows functions to take a variable number of unnamed arguments through ``*args``, like this function:

.. code::

    def multiply(*args):
        res = 1
        for num in args:
            res *= num
        return res

Let's see what happens when different calls are bound to their arguments:

.. code::

    >>> import inspect

    >>> inspect.signature(multiply)
    <Signature (*args)>

    >>> sig = inspect.signature(multiply)

    >>> sig
    <Signature (*args)>

    >>> sig.bind(1, 2)
    <BoundArguments (args=(1, 2))>    

    >>> sig.bind(3, 4, 5)
    <BoundArguments (args=(3, 4, 5))>

Notice how now the list of arguments is grouped under a tuple with the name ``args`` in the bound arguments.
To be able to check each of these arguments individually, pythonwhat allows you to do repeated indexing in ``check_args()``.
Instead of specifying the name of an argument, you can specify a list of indices:

.. code::

    # solution to check against
    multiply(2, 3, 4)

    # corresponding SCT
    Ex().check_function("multiply").multi(
        check_args(["args", 0]).has_equal_value(),
        check_args(["args", 1]).has_equal_value(),
        check_args(["args", 2]).has_equal_value()
    )

The ``check_args()`` subchains each zoom in on a particular tuple element of the bound ``args`` argument.

``**kwargs`` example
~~~~~~~~~~~~~~~~~~~~

Python allows functions to take a variable number of named arguments through ``**kwargs``, like this function:

.. code::

    def my_dict(**kwargs):
        return dict(**kwargs)

Let's see what happens when different calls are bound to their arguments:

.. code::

    >>> import inspect

    >>> sig = inspect.signature(my_dict)

    >>> sig.bind(a = 1, b = 2)
    <BoundArguments (kwargs={'b': 2, 'a': 1})>

    >>> sig.bind(c = 2, b = 3)
    <BoundArguments (kwargs={'b': 3, 'c': 2})>

Notice how now the list of arguments is grouped under a dictionary name ``kwargs`` in the bound arguments.
To be able to check each of these arguments individually, pythonwhat allows you to do repeated indexing in ``check_args()``.
Instead of specifying the name of an argument, you can specify a list of indices:

.. code::

    # solution to check against
    my_dict(a = 1, b = 2)

    # corresponding SCT
    Ex().check_function("my_dict").multi(
        check_args(["kwargs", "a"]).has_equal_value(),
        check_args(["kwargs", "b"]).has_equal_value()
    )

The ``check_args()`` subchains each zoom in on a particular dictionary element of the bound ``kwargs`` argument.

Manual signatures
~~~~~~~~~~~~~~~~~

Unfortunately for a lot of Python's built-in functions no function signature is readily available because the function has been implemented in C code.
To work around this, pythonwhat already includes manually specified signatures for functions such as ``print()``, ``str()``, ``hasattr()``, etc,
but it's still possible that some signatures are missing.

That's why ``check_function()`` features a ``signature`` parameter, that is ``True`` by default.
If pythonwhat can't retrieve a signature for the function you want to test,
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
- The second argument should be the 'kind' of parameter. ``param.POSITIONAL_OR_KEYWORD`` tells ``check_function`` that the parameter can be specified either through a positional argument or through a keyword argument.
Other common possibilities are ``param.POSITIONAL_ONLY`` and ``param.KEYWORD_ONLY`` (for a full list, refer to the `docs <https://docs.python.org/3.4/library/inspect.html#inspect.Parameter>`_).
- The third optional argument allows you to specify a default value for the parameter.  

.. note:: 

    If you find vital Python functions that are used very often and that are not included in pythonwhat by default, you can `let us know <mailto:content-engineering@datacamp.com>`_ and we'll add the function to our `list of manual signatures <https://github.com/datacamp/pythonwhat/blob/master/pythonwhat/signatures.py>`_.

Multiple function calls
=======================

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

The first ``check_function()`` chain, where ``index=0``, looks for the first call of ``round()`` in both student solution code,
while ``check_funtion()`` with ``index=1`` will look for the second function call. After this, the rest of the SCT chain behaves as before.

Methods
=======

Methods are Python functions that are called on objects. For testing this, you can also use ``check_function()``.
Consider the following examples, that calculates the ``mean()`` of the column ``a`` in the pandas data frame ``df``:

.. code::

    # pec
    import pandas as pd
    df = pd.DataFrame({ 'a': [1, 2, 3, 4] })

    # solution
    df.a.mean()

    # sct
    Ex().check_function('df.a.mean').has_equal_value()
    ```

The SCT is checking whether the method ``df.a.mean`` was called in the student code, and whether rerunning the call in both student and solution process is returning the same result.

As a more advanced example, consider this example of chained method calls:

.. code::

    # pec
    import pandas as pd
    df = pd.DataFrame({ 'type': ['a', 'b', 'a', 'b'], 'val': [1, 2, 3, 4] })

    # solution
    df.groupby('type').mean()

    # sct
    Ex().check_function('df.groupby').check_args(0).has_equal_value()
    Ex().check_function('df.groupby.mean', signature=sig_from_obj('df.mean')).has_equal_value()

Here:

- The first SCT is checking whether ``df.groupby()`` was called and whether the argument for ``df.groupby()`` was specified correctly to be ``'type'``.
- The second SCT is first checking whether ``df.groupby.mean()`` was called and whether calling it gives the right result. Notice several things:

  + We describe the entire chain of method calls, leaving out the parentheses and arguments used for method calls in between.
  + We use ``sig_from_obj()`` to manually specify a Python expression that pythonwhat can use to derive the signature from.
    If the string you use to describe the function to check evaluates to a method or function in the solution process, like for ``'df.groupby'``,
    pythonwhat can figure out the signature. However, for ``'df.groupby.mean'`` will `not` evaluate to a method object in the solution process,
    so we need to manually specify a valid expression that `will` evaluate to a valid signature with ``sig_from_obj()``.

In this example, you are only checking whether the function is called and whether rerunning it gives the correct result.
You are not checking the actual arguments, so there's actually no point in trying to match the function call to its signature.
In cases like this, you can set ``signature=False``, which skips the fetching of a signature and the binding or arguments altogether:

.. code::

    # pec
    import pandas as pd
    df = pd.DataFrame({ 'type': ['a', 'b', 'a', 'b'], 'val': [1, 2, 3, 4] })

    # solution
    df.groupby('type').mean()

    # sct
    Ex().check_function('df.groupby').check_args(0).has_equal_value()
    Ex().check_function('df.groupby.mean', signature=False).has_equal_value()

.. warning::

    Watch out with disabling signature binding as a one-stop solution to make your SCT run without errors.
    If there are arguments to check, argument binding makes sure that various ways of
    calling the function can all work. Setting ``signature=False`` will skip this binding, which can
    cause your SCT to mark perfectly valid student submissions as incorrect!

.. note::

    You can also use the ``sig_from_params()`` function to manually build the signature from scratch,
    but this this more work than simply specifying the function object as a string from which to extract the signature.


