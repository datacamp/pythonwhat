Expression tests
----------------

Expression tests run pieces of the student and solution code, and then check the resulting value, printed output, or errors they produce.

``has_equal`` syntax
====================

Once student/submission code has been selected using a check function, we can run it using one of three functions.
They all take the same arguments, and run the student and submission code in the same way.
However, they differ in how they compare the outcome:

* ``has_equal_value()`` - compares the value returned by the code.
* ``has_equal_output()`` - compares printed output.
* ``has_equal_error()`` - compares any errors raised.

Basic Usage
===========

Running the whole code submission 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the example below, we re-run the entire student and submission code, and check that they print out the same output.

.. code::

    # solution
    x = [1,2,3]
    print(x)

    # sct
    Ex().has_equal_output()

Note that while we could have used ``has_output()`` to verify that the student printed ``"[1, 2, 3]"``,
using ``has_equal_output`` simply requires that the student output matches the solution output.

Running part of the code
~~~~~~~~~~~~~~~~~~~~~~~~

Combining an expression test with part checks will run only a piece of the submitted code.
The example below first uses ``has_equal_value`` to run an entire if expression, and then to run only its body.

.. code::
    
    # solution
    x = [1,2,3]
    sum(x) if x else None
    
    # sct to test body of if expression
    (Ex().check_if_exp(0)     # focus on if expression
         .has_equal_value()   # run entire if expression, check value
         .check_body()        # focus on body "sum(x)"
         .has_equal_value()   # run body, check value
         )
    
.. note::

    Because ``has_equal_value()`` returns the exact same state as it was passed,
    commands chaining off of ``has_equal_value`` behave as they would have if ``has_equal_value`` weren't used.

Context Values
==============

Suppose we want the student to define a function, that loops over the elements in a dictionary, and prints out each key and value, as follows:

.. code::

    # solution
    def print_dict(my_dict):
        for key, value in my_dict.items():
            print(key + " - " + str(value))

