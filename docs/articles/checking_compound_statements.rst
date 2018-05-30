Checking compound statements
----------------------------

.. role:: python(code)
   :language: python

As described in the `official Python documentation <https://docs.python.org/3/reference/compound_stmts.html>`_, 
*compound statements contain (groups of) other statements; they affect or control the execution of those other statements in some way.
In general, compound statements span multiple lines, although in simple incarnations a whole compound statement may be contained in one line.*

``if``, ``while``, ``for``, ``try``, and ``with`` statements are all examples of compounds statements, and ``pythonwhat`` contains functionality to check all of these,
- as well as function definitions, list and dictionary comprehensions, generator expressions and lambda functions - in a consistent fashion.

Inner workings
==============

The ``if`` statement example in the `Syntax article <syntax.html>`_ describes how different ``check_`` functions zoom into a specific part of a submission and solution,
producing a child state, to which additional SCT functions can be chained.

The  ``check_if_else()`` function scanned the code for an ``if`` statement,
and broke it into three parts: a ``test``, the ``body`` and the ``orelse`` part;
the former two were dived into with the SCT functions ``check_test`` and ``check_body``.
Notice that the naming is consistent: the ``test`` part that ``check_if_else()`` surfaces can be inspected with ``check_test()``.
The ``body`` part that ``check_if_else()`` unearths can be inspected with ``check_ifs``.

Similar to how ``if`` statements has a ``check_if_else`` associated with it, all other compound statements have corresponding ``check_`` functions to perform this action of looking up a statement, and chopping it up into its constituents that can be inspected with ``check_<part>()``:

- ``check_for()`` will look for a ``for`` loop, an break it up into a ``iter``, ``body`` and ``orelse`` part, that can be zoomed in on using ``check_iter()``, ``check_body()`` and ``check_orelse()`` respectively.
- ``check_list_comp()`` will look for a list comprehension and break it up into a ``iter``, ``ifs`` and ``body`` part, that can be zoomed in on using ``check_iter()``, ``check_ifs()`` and ``check_body()`` respectively.
- etc.

The table below summarizes all compound statements that ``pythonwhat`` supports.
Code in all caps indicates the name of a piece of code that may be inspected using, ``check_{part}``, 
where ``{part}`` is replaced by the name in caps (e.g. ``check_if_else(0).check_test()``). The concept of target variables will be explained later in this article.

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
|check_while(0)          | .. code::                                            |                   |
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
|check_for_loop(0)       | .. code::                                            | ``i``, ``j``      |
|                        |                                                      |                   |
|                        |     for i, j in ITER:                                |                   |
|                        |         BODY                                         |                   |
|                        |     else:                                            |                   |
|                        |         ORELSE                                       |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_try_except(0)     | .. code::                                            | ``e``             |
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
|check_with(0)           | .. code::                                            | ``f``             |
|                        |                                                      |                   |
|                        |     with CONTEXT[0] as f1, CONTEXT[1] as f2:         |                   |
|                        |         BODY                                         |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_function_def('f') | .. code::                                            | argument names    |
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

Advanced part checking
======================

Let's recap the ``if`` statement example in the `Syntax article <syntax.html>`_:

.. code::

    # solution
    x = 4
    if x > 0:
        print("x is positive")
    
    # sct
    Ex().check_if_else().multi(
        check_test().has_code(/x\s+>\s+0/), # chain A
        check_body().check_function('print', 0).check_args('value').has_equal_value() # chain B
        )

It manages to check whether the student specified an ``if`` statement, but the check of the ``test`` part is not very robust.
The SCT would not accept a submission that contains ``0 < x`` in the test.

To increase robustness, ``pythonwhat`` features functionality to rerun pieces of the student and solution code,
and then check the resulting value, printed output, or errors they produce.

As an example, consider this improved SCT of the example above:

.. code::

    # sct
    Ex().check_if_else().multi(
        check_test().has_equal_value(), # chain A
        check_body().check_function('print', 0).check_args('value').has_equal_value() # chain B
    )

Chain A has been updated to use ``has_equal_value()`` instead of ``has_code()``.
``has_equal_value()`` will execute the ``test`` portion of the ``if`` statement in both
the student and solution coding process and will compare their results, making it more robust.
If the student sets ``x = 4`` and the test condition to ``x > 0`` (or ``0 < x``), it will evaluate to ``True``, the same as the solution, and ``has_equal_value()`` will pass.
If the student sets ``x = 4`` and the test condition to ``x < 0``, it will evaluate to ``False``, different from the solution, and ``has_equal_value()`` will fail.

Things could be further improved though. If the student sets ``x = 4`` and the test to ``x > 2``,
it will still evaluate to ``True`` and ``has_equal_value()`` will still pass. To solve this, ``pythonwhat`` allows you to rerun the parts in different situations:

