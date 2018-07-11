Checking compound statements
----------------------------

As described in the `official Python documentation <https://docs.python.org/3/reference/compound_stmts.html>`_, 
*compound statements contain (groups of) other statements; they affect or control the execution of those other statements in some way.
In general, compound statements span multiple lines, although in simple incarnations a whole compound statement may be contained in one line.*

``if``, ``while``, ``for``, ``try``, and ``with`` statements are all examples of compounds statements, and pythonwhat contains functionality to check all of these,
- as well as function definitions, list and dictionary comprehensions, generator expressions and lambda functions - in a consistent fashion.

Inner workings
==============

The ``if`` statement example in the tutorial describes how different ``check_`` functions zoom into a specific part of a submission and solution,
producing a child state, to which additional SCT functions can be chained. The  ``check_if_else()`` function scanned the code for an ``if`` statement,
and broke it into three parts: a ``test``, the ``body`` and the ``orelse`` part; the former two were dived into with the SCT functions ``check_test`` and ``check_body``.
Notice that the naming is consistent: the ``test`` part that ``check_if_else()`` surfaces can be inspected with ``check_test()``.
The ``body`` part that ``check_if_else()`` unearths can be inspected with ``check_ifs``.

Similar to how ``if`` statements has a ``check_if_else`` associated with it,
all other compound statements have corresponding ``check_`` functions to perform this action of looking up a statement,
and chopping it up into its constituents that can be inspected with ``check_<part>()``:

- ``check_for_loop()`` will look for a ``for`` loop, an break it up into a ``iter``, ``body`` and ``orelse`` part, that can be zoomed in on using ``check_iter()``, ``check_body()`` and ``check_orelse()`` respectively.
- ``check_list_comp()`` will look for a list comprehension and break it up into a ``iter``, ``ifs`` and ``body`` part, that can be zoomed in on using ``check_iter()``, ``check_ifs()`` and ``check_body()`` respectively.
- etc.

Examples
========

``check_if_else()``
~~~~~~~~~~~~~~~~~~~

Let's recap the ``if`` statement example from the tutorial article:

.. code::

    # solution
    x = 4
    if x > 0:
        print("x is strictly positive")
    
    # sct
    Ex().check_if_else().multi(
        check_test().has_code(/x\s+>\s+0/), # chain A
        check_body().check_function('print', 0).check_args('value').has_equal_value() # chain B
    )

It checks whether the student specified an ``if`` statement, but the check of the ``test`` part is not very robust.
The SCT would not accept a submission that contains ``0 < x`` in the test.

To increase robustness, pythonwhat features functionality to rerun pieces of the student and solution code,
and then check the resulting value, printed output, or errors they produce.

Consider the same solution, an example submission, and a better SCT:

.. code::

    # solution
    x = 4
    if x > 0:
        print("x is strictly positive")

    # sct
    Ex().check_if_else().multi(
        check_test().multi(
            set_env(x = -1).has_equal_value(), # chain A1
            set_env(x =  1).has_equal_value(), # chain A2
            set_env(x =  0).has_equal_value()  # chain A3
        ),
        check_body().check_function('print', 0).check_args('value').has_equal_value() # chain B
    )

    # example student submission
    x = 4
    if x >= 0:
        print("x is strictly positive")


In this SCT, `chain A` has been made more advanced:

- As explained previously, ``check_test()`` zooms on the 'test portions' of the if statement in both student (``x >= 0``) and solution code (``x > 0``)
- Instead of ``has_code()``, we are using a series of ``set_env().has_equal_value()`` calls.
  ``set_env()`` will temporarily override the value of ``x`` in the student/solution process,
  and ``has_equal_value()`` will re-execute the pieces of code that are zoomed in on, and compare the results.

  + chain A1 re-executes ``x >= 0`` in the student process and ``x > 0`` in the solution process when ``x`` is equal to ``-1``, and checks if the results are the same, which they are: they both evaluate to ``False``.
  + chain A2 re-executes ``x >= 0`` in the student process and ``x > 0`` in the solution process when ``x`` is equal to ``1``, and checks if the results are the same, which they are: they both evaluate to ``True``.
  + chain A3 re-executes ``x >= 0`` in the student process and ``x > 0`` in the solution process when ``x`` is equal to ``1``, and checks if the results are the same.
    They are not: the student expression evaluates to ``False``, while the solution expressione evaluates to ``True``.