An appropriate SCT for this exercise could be the following (for clarity, we're not using any default messages):

.. code::

    # get for loop code, set context for my_dict argument
    for_loop = (Ex()
         .check_function_def('print_dict')          # ensure 'print_dict' is defined
         .check_body()                              # get student/solution code in body
         .set_context(my_dict = {'a': 2, 'b': 3})   # set print_dict's my_dict arg
         .check_for_loop(0)                         # ensure for loop is defined
         )
    
    # test for loop iterator
    for_loop.check_iter().has_equal_value()         # run iterator (my_dict.items())
    # test for loop body
    for_loop.check_body().set_context(key = 'c', value = 3).has_equal_value()

Assuming the student coded the function in the exact same way as the solution, the following things happen:

- checks whether ``print_dict`` is defined, then gets the code for the function definition body.
- because ``print_dict`` takes an argument ``my_dict``, which would be undefined if we ran the body code, ``set_context`` defines what ``my_dict`` should be when running the code. Note that its okay if the submitted code named the argument ``my_dict`` something else, since set_context matches submission / solution arguments up by position.

When running the bottom two SCTs for the for_loop

- ``for_loop.check_iter().has_equal_value()`` - runs the code for the iterator, ``my_dict.items()`` in the solution and its corresponding code in the submission, and compares the values they return.
- ``for_loop.check_body().set_context(key = 'c', value = 3).has_equal_value()`` - runs the code in the for loop body, ``print(key + " - " + str(value))`` in the solution, and compares outputs. 
  Since this code may use variables the for loop defined, ``key`` and ``value``, we need to define them using ``set_context``.

How are Context Values Matched?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Context values are matched by position. For example, the submission and solution codes...

.. code::

   # solution
   for ii, x in enumerate(range(3)): print(ii)
   
   # student submission
   for jj, y in enumerate(range(3)): print(jj)

Using ``Ex().check_for_loop(0).check_body().set_context(...)`` will do the following...

====================== ======================= ==========================
 statement              solution (ii, x)        submission (jj, y)
====================== ======================= ==========================
set_context(ii=1, x=2)  ii = 1, x = 2           jj = 1, y = 2
set_context(ii=1)       ii = 1, x is undefined  jj = 1, y is undefined
set_context(x=2)        ii is undefined, x = 2  jj is undefined, y = 2
====================== ======================= ==========================

.. note:: 
   
   If ``set_context`` does not define a variable, nothing is done with it.
   This means that in the code examples above, running the body of the for loop would call print with ::ii:: or ::jj:: left at 2 (the values they have in the solution/submission environments).

Context values for nested parts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Context values may now be defined for nested parts. For example, the print statement below,

.. code::

    for i in range(2):              # outer for loop part
        for j in range(3):          # inner for loop part
            print(i + j)

may be tested by setting context values at each level,

.. code::

    (Ex()
        .check_for_loop(0).check_body().set_context(i = 1)    # outer for
        .check_for_loop(0).check_body().set_context(j = 2)    # inner for
            .has_equal_output()
        )


``pre_code``: fixing mutations
===============================

Python code commonly mutates, or changes values within an object. 
For example, the variable ``x`` points to an object that is mutated every time a function is called.


.. code::

    x = {'a': 1}

    def f(d): d['a'] += 1

    f(x)     # x['a'] == 2 now
    f(x)     # x['a'] == 3 now

In this case, when ``f`` is run, it changes the contents of ``x`` as a side-effect and returns None.
When using SCTs that run expressions, mutations in either the solution or submission environment can cause very confusing results.
For example, calling ``np.random.random()`` will advance numpy's random number generator. Consider the markdown source for an exercise that illustrates this.

.. code-block:: none

    `@pre_exercise_code`
    ```{python}
    import numpy as np
    np.random.seed(42)               # set random generator seed to 42
    ```

    `@solution`
    ```{python}
    if True: np.random.random()      # 1st random call: .37
    
    np.random.random()               # 2nd random call: .95
    ```
   
    `@sct`
    ```{python}
    # Should pass but fails, because random generator has advanced
    # twice in solution, but only once in submission
    Ex().check_if_else(0).check_body().has_equal_value()
    ```

Assume this student submission:

.. code::

    if True: np.random.random()      # 1st random call: .37
     
    # forgot 2nd call to np.random.random()
    

In this situation the random seed is set to 42, but the solution code advances the random generator further than the submission code.
As a result the SCT will fail. In order to test random code, the random generator needs to be at the same state between submission and solution environments.
Since their generators can be thrown out of sync, the most reliable way to do this is to set the seed using the ``pre_code`` argument to ``has_equal_value``.
In the case above, the SCT may be fixed as follows

.. code:: 

   Ex().check_if_else(0).check_body().has_equal_value(pre_code = "np.random.seed(42)")

More generally, it can be helpful to define a pre_code variable to use before expression tests...

.. code::

   pre_code = """
   np.random.seed(42)
   """
   
   Ex().has_equal_output(pre_code=pre_code)
   Ex().check_if_else(0).check_body().has_equal_value(pre_code = pre_code)


``extra_env``
=============

As illustrated in the `Advanced part checking section <checking_compound_statements.html#advanced-part-checking>`_  of the Checking compound statements article,
``set_env()`` (as a function) or ``extra_env`` (as an arugment) can be used to temporarily override the student and solution process to
run an expression in multiple situations.

Setting extra environment variables is similar to ``pre_code``, in that you can (re)define objects in the student and submission environment before running an expression.
The difference is that, rather than passing a string that is executed in each environment, ``extra_env`` lets you pass objects directly.
For example, the three SCT chains below are equivalent...

.. code::

    Ex().has_equal_value(pre_code="x = 10")
    Ex().set_env(x = 10).has_equal_value()
    Ex().has_equal_value(extra_env = {'x': 10})

In practice they can often be used interchangably.
However, one area where ``extra_env`` may shine is in mocking up data objects before running tests.
For example, if the SCT below didn't use ``extra_env``, then it would take a long time to run.

.. code::

   `@pre_exercise_code`
   ```{python}
   a_list = list(range(10000000))
   ```

   `@solution`
   ```{python}
   print(a_list[1])
   ```

   `@sct`
   ```{python}
   Ex().set_env(a_list = list(range(10))).has_equal_output()
   ```
   
The reason extra_env is important here, is that ``pythonwhat`` tries to make a deepcopy of lists, so that course developers don't get bit by unexpected mutations.
However, the larger the list, the longer it takes to make a deepcopy. 
If an SCT is running slowly, there's a good chance it uses a very large object that is being copied for every expression test.

``expr_code``: change expression
================================

The ``expr_code`` argument takes a string, and uses it to replace the code that would be run by an expression test.
For example, the markdown source for the following exercise simply runs ``len(x)`` in the solution and student environments.
   
.. code::

    `@solution`
    ```{python}
    # keep x the same length
    x = [1,2,3]
    ```

    `@sct`
    ```{python}
    Ex().has_equal_value(expr_code="len(x)")
    ```
   
.. note::

   Using ``expr_code`` does not change how expression tests perform highlighting. 
   This means that ``Ex().for_loop(0).has_equal_value(expr_code="x[0]")`` would highlight the body of the checked for loop.


``call`` Syntax
===============

Testing a function definition or lambda may require calling it with some arguments.
In order to do this, use the ``call()`` SCT.
There are two ways to tell it what arguments to pass to the function/lambda,

- ``call("f (1, 2, x = 3)")`` - as a string, where ``"f"`` gets substituted with the function's name.
- ``call([1,2,3])`` - as a list of positional arguments.

Below, two alternative ways of specifying the arguments to pass are shown.

.. code::

    # solution
    def my_fun(x, y = 4, z = ('a', 'b'), *args, **kwargs):
        return [x, y, *z, *args]
 
    # sct
    Ex().check_function_def('my_fun').call("f(1, 2, (3,4), 5, kw_arg='ok')")  # as string
    Ex().check_function_def('my_fun').call([1, 2, (3,4), 5])                  # as list

.. note::

   Technically, you can get crazy and replace the list approach with a dictionary of the form ``{'args': [POSARG1, POSARG2], 'kwargs': {KWARGS}}``.

Additional Parameters
~~~~~~~~~~~~~~~~~~~~~

In addition to its first argument, ``call()`` accepts all the parameters that the expression tests above can (i.e. ``has_equal_value``, ``has_equal_error``, ``has_equal_output``).
The function call is run at the point where these functions would evaluate an expression.
Moreover, setting the argument ``test`` to either "value", "output", or "error" controls which expression test it behaves like.

For example, the SCT below shows how to run some ``pre_code``, and then evaluate the output of a call.

.. code::

    Ex().check_function_def('my_fun').call("f(1, 2)", test="output", pre_code="x = 1")
