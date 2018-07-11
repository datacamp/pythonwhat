Checking through string matching
--------------------------------

has_code
========

With ``has_code()``, you can look through the student's submission to find a match with a search pattern you have specified.

- If ``pattern = True``, the default, the ``text`` is used as a regular expression to match against.
- If ``pattern = False``, ``has_code()`` will consider the text you pass as an actual string that has to be found exactly.

.. caution::

    It is often tempting to use ``has_code()`` as it's straightforward to use,
    but **you should avoid using this function**, as it imposes severe restrictions on how a student can solve an exercise.
    Often, there are many different ways to solve an exercise. Unless you have a very advanced regular expression,
    ``has_code()`` will not be able to accept all these different approaches.
    Always think about better ways to test a student submission before you resort to ``has_code()``.

Take the following example:

.. code::

    # solution
    s = sum(range(10))

    # sct that checks whether sum(range( is in the code
    Ex().has_code("sum\s*\(\s*range\s*\(", not_typed_msg="You didn't use ``range()`` inside ``sum()``.")

We also used ``not_typed_msg`` here to specify the feedback message shown to the student if ``has_code()`` doesn't pass.

has_equal_ast
=============

AST stands for `abstract syntax tree`; it is a way of representing the high-level structure of python code.
As the name suggests, ``has_equal_ast()`` verifies whether the code portion under consideration has the same AST representation in student and solution.
Compared to ``has_code()``, it is more robust to small syntactical details that are equivalent.

- Quotes: the AST for ``x = "1"`` or ``x = '1'`` will be the same.
- Parentheses: Grouping by parentheses produces the same AST, when the same statement would work the same without them.
  ``(True or False) and True``, and ``True or False and True``, are the same due to operator precedence.
- Spacing: ``x     = 1`` or ``x = 1`` have the same AST.

The AST does **not** represent is values that are found through evaluation. For example, the first item in the list in

.. code::

    x = 1
    [x, 2, 3]

and

.. code::

    [1, 2, 3]

Is not the same. In the first case, the AST represents that a variable ``x`` needs to be evaluated in order to find out what its value is.
In the second case, it just represents the value ``1``.

.. caution::

    Note that it is `not` a good idea to use ``Ex().has_equal_ast()``, effectively comparing the entire solution with the entire student submission.
    It `is` a good idea, however, to use `has_equal_ast` for checking small excerpts of code when checking compound statements,
    for example to inspect the test part of an ``if`` statement.

As an example, consider this example that checks whether a student correclty coded a condition in a for loop (note that there are better ways to check this with ``has_equal_value()``!):

.. code::

    # solution
    x = 3
    if x % 2 == 0:
        print('x is even')

    # sct
    Ex().check_if_else().multi(
        check_test().has_equal_ast(),
        check_body().has_equal_output()
    )

    # passing submission 1
    x = 3
    if (x % 2 == 0):
        print('x is even')

    # passing submission 2
    x = 3
    if x%2==0:
        print('x is even')

    # failing submission
    x = 3
    if 0 == x % 2:
        print('x is even')

Here, the ``Ex().check_if_else().check_test()`` chain zooms in on the test part of the if statement.
With ``has_equal_ast()`` you are checking whether the AST representation of the test in the solution, ``x % 2 == 0`` is also found in the test specified by the student.
Notice that ``has_equal_ast()`` is not robust against a simple switching the order of the operands of the ``==`` operator.
A better SCT here would not use string (or AST) matching in the first place and rerun the test for different values of ```x``:

.. code::

    Ex().check_if_else().multi(
        check_test().multi(
            set_env(x = 3).has_equal_value(),
            set_env(x = 4).has_equal_value(),
            set_env(x = 4).has_equal_value()
        ),
        check_body().has_equal_output()
    )