With this example student submission, the SCT will fail and pythonwhat will automatically generate a meaningful feedback message.
However, because we are not merely string-matching the SCT allows for much more ways of (correctly solving) the problem that would be hard to cater for with ``has_code()``:

.. code::

    # example student submission (passing)
    x = 4
    if x > 0:
        print("x is strictly positive")

    # example student submission (passing)
    x = 4
    if 0 < x:
        print("x is strictly positive")

.. note::

    Notice that ``has_equal_value()`` is also used in the context of checking objects and function arguments.
    When checking objects, ``has_equal_value()`` is executing the expression ``<var_name>`` and comparing the result.
    When checking function arguments, ``has_equal_value()`` executes the expression that specifies an argument.
    They are different applications of the same concept: zooming in on a part of the student/solution submission,
    rerunning the expressions and comparing the results.


``check_for()``
~~~~~~~~~~~~~~~

The following example checks whether the student properly iterates over a dictionary and does the appropriate printouts:

.. code::

    # solution
    my_dict = {'a': 1, 'b': 2}
    for key, value in my_dict.items():
        print(key + " - " + str(value))

    # sct
    Ex().check_object('my_dict').has_equal_value()
    Ex().check_for_loop().multi(
        check_iter().has_equal_value(),
        check_body().multi(
            set_context('a', 1).has_equal_output(),
            set_context('b', 2).has_equal_output()
        )
    )

Unlike the ``if`` statement, the ``for`` loop introduces two context values, ``key`` and ``value``.
pythonwhat treats them different from regular variables like ``x`` in the previous example to be robust to students using different names for these context variables, 
Similar to ``set_env()``, you can now use ``set_context()`` to temporarily override the values of these context variables.
Next, you can use ``has_equal_x()`` like before to rerun the body of the for loop for different situations.

- The ``check_object()`` chain verifies that ``my_dict`` is properly initialized.
- ``check_for_loop()`` zooms in on the ``for`` loop, and makes its parts available for further checking.
- ``check_iter()`` zooms in on the iterator part of the for loop, ``my_dict.items()`` in the solution.
    
  + ``has_equal_value()`` re-executes the expressions specified by student and solution and compares their results.

- ``check_body()`` zooms in on the body part of the for loop, ``print(key + " - " + str(value))``:

  + Similar to ``set_env()``, we now use ``set_context()`` to temporarily override the values of the context variables ``key`` and ``value``, in this order.
    Notice that the context values are not specified by name, this is on purpose.
  + ``has_equal_output()`` re-executes the entire for loop body and captures the output this generates. It does this for both the student and solution body, and checks if the outputs are equal.

Because pythonwhat treats context values differently from normal variables and we're not specifying the variables by name in ``set_context()``,
we can make the SCT robust against submissions that code the correct logic, but use different names for the context values.
Consider the following student submissions that would also pass the SCT:

.. code::

    # passing submission 1
    my_dict = {'a': 1, 'b': 2}
    for k, v in my_dict.items():
        print(k + " - " + str(v))

    # passing submission 2
    my_dict = {'a': 1, 'b': 2}
    for first, second in my_dict.items():
        mess = first + " - " + str(second) 
        print(mess)


``check_function_def()``
~~~~~~~~~~~~~~~~~~~~~~~~

The following example checks whether students correctly defined their own function:

.. code::

    # solution
    def shout_echo(word1, echo=1):
        echo_word = word1 * echo
        shout_words = echo_word + '!!!'
        return shout_words

    # sct
    Ex().check_function_def('shout_echo').test_correct(
        multi(
            call(['hey', 3], 'value'),
            call(['hi', 2], 'value'),
            call(['hi'], 'value')
        ),
        check_body().set_context('test', 1).multi(
            has_equal_value(name = 'echo_word'),
            has_equal_value(name = 'shout_words')
        )
    )

Here:

- ``check_function_def()`` zooms in on the function definition of ``shout_echo`` in both student and solution code (and process)
- ``test_correct()`` is used to
  + First check whether the function gives the correct result when called in different ways (through ``call()``).
  + Only if these 'function unit tests' don't pass, `test_correct()` will run the `check_body()` chain that dives deeper into the 
  function definition body. This chain sets the context variables - ``word1`` and ``echo``, the arguments of the function - to
  the values ``'test'`` and ``1`` respectively, again while being agnostic to the actual name of these context variables.

