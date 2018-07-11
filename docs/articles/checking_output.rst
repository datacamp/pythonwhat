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

    # Using exact string matching
    Ex().has_output("This is some weird stuff", pattern = False)

    # Using a regular expression (more robust) - pattern = True is the default
    Ex().has_output(r"This is some \w* stuff",
                    no_output_msg = "Print out ``This is some ... stuff`` to the output, fill in ``...`` with a word you like.")


Checking ``print()`` calls
~~~~~~~~~~~~~~~~~~~~~~~~~~

Checking whether the right printouts were done is easy:

.. code::

    # solution
    x = 4
    print(x)

    # sct
    Ex().has_output(0)

``has_output()`` will look for the printout in the solution code that you specified with ``index`` (0 in this case), rerun the ``print()`` call in
the solution process, capture its output, and verify whether the output is present in the output of the student.

Watch out: ``has_printout()`` will effectively **rerun** the ``print()`` call in the solution process after the entire solution script was executed.
If your solution script updates the value of `x` after executing it, ``has_output()`` will not work:

.. code::

    # solution
    x = 4
    print(x)
    x = 6

    # sct that won't work
    Ex().has_output(0)

In this example, when the ``print(x)`` call is executed, the value of ``x`` will be 6, and pythonwhat will look for the output `'6`' in the output the student generated.
In cases like these, default to using the classical pattern to check function calls:

.. code::
    
    # sct that will work
    Ex().check_function('print').check_args(0).has_equal_value()``

