Checking output
---------------

Checking any output
~~~~~~~~~~~~~~~~~~~

Among the student and solution process, the student submission and solution code as a string,
the ``Ex()`` state also contains the output that a student generated with his or her submission.

With ``has_output()``, you can access this output and match it against a regular or fixed expression.

As an example, suppose we want a student to print out a sentence:

.. code::

    # Print the "This is some ... stuff"
    print("This is some weird stuff")


The following SCT tests whether the student prints out ``This is some weird stuff``:

.. code::

    Ex().has_output("This is some weird stuff", pattern = False)

The ``pattern`` is set to ``False`` which causes ``has_output()`` to search for the pure string.
This SCT is not robust, because it won't be accepted if the student submits ``print("This is some cool stuff")``, for example.
Therefore, it's a good idea to use `regular expressions <https://docs.python.org/3.5/library/re.html>`_.
`pattern=True` by default, so there's no need to specify this:

.. code::

    Ex().has_output(r"This is some \w* stuff",
                    no_output_msg = "Print out ``This is some ... stuff`` to the output, fill in ``...`` with a word you like.")

Now, different printouts will be accepted. Notice that we also specified ``no_output_msg`` here. If the pattern is not
found in the output generated, this message will be shown instead of a (typically unhelpful) message that's automatically generated.

Checking printouts
~~~~~~~~~~~~~~~~~~

In the past, the following SCT was used to check printouts:

.. code::

    Ex().check_function('print', 0).check_args(0).has_equal_value()

Not only is this very tedious and long to write for something that is so common, it is also not very robust.
``pythonwhat`` will look for the first ``print()`` call in the student code, which breaks if the student did
another printout call before the one you're trying to test. Also, this approach requires the student to call
the ``print()`` function in exactly the same way as the solution, although there are multiple ways.

Instead, you can now use

.. code::

    Ex().has_printout(0)

This will look for the printout in the solution code that you specified with ``index``, rerun the ``print()`` call in
the solution process, capture its output, and verify whether the output is present in the output of the student.
It's faster and more robust!