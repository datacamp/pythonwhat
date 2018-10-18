Tutorial
--------

pythonwhat uses the ``.`` to 'chain together' SCT functions. Every chain starts with the ``Ex()`` function call, which holds the exercise state.
This exercise state contains all the information that is required to check if an exercise is correct, which are:

+ the student submission and the solution as text, and their corresponding parse trees.
+ a reference to the student process and the solution process.
+ the output and errors that were generated when executing the student code.

As SCT functions are chained together with ``.``, the ``Ex()`` exercise state is copied and adapted into 'sub states' to zoom in on particular parts of the state.
Before this terminology blows your brains out, let's have a look at some basic examples.

Example 1: output
=================

Assume we want to robustly check whether a student correctly printed out a sentence:

.. code::

    print('hi, my name is DataCamp')

The following SCT would do that:

.. code::

    Ex().has_output(r'[H|h]i,\s+my name is \w+')

Let's see what happens when the SCT runs:

- ``Ex()`` returns the 'root state', which considers the entire student submission and solution code,
  a reference to the student and solution process, and the output and errors generated.
- ``has_output(r'<regex>')`` fetches the output the student generated from the root state and checks whether it can match the specified regular expression against it.

  + If the student had submitted ``print('Hi, my name is Filip')``, the regex will match, the SCT will pass, and the student is presented with a congratulatory message.
  + If the student had submitted ``print('Hi,mynameis'_``, the regex will not have found a match, the SCT will fail, and pythonwhat will automatically generate a feedback message.

Example 2: function call
========================

Assume we want to check whether a student correctly called the ``DataFrame`` function of the ``pandas`` package.

.. code::

    import pandas as pd
    pd.DataFrame([1, 2, 3])

The following SCT would do that:

.. code::

    Ex().check_function('pandas.DataFrame').check_args('data').has_equal_value()

Assume the student submits the following (incorrect) script:

.. code::

    import pandas as pd
    pd.DataFrame([1, 2, 3, 4])

Let's see what happens when the SCT runs:

- ``Ex()`` returns the 'root state', which considers the entire student submission and solution code:

  .. code::

      # solution
      import pandas as pd
      pd.DataFrame([1, 2, 3])

      # student
      import pandas as pd
      pd.DataFrame([1, 2, 3, 4])

- ``check_function('pandas.DataFrame')`` continues from the root state (considering the entire student submission and solution),
  and looks for a call of ``pd.DataFrame`` in both. It finds them, and 'zooms in' on the arguments.
  In simplified terms, this is the state that ``check_function()`` produces:

  .. code::

      # solution args
      { "data": [1, 2, 3] }

      # student arg
      { "data": [1, 2, 3, 4] }

- ``check_args('data')`` continues from the state produced by ``check_function()`` and looks for the ``"data"`` argument in both the student and solution arguments.
  It finds it in both and produces a state that zooms in on the expression used to specify this argument:

  .. code::

      # solution expression for data arg
      [1, 2, 3]

      # student expression for data arg
      [1, 2, 3, 4]

- Finally, ``has_equal_value()`` takes the state produced by ``check_args()``,
  executes the student and solution expression in their respective processes, and verifies if they give the same result.
  In this example, the results of the expressions don't match: a 3-element array vs a 4-element array.
  Hence, the SCT fails and automatically generates a meaningful feedback message.

Example 3: if statement
=======================

As a more advanced example, assume we want to check that the student coded up an `if` statement correctly:

.. code::

    x = 4
    if x > 0:
        print("x is strictly positive")

The following SCT would do that:

.. code::

    Ex().check_if_else().multi(
        check_test().has_code(r'x\s+>\s+0'), # chain A
        check_body().check_function('print').check_args(0).has_equal_value() # chain B
        )

Notice how this time, ``multi()`` is used to have the SCT chains 'branch out';
both ``check_body()`` and ``check_test()`` continue from the state produced by ``check_if_else()``.

Case 1
~~~~~~

In the first case, assume the following incorrect student submission:

.. code::

    x = 4
    if x < 0:
        print("x is negative")

In chain A, this is what happens:

- ``check_if_else()`` considers the entire submission received from ``Ex()``,
  looks for the first if-else statement in both student and solution code,
  and produces a child state that zooms in on onlty these ``if`` statements:

  .. code::

      # solution
      if x > 0:
          print("x is strictly positive")

      # student
      if x < 0:
          print("x is negative")

- ``check_test()`` considers the state above produced by ``check_if_else()``
  and produces a child state that zooms in on the condition parts of the ``if`` statements:

  .. code::

      # solution
      x > 0

      # student
      x < 0

- ``has_code()`` considers the state above produced by ``check_test()``
  and tries to match the regexes to the ``x < 0`` student snippet. The regex does not match, so the test fails.

Case 2
~~~~~~

Assume now that the student corrects the mistake and submits the following (which is still not correct):

.. code::

    x = 4
    if x > 0:
        print("x is negative")

Chain A will go through the same steps and will pass this time as ``x > 0`` in the student submission now matches the regex. In Chain B:

- ``check_body()`` considers the state produced by ``check_if_else()``, and produces a child state that zooms in on the body parts of the ``if`` statements:

  .. code::

      # solution
      print("x is strictly positive")

      # student
      print("x is negative")

- ``check_function()`` considers the state above produced by ``check_if_else()``, and tries to find the function ``print()``.
  Next, it produces a state that refers to the different function arguments and the expressions used to specify them:

  .. code::

      # solution
      { "value": "x is strictly positive" }

      # student
      { "value": "x is negative" }
  
- ``check_args(0)`` looks for the first argument in the state produced by ``check_function()`` and produces a child state that zooms in on the expressions for the ``value`` argument:

  .. code::

      # solution
      "x is strictly positive"

      # student
      "x is negative"
  
- Finally, ``has_equal_value()`` takes the state produced by ``check_args()``,
  executes the student and solution expression in their respective processes, and verifies if they give the same result.
  The result of executing ``"x is strictly positive"`` and ``"x is negative"`` don't match so the SCT fails.

.. caution::

    We strongly advise against using ``has_code()`` to verify the correctness of excerpts of a student submission.
    Visit the 'checking compount statements' article to take a deeper dive.


What is good feedback?
======================

For larger exercises, you'll often want to be flexible: if students get the end result right, you don't want to be picky about how they got there.
However, when they do make a mistake, you want to be specific about the mistake they are making. In other words, a good SCT is robust against different ways of solving a problem, but specific when something's wrong.

These seemingly conflicting requirements can be satisfied with ``check_correct()``. It is an **extremely powerful function** that should be used whenever it makes sense.
The `Make your SCT robust <make_your_sct_robust.html>`_ article is highly recommended reading.

For other guidelines on writing good SCTs, check out the 'How to write good SCTs' section on DataCamp's `general SCT documentation page <https://instructor-support.datacamp.com/courses/course-development/submission-correctness-tests>`_.

