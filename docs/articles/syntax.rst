Syntax
------

.. role:: python(code)
   :language: python

``pythonwhat`` uses the ``.`` to 'chain together' SCT functions. Every chain starts with the ``Ex()`` function call, which holds the exercise state. This exercise state contains all the information that is required to check if an exercise is correct, which are:

+ the student submission and the solution as text, and their corresponding parse trees.
+ a reference to the student workspace and the solution workspace.
+ the output and errors that were generated when executing the student code.

As SCT functions are chained together with ``.``, the exercise state is copied and adapted into so-called child states to zoom in on particular parts of the state.

Example 1: function call
========================

Consider the following snippet of markdown that represents part of an exercise

.. code::

    `@solution`
    ```{python}
    import pandas as pd
    pd.DataFrame([1, 2, 3])
    ```

    `@sct`
    ```{python}
    Ex().check_function('pandas.DataFrame').check_args('data').has_equal_value()
    ```

Assuming the student submitted the exact same code as the solution, the following happens when this SCT is executed:

- `Ex()` returns the 'root state', which considers the entire student submission and solution code:

  .. code::

      import pandas as pd
      pd.DataFrame([1, 2, 3])

- `check_function()` continues from the root state (considering the entire student submission and solution),
  and looks for a call of `DataFrame` in the `pandas` package. Afterwards, it 'zooms in' on the arguments.
  In simplified terms, this is the state it produces:

  .. code::

      { "data": [1, 2, 3] }

- `check_args()` continues from the state produced by ``check_function()`` and zooms in on the expression used to specify the argument `data`:

  .. code::

      [1, 2, 3]

- Finally, ``has_equal_value()`` evaluates the expression that is used to specify the argument (e.g. ``[1, 2, 3]`` for `data`),
  executes these expressions and verifies if they correspond between student and solution. As the student submission and solution code are the same, 
  the expression `[1, 2, 3]` evaluate to the same list, so the SCT passes.


Example 2: if statement
=======================

As a more advanced example, consider the following snippet of markdown that represents part of an exercise:

.. code::

    `@solution`
    ```{python}
    x = 4
    if x > 0:
        print("x is positive")
    ```
    
    `@sct`
    ```{python}
    Ex().check_if_else().multi(
        check_test().has_code(/x\s+>\s+0/), # chain A
        check_body().check_function('print', 0).check_args('value').has_equal_value() # chain B
        )
    ```

Notice how this time, ``multi()`` is used to have the SCT chains 'branch out'.
Both ``check_body()`` and ``check_test()`` continue from the state produced by ``check_if_else()``.

Case 1
~~~~~~

Int he first case, ssume the following student submission:

.. code::

    x = 4
    if x < 0:
        print("x is negative")

In chain A, this is what happens:

- ``check_if_else()`` considers the entire submission received from ``Ex()``
  and produces a child state that contains the ``if`` statements in student and solution:

  .. code::

      # solution
      if x > 0:
          print("x is positive")

      # student
      if x < 0:
          print("x is negative")

- ``check_test()`` considers the state above produced by ``check_if_else()``
  and produces a child state with only the condition parts of the ``if`` statements:

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

Chain A will go through the same steps and will pass this time as ``x > 0`` in the student submission now matches the regex. In Chain B, this is what happens:

- ``check_body()`` considers the state produced by ``check_if_else()``, and produces a child state with only the body parts of the ``if`` statements:

  .. code::

      # solution
      print("x is positive")

      # student
      print("x is negative")

- ``check_function()`` considers the state above produced by ``check_if()``, and tries to find the function ``print()``. Next, it produces a state with references to the different arguments that were specified and their values:

  .. code::

      # solution
      { "x": "x is positive" }

      # student
      { "x": "x is negative" }
  
- ``check_args()`` checks if the argument ``x`` is specified, and produces a child state that zooms in on the actual value of ``x``:

  .. code::

      # solution
      "x is positive"

      # student
      "x is negative"
  
- Finally, ``has_equal_ast()`` compares the equality of the two 'focused' arguments. They are not equal, so the check fails.


Test vs Has?	
============

As a general rule:

- ``check_`` functions produce a child state that 'dives' deeper into a part of the state it was passed.	They are typically chained off of for further checking.	
- ``has_`` functions always **return the state that they were intially passed** and are used at the 'end' of a chain.