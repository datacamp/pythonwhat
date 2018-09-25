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
The ``body`` part that ``check_if_else()`` unearths can be inspected with ``check_body``.

Similar to how ``if`` statements has a ``check_if_else`` associated with it,
all other compound statements have corresponding ``check_`` functions to perform this action of looking up a statement,
and chopping it up into its constituents that can be inspected with ``check_<part>()``:

- ``check_for_loop()`` will look for a ``for`` loop, an break it up into a ``iter``, ``body`` and ``orelse`` part, that can be zoomed in on using ``check_iter()``, ``check_body()`` and ``check_orelse()`` respectively.
- ``check_list_comp()`` will look for a list comprehension and break it up into a ``iter``, ``ifs`` and ``body`` part, that can be zoomed in on using ``check_iter()``, ``check_ifs()`` and ``check_body()`` respectively.
- etc.

For specific examples on checking for loops, list comprehensions, function definitions etc.,
visit the reference. Every function is documented with a full example and corresponding explanation.
All of these examples are specific to a single construct, but of course you can combine things up to crazy levels.

Crazy combo, example 1
======================

Suppose you want to check whether a function definition containing a for loop was coded correctly as follows:

.. code::

    def counter(lst, key):
        count = 0
        for l in lst:
            count += l[key]
        return count

The following SCT would robustly verify this:

.. code::

    Ex().check_function_def('counter').check_correct(
        multi(
            check_call("f([{'a': 1}], 'a')").has_equal_value(),
            check_call("f([{'b': 1}, {'b': 2}], 'b')").has_equal_value()
        ),
        check_body().set_context([{'a': 1}, {'a': 2}], 'a').set_env(count = 0).check_for_loop().multi(
            check_iter().has_equal_value(),
            check_body().set_context({'a': 1}).has_equal_value(name = 'count')
        )
    )

Some notes about this SCT:

- ``check_correct()`` is used so the body is not further checked if calling the function in different ways produces the same value in both student and solution process.
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
|check_class_def('f')    | .. code::                                            |                   |
|                        |                                                      |                   |
|                        |       class KLS(BASES[0], BASES[1]):                 |                   |
|                        |           BODY                                       |                   |
|                        |                                                      |                   |
+------------------------+------------------------------------------------------+-------------------+
