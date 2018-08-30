SingleProcessExercise
---------------------

Introduction
============

Typical interactive exercises on DataCamp will be of the type ``NormalExercise`` or something similar.

For these normal exercises, the pythonbackend (the Python package responsible
for running Python code that the student submitted) will execute:

- the solution code in a solution process
  (once, at exercise initialization),
- the student's submission in a student process
  (every time the student hits submit, after which the process is restarted from scratch)
- the student's experimentation commands in the console in a console process
  (every time the user executes a command, without restarting afterwards)

These completely separate processes make sure that:

- the different commands do not interfere with one another;
  if you import a package in one process,
  the package will not become available in the other process.
- pythonwhat has access to a 'target solution process' to easily do comparisons;
  to compare an object ``x``, you simply have to use ``Ex().check_object('x').has_equal_value()`` and
  pythonwhat will figure out the value ``x`` should have from the solution process.

To learn more about how the backend works, you can visit
`this wiki article <https://github.com/datacamp/pythonbackend/wiki>`_.

Why does this exercise type exist?
==================================

There are Python courses that make extensive use of programs running outside of Python.
Sometimes, these programs cannot handle it well when different
Python process are trying to interface with it.
An example of this is PySpark, where on container startup,
a Spark cluster is started up, that you can then interface with.
Things go horribly wrong if you try to access this PySpark cluster from different Python processes.

To solve for this, a new exercise type was built,
that does not create three separate Python processes (solution, student, console).
Instead, only one process is created:

- the solution code is not executed in this process.
- the student's sumission is executed in this process, but the process is not restarted afterwards
- the student's experimentation commands in the console are executed in the same process.

From a user perspective, this shouldn't pose too much difficulties,
with the exception that the code execution is now stateful.

So, what's the problem then?
============================

As mentioned earlier, pythonwhat depends heavily on the existence of
two separate process: a 'target' solution process, and a student process.
Functions such as ```has_equal_value()`` compare values and the results of expression in these processes.
In the ``SingleProcessExercise``, the student process and
the solution process are identical, it's one and the same process,
so these comparisons don't make any sense.

Therefore, the 'process-based checks' in pythonwhat have to be used with care when
writing SCTs for a ``SingleProcessExercise``. More specifically:

- ``check_object()`` should work okay, as there is some magic happening behind the scenes.
- ``has_equal_value()`` and ``has_equal_output()`` should be used with the ``override`` argument.
  When this argument is specified, the expression that is 'zoomed in on' in the solution code will not be executed in the solution proces.
  Instead, it will just take the value you pass to ``override`` to compare the result/output of the expression that is zoomed in on in the student code to.

Example
=======

As an example, suppose we want to check whether a student correctly created a list ``x``:

.. code::

    # solution
    x = [1, 2, 3, 4, 5]

If this solution were part of a traditional ``NormalExercise``, your SCT would be simple:

.. code::

    # SCT
    Ex().check_object('x').has_equal_value()

However, if this solution were part of a ``SingleProcessExercise``, the above SCT would not work.
Instead, you'll want to do the following:

.. code::

    # SCT
    Ex().check_object('x').has_equal_value(override = [1, 2, 3, 4, 5])

Here, we use ``override`` to tell pythonwhat not to go look for the value of ``x`` in the solution process.
Instead, it uses the manually specified value in ``override`` to compare to.

You can use ``override`` in combination with other arguments in ``has_equal_x()``, such as ``expr_code``.
Suppose you're only interested in the element at index 2 of the list ``x``:

.. code::

    # SCT
    Ex().check_object('x').has_equal_value(expr_code = 'x[2]', override = 3)

Tricky stuff, but it works!