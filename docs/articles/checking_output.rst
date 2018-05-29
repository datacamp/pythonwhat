Checking output
---------------

Among the student and solution process, the student submission and solution code as a string,
the ``Ex()`` state also contains the output that a student generated with his or her submission.

With ``check_output()``, you can access this output and match it against a regular or fixed expression.

As an example, suppose we want a student to print out a sentence:

.. code::

    # Print the "This is some ... stuff"
    print("This is some weird stuff")


The following SCT tests whether the student prints out ``This is some weird stuff``:

.. code::

    Ex().check_output("This is some weird stuff", pattern = False)

The ``pattern`` is set to ``False`` which causes ``check_output()`` to search for the pure string.
This SCT is not robust, because it won't be accepted if the student submits ``print("This is some cool stuff")``, for example.
Therefore, it's a good idea to use [regular expressions](https://docs.python.org/3.5/library/re.html).
`pattern=True` by default, so there's no need to specify this:

.. code::

    Ex().check_output(r"This is some \w* stuff",
                      no_output_msg = "Print out ``This is some ... stuff`` to the output, fill in ``...`` with a word you like.")

Now, different printouts will be accepted. Notice that we also specified ``no_output_msg`` here. If the pattern is not found in the output generated, this message will be shown instead of a (typically unhelpful) message that's automatically generated.