.. code::

    # sct
    Ex().check_if_else().multi(
        check_test().multi(
            has_equal_value(), # chain A1
            has_equal_value(extra_env = {'x': -1}), # chain A2
            has_equal_value(extra_env = {'x': 0}), # chain A3
            has_equal_value(extra_env = {'x': 1}) # chain A4
            ) 
        check_body().check_function('print', 0).check_args('value').has_equal_value() # chain B
        )   

    # sct, short version
    Ex().check_if_else().multi(
        check_test().multi([ has_equal_value(extra_env = {'x': i}) for i in [4, -1, 0, 1] ]), # chain A
        check_body().check_function('print', 0).check_args('value').has_equal_value() # chain B
        )   

Through ``extra_env``, we're temporarily overriding the value of ``x`` in the coding process before rerunning the piece of code.
This is done for both student and solution process, and again results are compared. This adds robustness.

Aside from ``has_equal_value()`` you can also use ``has_equal_output()`` and ``has_equal_error()`` to state your expectations about pieces of code.
For more information about these functions and how they can be tweaked, check out the `Expression tests article <expression-tests.html>`_.

.. note::

    Notice that ``has_equal_value()`` is also being used in the context of checking objects and function arguments.
    When checking objects, ``has_equal_value()`` is executing the expression ``<var_name>`` and comparing the result.
    When checking function arguments, ``has_equal_value()`` executes the expression that specifies an argument.
    Instead of requiring dedicated functions, ``has_equal_value()`` can be consistently reused in this context.

Context values
==============

Most compound statements build up a local context when executed.
To illustrate this point, have a look at this ``for`` loop example that iterates over dictionaries:

.. code::

    # solution
    my_dict = {'a': 1, 'b': 2}
    for key, value in my_dict.items():
        print(key + " - " + str(value))

    # sct
    Ex().check_object('my_dict').has_equal_value()
    Ex().check_for_loop(0).multi(
        check_iter().has_equal_value(),                                      # run iterator (my_dict.items())
        check_body().set_context(key = 'c', value = 3).has_equal_output()    # run print statement
    )

The ``for`` loop introduces two context values, ``key`` and ``value``, that are only specified at run-time in the context of the for loop.
With ``set_context()``, these context values can be specified before using a ``has_equal_x()`` function.

Assuming the student coded the function in the exact same way as the solution, the following things happen:

- The ``check_object()`` chain verifies that ``my_dict`` is properly initialized.
- ``check_for_loop()`` zooms in on the ``for`` loop, and makes its parts available for further checking.
- The ``check_iter()`` chain runs the code for the iterator, ``my_dict.items()``, and compares the values they return.
- The ``check_body()`` chain runs the code in the for loop body, ``print(key + " - " + str(value))``, and compares outputs. 
  Since this code may use variables the for loop defined, ``key`` and ``value``, we need to define them using ``set_context``.

The table introduced earlier includes a column that shows which compound statements produces which context values.

To learn more about context values, and how to set them (both by name and by position), check out the `Expression tests article <expression-tests.html>`_.

Nested Part Checking
====================

Check functions may be combined to focus on parts within parts, such as

.. code::

   [i*2 if i> 5 else 0 for i in range(0,10)]

In this case, a representation with the parts in caps and wrapping the inline if expression with ``{BODY=...}`` is

.. code::

   [{BODY=BODY if TEST else ORELSE} for i in ITER]

in order to test running the inline if expression we could go from ``list_comp => body => if_exp``. One possible SCT is shown below.

.. code::

   (Ex().check_list_comp(0)                 # first comprehension
        .check_body().set_context(i=6)      # comp's body
        .check_if_exp(0).has_equal_value()  # body's inline IFS
        )

Note that we use ``set_context`` to define the context variable (``i`` in the solution code) on the body of the list comprehension.
This makes it very clear when the context value was introduced.
It is worth pointing out that of the parts a list comprehension has, BODY and IFS, but not ITER have ``i`` as a context value.
This is because in python ``i`` is undefined in the ITER part.


Special cases
=============

elif statements
~~~~~~~~~~~~~~~

In Python, when an if-else statement has an elif clause, it is held in the ORELSE part,

.. code::

  if TEST:
      BODY
  ORELSE        # elif and else portion

In this sense, an if-elif-else statement is represented by python as nested if-elses. For example, the final ``else`` below

.. code::
   
   if x:   print(x)        # line 1
   elif y: print(y)        #  ""  2
   else:   print('none')   #  ""  3
   
can be checked with the following SCT

.. code::

   (Ex().check_if_else(0)                    # lines 1-3
        .check_orelse().check_if_else(0)     # lines 2-3
        .check_orelse().has_equal_output()       # line 3
        )


function definition / lambda args
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``ARGS`` part in function definitions and lambdas may be selected by position or keyword. 
For example, the arguments ``a`` and ``b`` below,

.. code::

  def f(a, b=2, *some_name):
      BODY

Could be tested using,

.. code::

  Ex().check_function_def('f').multi(
          check_args('a').is_default(),
          check_args('b').is_default().has_equal_value(),
          check_args('*args', 'missing a starred argument!')
          )

Note that ``check_args('*args')`` and ``check_args('**kwargs')`` may be used to test ``*args``, and ``**kwargs`` style parameters, regardless of their name in the function definition.

