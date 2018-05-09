Checking through string matching
--------------------------------

test_student_typed
==================

With ``test_student_typed()``, you can look through the student's submission to find a match with a search pattern you have specified.
If ``pattern = True``, the default, the ``text`` is used as a regular expression to match against.
If ``pattern = False``, ``test_student_typed()`` will consider the text you pass as an actual string that has to be found exactly.


.. note::

    It is often tempting to use ``test_student_typed()`` as it's straightforward to use,
    but **you should avoid using this function**, as it imposes severe restrictions on how a student can solve an exercise.
    Often, there are many different ways to solve an exercise. Unless you have a very advanced regular expression,
    ``test_student_typed()`` will not be able to accept all these different approaches.
    **Always think about better ways to test a student submission before you resort to ``test_student_typed()``**.

Suppose the solution of an exercise looks like this:

.. code::

    # Calculate the sum of all single digit numbers and assign the result to 's'
    s = sum(range(10))

The following SCT tests whether the student typed ``"sum(range("``:

.. code::

    test_student_typed("sum(range(", pattern = False)

Notice that we set ``pattern`` to ``False``, this will cause ``test_student_typed()`` to search for the pure string, no patterns are used.
This SCT is not that robust though, it won't accept something like ``sum(  range(10) )``. This is why we should almost always use [regular expressions](https://docs.python.org/3.5/library/re.html) in ``test_student_typed()``:

.. code::

    test_student_typed("sum\s*\(\s*range\s*\(", not_typed_msg="You didn't use ``range()`` inside ``sum()``.")
    success_msg("Great job!")

We also used ``not_typed_msg`` here, which will control the feedback given to the student when ``test_student_typed()`` doesn't pass.

has_equal_ast
=============

AST stands for `abstract syntax tree`; it is a way of representing the high-level structure of python code. As the name suggests, ``has_equal_ast()`` verifies whether the code portion under consideration has the same AST representation in student and solution.
Compared to ``test_student_typed()``, it is more robust to small syntactical details that are equivalent. 

Note that it is `not` a good idea to use ``Ex().has_equal_ast()``, effectively comparing the entire solution with the entire student submission.
It `is` a good idea, however, to use `has_equal_ast` for checking small excerpts of code when checking compound statements,
for example to inspect the test part of an ``if`` statement.

Example: quotes
~~~~~~~~~~~~~~~

Whether you use the concrete syntax ``x = "1"`` or ``x = '1'``, the abstract syntax is the same: x is being assigned to the string "1".

Example: parenthesis
~~~~~~~~~~~~~~~~~~~~

Grouping by parentheses produces the same AST, when the same statement would work the same without them.
For example, ``(True or False) and True``, and ``True or False and True``, are the same due to operator precedence.

Example: spacing
~~~~~~~~~~~~~~~~

The same holds for different types of spacing that essentially specify the same statement: ``x     = 1`` or ``x = 1``.

Caveat: evaluating
~~~~~~~~~~~~~~~~~~

What the AST doesn't represent is values that are found through evaluation. For example, the first item in the list in

.. code::

    x = 1
    [x, 2, 3]

and

.. code::

    [1, 2, 3]

Is not the same. In the first case, the AST represents that a variable ``x`` needs to be evaluated in order to find out what its value is.
In the second case, it just represents the value ``1``.