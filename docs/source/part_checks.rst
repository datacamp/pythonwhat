Part Checks
================

.. role:: python(code)
   :language: python

Check Syntax
--------------

In Brief
~~~~~~~~

While functions beginning with ``test_``, such as ``test_student_typed`` look over some code or output, ``check_`` functions allow us to zoom in on parts of that student and solution code.

For example, ``check_list_comp`` examines list comprehensions by breaking them into 3 parts: ``body``, ``comp_iter``, and ``ifs``. This is shown below.


:code:`[i*2 for i in range(10) if i>2]` => :code:`[BODY for i in COMP_ITER if IFS]`

Each of these 3 parts may be tested individually using the simple test functions.
For example, in order to test the body of the comprehension above, we could create the following exercise.

.. code:: python

    *** =solution
    ```{python}
    L2 = [i**2 for i in range(0,10) if i>2]
    ```

    *** =sct
    ```{python}
    (Ex().check_list_comp(0)                         # focus on first list comp
           .check_body().test_student_typed('i\*2')  # focus on its body for test
           )
    ```

In the SCT, ``check_list_comp`` gets the first comprehension, and will fail with feedback if no comprehensions were used in th submission code. ``check_body`` gets ``i**2`` in the solution code, and whatever corresponds to BODY in the submission code. 

(Note: the parentheses around the entire statement are just syntactic sugar, to let us chain commands in python without using ``\`` at the end of each line.)

Full Example
~~~~~~~~~~~~

This section expands the above example to run tests on each part: body, iter, and ifs.

.. code-block:: python

    *** =solution
    ```{python}
    L2 = [i*2 for i in range(0,10) if i>2]
    ```

    *** =sct
    ```{python}
    list_comp = Ex().check_list_comp(0, missing_msg="Did you include a list comprehension?")
    list_comp.check_body().test_student_typed('i\*2')
    list_comp.check_iter().has_equal_value()
    list_comp.check_ifs(0).multi([has_equal_value(context_vals=[i]) for i in range(0,10)])
    ```

In this SCT, the first line focuses on the first list comprehension, and assigns it to ``list_comp``, so we can test each part in turn. As a reminder, the code corresponding to each part in the solution code is..

* BODY: ``i**2``
* COMP_ITER: ``range(0,10)``
* IFS: [``i>2``]