Notice how ``test_correct()`` is used to great effect here: why check the function definition internals if the I/O of the function works fine?
Because of this construct, all the following submissions will pass the SCT:

.. code::

    # passing submission 1
    def shout_echo(w, e=1):
        ew = w * e
        return ew + '!!!'

    # passing submission 2
    def shout_echo(a, b=1):
        return a * b + '!!!'

elif statements
~~~~~~~~~~~~~~~

In Python, when an if-else statement has an ``elif`` clause, it is held in the `orelse` part.
In this sense, an if-elif-else statement is represented by python as nested if-elses. More specifically, this if-else statement:

.. code::

    if x:
        print(x)
    elif y:
        print(y)
    else:
        print('none')

Is syntactically equivalent to:

.. code::

    if x:
        print(x)
    else:
        if y:
            print(y)
        else:
            print('none')

The second representation has to be followed when writing the corresponding SCT:

.. code::

   Ex().check_if_else() \
       .check_orelse().check_if_else() \
       .check_orelse().has_equal_output()


Crazy combo
~~~~~~~~~~~

Suppose you want to check whether a function definition containing a for loop was coded correctly. Here's an example:

.. code::

    # solution
    def counter(lst, key):
        count = 0
        for l in lst:
            count += l[key]
        return count

    # sct that robustly checks this
    Ex().check_function_def('counter').test_correct(
        multi(
            call([[{'a': 1}], 'a'], 'value'),
            call([[{'b': 1}, {'b': 2}], 'b'], 'value')
        ),
        check_body().set_context([{'a': 1}, {'a': 2}], 'a').set_env(count = 0).check_for_loop().multi(
            check_iter().has_equal_value(),
            check_body().set_context({'a': 1}).has_equal_value(name = 'count')
        )
    )

Some notes about this SCT:

- ``test_correct()`` is again used so the body is not further checked if calling the function in different ways produces the same value in both student and solution process.
- ``set_context()`` is used twice. Once to set the context variables introduced by the function definition, and once to set the context variable introducted by the for loop.
- ``set_env()`` had to be used to initialize ``count`` to a variable that was scoped only to the function definition.


Overview of all supported compound statements
=============================================

The table below summarizes all checks that pythonwhat supports to test compound statements.

- Code in all caps indicates the name of a piece of code that may be inspected using ``check_{part}``, 
  where ``{part}`` is replaced by the name in caps (e.g. ``check_if_else().check_test()``).
- If the statement produces context variables, these are referred to in the parts column and listed
  in the context variables column. The names used are just to refer to which context variable comes
  from where; you are totally free in naming your context variables.


+------------------------+------------------------------------------------------+-------------------+
| check                  | parts                                                | context variables |
+========================+======================================================+===================+
|check_if_else()         | .. code::                                            |                   |
|                        |                                                      |                   |
|                        |     if TEST:                                         |                   |
|                        |         BODY                                         |                   |
|                        |     else:                                            |                   |
|                        |         ORELSE                                       |                   |
|                        |                                                      |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_while()           | .. code::                                            |                   |
|                        |                                                      |                   |
|                        |      while TEST:                                     |                   |
|                        |          BODY                                        |                   |
|                        |      else:                                           |                   |
|                        |          ORELSE                                      |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_list_comp()       | .. code::                                            | ``i``             |
|                        |                                                      |                   |
|                        |     [BODY for i in ITER if IFS[0] if IFS[1]]         |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_generator_exp()   | .. code::                                            | ``i``             |
|                        |                                                      |                   |
|                        |     (BODY for i in ITER if IFS[0] if IFS[1])         |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_dict_comp()       | .. code::                                            | ``k``, ``v``      |
|                        |                                                      |                   |
|                        |     {KEY : VALUE for k, v in ITER if IFS[0]}         |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_for_loop()        | .. code::                                            | ``i``, ``j``      |
|                        |                                                      |                   |
|                        |     for i, j in ITER:                                |                   |
|                        |         BODY                                         |                   |
|                        |     else:                                            |                   |
|                        |         ORELSE                                       |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
|check_try_except()      | .. code::                                            | ``e``             |
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
|check_with()            | .. code::                                            | ``f``             |
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
|check_lambda_function() | .. code::                                            | argument names    |
|                        |                                                      |                   |
|                        |     lambda ARGS[0], ARGS[1]: BODY                    |                   |
|                        |                                                      |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