Note that IFS is represented as a list, and the index 1 was passed to `check_ifs` because a list comprehension may have multiple if statements. Since the test on BODY, is explained in the [In Brief section](#In_Brief), we will focus on the tests on ITER and and IFS.

check_iter
^^^^^^^^^^^^^^

In the line ``list_comp.check_iter().equal_value()``, ``check_iter`` gets the ITER part in the solution and submission code, while ``has_equal_value`` tells pythonwhat to run those parts and see if they return equal values. Below are example solution and submission codes, with the ITER part they would produce

================ ============================================ ====================
 type              code                                       ITER part
================ ============================================ ====================
 **solution**     :python:`[i*2 for i in range(0,10) if i>2]`  :code:`range(0,10)`
**submission**    :python:`[i*2 for i in range(10) if i>2]`    :code:`range(10)`
================ ============================================ ====================

In this case, ``equal_value`` will run each part, and then confirm that :python:`range(0,10) == range(10)`. For more on functions that run code, like ``has_equal_value`` see [Expressions Tests](processes).

check_ifs
^^^^^^^^^^^^^

The line 

.. code-block:: python
  
  list_comp.check_ifs(0).multi([has_equal_value(context_vals=[i] for i in range(0,10))])

is a doozy, but can be broken down into

.. code-block:: python

  equal_tests = [has_equal_value(context_vals=[i] for i in range(0,10))]    # collection of has_equal_tests
  list_comp.check_ifs(0).multi(equal_tests)                                 # focus on IFS run equal_tests`

In this case ``equal_tests`` is a list of ``has_equal_value`` tests that we'll want to perform. ``check_ifs(1)`` grabs the first IFS part, and ``multi(equal_tests)`` runs each ``has_equal_value`` test on that part. 

Notice that ``has_equal_value`` was given a context_val argument. This is because the list comprehension creates a temporary variable that needs to be defined when we run the IFS code.

================ ============================================== ================ ===============
 type             code                                           IFS part         context value
================ ============================================== ================ ===============
 **solution**     :python:`[i*2 for i in range(0,10) if i>2]`   :python:`if i>2`   ``i`` 
 **submission**   :python:`[j*2 for j in range(0,10) if j>2]`   :python:`if j>2`   ``j`` 
================ ============================================== ================ =============== 

In this case, the context_vals argument is a list of values, with one for each (in this case only a single) context value. In this way, ``has_equal_value`` assigns ``i`` and ``j`` to the same value, before running the IFs part. By creating a list of ``has_equal_tests`` with context vals spanning ``range(0,10)``, we test the IFS across a range of values.

Nested Part Example
~~~~~~~~~~~~~~~~~~~~

Check functions may be combined to focus on parts within parts, such as

.. code:: python

   *** =solution
   ```{python}
   [i*2 if i> 5 else 0 for i in range(0,10)]
   ```

In this case, a representation with the parts in caps and wrapping the inline if expression with ``{BODY=...}`` is

.. code::

   [{BODY=BODY if TEST else ORELSE} for i in ITER]

in order to test running the inline if expression we could go from list_comp => body => if_exp. One possible SCT is shown below.

.. code:: python

   *** =sct
   ```{python}
   (Ex().check_list_comp(0)                     # first comprehension
        .check_body().set_context(i=6)      # comp's body
        .check_if_exp(0).has_equal_value()  # body's inline IFS
        )
   ```

Note that rather than using the ``context_vals`` argument of ``has_equal_value`` we use ``set_context`` to define the context variable (``i`` in the solution code) on the body of the list comprehension. This makes it very clear when the context value was introduced. It is worth pointing out that of the parts a list comprehension has, BODY and IFS, but not ITER have ``i`` as a context value. This is because in python ``i`` is undefined in the ITER part. Context values are listed in the [see cheatsheet below].

Testing only the body of the list comprehension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If we left out the ``check_if_exp`` above, the resulting SCT,

.. code:: python
   
   (Ex().check_list_comp(0).check_body().set_context(i=6)
            #.check_if_exp(1)
            .has_equal_value()
            )

would still run the same code for the solution (the inline if expression), since it's the only thing in the BODY of the list comprehension. However it wouldn't check if an if expression was used, allowing a wider range of passing and failing submissions (for better or worse!). Moreover, `has_equal_value` may be used multiple times during the chaining, as it doesn't change what the focus is.

Helper Functions
----------------

multi
~~~~~~~

.. autofunction:: pythonwhat.check_funcs.multi

Comma separated arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^

For example, this code without multi,

.. code::

    Ex().check_if_exp(0).check_body().has_equal_value()
    Ex().check_if_exp(0).check_test().has_equal_value()


is equivalent to

.. code::

    Ex().check_if_exp(0).multi(
            check_body().has_equal_value(),
            check_test().has_equal_value()
            )

List or generator of subtests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Rather than one or more subtest args, multi can take a single list or generator of subtests.
For example, the code below checks that the body of a list comprehension has equal value
for 10 possible values of the iterator variable, ``i``.

.. code::

    Ex().check_list_comp(0)
        .check_body()
        .multi(set_context(i=x).has_equal_value() for x in range(10))

Chaining off multi
^^^^^^^^^^^^^^^^^^^

Multi returns the same state, or focus, it was given, so whatever comes after multi will run 
the same as if multi wasn't used. For example, the code below tests a list comprehension's body,
followed by its iterator.

.. code::

    Ex().check_list_comp(0) \
        .multi(check_body().has_equal_value()) \
        .check_iter().has_equal_value()


set_context
~~~~~~~~~~~~~

.. autofunction:: pythonwhat.check_funcs.set_context

Sets the value of a temporary variable, such as ``ii`` in the list comprehension below.

.. code::

    [ii + 1 for ii in range(3)]

Variable names may be specified using positional or keyword arguments.

Example
^^^^^^^^

**Solution Code**

.. code::

    ltrs = ['a', 'b']
    for ii, ltr in enumerate(ltrs):
        print(ii)

**SCT**

.. code::

    Ex().check_for_loop(0).check_body() \
        .set_context(ii=0, ltr='a').has_equal_output() \
        .set_context(ii=1, ltr='b').has_equal_output()

Note that if a student replaced `ii` with `jj` in their submission, `set_context` would still work.
It uses the solution code as a reference. While we specified the target variables ``ii`` and ``ltr``
by name in the SCT above, they may also be given by position..

.. code::

    Ex().check_for_loop(0).check_body().set_context(0, 'a').has_equal_output()

Instructor Errors
^^^^^^^^^^^^^^^^^^^

If you are unsure what variables can be set, it's often easiest to take a guess.
When you try to set context values that don't match any target variables in the solution code,
``set_context`` raises an exception that lists the ones available.



with_context
~~~~~~~~~~~~~~

.. autofunction:: pythonwhat.check_funcs.with_context

Runs subtests after setting the context for a ``with`` statement.

This function takes arguments in the same form as ``multi``. 
Note also that ``with_context`` was the default behavior for ``test_with`` in pythonwhat version 1.

Context Managers Explained
^^^^^^^^^^^^^^^^^^^^^^^^^^^

With statements are special in python in that they enter objects called a context manager at the beginning of the block,
and exit them at the end. For example, the object returned by ``open('fname.txt')`` below is a context manager.

.. code::

    with open('fname.txt') as f:
        print(f.read())

This code runs by

1. assigning ``f`` to the context manager returned by ``open('fname.txt')``
2. calling ``f.__enter__()``
3. running the block
4. calling ``f.__exit__()``

``with_context`` was designed to emulate this sequence of events, by setting up context values as in step (1), 
and replacing step (3) with any sub-tests given as arguments.


fail
~~~~~~

.. autofunction:: pythonwhat.check_funcs.fail

Fails. This function takes a single argument, ``msg``, that is the feedback given to the student.
Note that this would be a terrible idea for grading submissions, but may be useful while writing SCTs.
For example, failing a test will highlight the code as if the previous test/check had failed.

As a trivial SCT example,

.. code::

    Ex().check_for_loop(0).check_body().fail()     # fails boo

This can also be helpful for debugging SCTs, as it can be used to stop testing as a given point.

Check Functions
----------------

**Arguments**

* **index**: index or key corresponding to the node or part of interest. 
  This applies to all functions in the **check** column in the table below.
  However, apart from that, it only applies when there is more than one of a specific part to choose from ---
  ``check_ifs``, ``check_args``, ``check_handlers``, and ``check_context``.
  (e.g. ``Ex().check_list_comp(0).check_ifs(0)``)
* **missing_msg**: optional feedback message if node or part doesn't exist.

Note that code in all caps indicates the name of a piece of code that may be inspected using, ``check_{part}``, 
where ``{part}`` is replaced by the name in caps (e.g. ``check_if_else(0).check_test()``).
Target variables are those that may be set using ``set_context``.
These variables may only be set in places where python would set them.
For example, this means that a list comprehension's ITER part has no target variables,
but its BODY does.


+------------------------+------------------------------------------------------+-------------------+
| check                  | parts                                                | target variables  |
+========================+======================================================+===================+
|check_if_else(0)        | .. code::                                            |                   |
|                        |                                                      |                   |
|                        |     if TEST:                                         |                   |
|                        |         BODY                                         |                   |
|                        |     else:                                            |                   |
|                        |         ORELSE                                       |                   |
|                        |                                                      |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_while(0)          |  .. code:: python                                    |                   |
|                        |                                                      |                   |
|                        |      while TEST:                                     |                   |
|                        |          BODY                                        |                   |
|                        |      else:                                           |                   |
|                        |          ORELSE                                      |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_list_comp(0)      | .. code::                                            | ``i``             |
|                        |                                                      |                   |
|                        |     [BODY for i in ITER if IFS[0] if IFS[1]]         |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_generator_exp(0)  | .. code::                                            | ``i``             |
|                        |                                                      |                   |
|                        |     (BODY for i in ITER if IFS[0] if IFS[1])         |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_dict_comp(0)      | .. code::                                            | ``k``, ``v``      |
|                        |                                                      |                   |
|                        |     {KEY : VALUE for k, v in ITER if IFS[0]}         |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_for_loop(0)       | .. code::                                            | ``i``             |
|                        |                                                      |                   |
|                        |     for i in ITER:                                   |                   |
|                        |         BODY                                         |                   |
|                        |     else:                                            |                   |
|                        |         ORELSE                                       |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_try_except(0)     |  .. code:: python                                    | ``e``             |
|                        |                                                      |                   |
|                        |    try:                                              |                   |
|                        |        BODY                                          |                   |
|                        |    except BaseException as e:                        |                   |
|                        |        HANDLERS['BaseException']                     |                   |
|                        |    except:                                           |                   |
|                        |        HANDLERS['all']                               |                   |
|                        |    else:                                             |                   |
|                        |        ORELSE                                        |                   |
|                        |    finally:                                          |                   |
|                        |        FINALBODY                                     |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_with(0)           |   .. code:: python                                   | ``f``             |
|                        |                                                      |                   |
|                        |     with CONTEXT[0] as f1, CONTEXT[1] as f2:         |                   |
|                        |         BODY                                         |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_function_def('f') |   .. code:: python                                   | argument names    |
|                        |                                                      |                   |
|                        |       def f(ARGS[0], ARGS[1]):                       |                   |
|                        |           BODY                                       |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_lambda(0)         | .. code::                                            | argument names    |
|                        |                                                      |                   |
|                        |     lambda ARGS[0], ARGS[1]: BODY                    |                   |
|                        |                                                      |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_function('f', 0)  | .. code::                                            | argument names    |
|                        |                                                      |                   |
|                        |     f(ARGS[0], ARGS[1])                              |                   |
|                        |                                                      |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+

More
------

elif statements
~~~~~~~~~~~~~~~~

In python, when an if-else statement has an elif clause, it is held in the ORELSE part,

.. code:: python

  if TEST:
      BODY
  ORELSE        # elif and else portion

In this sense, an if-elif-else statement is represented by python as nested if-elses. For example, the final ``else`` below

.. code:: python
   
   if x:   print(x)        # line 1
   elif y: print(y)        #  ""  2
   else:   print('none')   #  ""  3
   
can be checked with the following SCT

.. code:: python

   (Ex().check_if_else(0)                    # lines 1-3
        .check_orelse().check_if_else(0)     # lines 2-3
        .check_orelse().has_equal_output()       # line 3
        )


function definition / lambda args
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

the ARGS part in function definitions and lambdas may be selected by position or keyword. 
For example, the arguments `a` and `b` below,

.. code:: python

  def f(a, b=2, *some_name):
      BODY

Could be tested using,

.. code:: python

  Ex().check_function_def('f').multi(
          check_args('a').is_default(),
          check_args('b').is_default().has_equal_value(),
          check_args('*args', 'missing a starred argument!')
          )

Note that ``check_args('*args')`` and ``check_args('**kwargs')`` may be used to test *args, and **kwargs style parameters, regardless of their name in the function definition.

function call args
~~~~~~~~~~~~~~~~~~~

Behind the scenes, ``check_function`` uses the same logic for matching arguments to function signatures as `test_function_v2 <pythonwhat.wiki/test_function_v2.html>`__.
It also has a ``signature`` argument that accepts a custom signature.

Matching Signatures
^^^^^^^^^^^^^^^^^^^^

By default, ``check_function`` tries to match each argument in the function call with the appropriate parameters in that function's call signature.
For example, all the calls to ``f`` below use ``a = 1`` and ``b = 2``.

.. code::

   def f(a, b): pass
   
   f(1, 2)           # by position
   f(a = 1, b = 2)   # by keyword
   f(1, b = 2)       # mixed

However, when testing a submission, we may not care how the argument was specified.

.. code::

   *** =pre_exercise_code
   ```{python}
   def f(a, b): pass
   ```

   *** =solution
   ```{python}
   f(1, b=2)
   ```
   
   *** =sct
   ```{python}
   Ex().check_function('f', 0).check_args('a').has_equal_value()
   ```
   
will pass for all the ways of calling ``f`` listed above.

signature = False
^^^^^^^^^^^^^^^^^^

Setting signature to false, as below, only allows you to check an argument by name, if the name was explicitly specified in the function call.
For example,

.. code::

   *** =solution
   ```{python}
   dict( [('a', 1)],  c = 2)
   ```
   
   *** =sct
   ```{python}
   Ex().check_function('dict', 0, signature=False)\
       .multi(
           check_args(0),     # can only select by position
           check_args('c')    # could use check_args(1)
           )
   ```

Note that here, an argument's position is referring to its position in the function call (not its signature).

Example: testing a list passed as an argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose you want to test the first argument passed to `sum`.
Below, we show how this can be down, using `has_equal_ast()` to check that the abstract syntax trees for the 1st argument match.

.. code:: python

   *** =solution
   ```{python}
   sum([1, 2, 3])
   ```

   *** =sct
   ```{python}
   (Ex().check_function('sum', 0)
        .check_args(0)
        .has_equal_ast("ast fail")                        # compares abstract representations
        .test_student_typed("\[1, 2, 3\]", "typed fail")  # alternative, more rigid test
        )
   ```

Notice that testing the argument is similar to testing, say, the body of an if statement.
In this sense, we could even do deeper checks into an argument.
Below, the SCT verifies that the first argument passed to sum is a list comprehension.

.. code:: python

   *** =solution
   ```{python}
   sum([i for i in range(10)])
   ```

   *** =sct
   ```{python}
   (Ex().check_function('sum', 0)
        .check_args(0)
        .check_list_comp(0)
        .has_equal_ast()
        )
   ```
