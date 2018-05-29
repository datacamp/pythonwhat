Combining sets of SCTs
----------------------

In Python, there are many ways to solve a problem.
Writing an SCT that checks when students make a mistake, but is robust to multiple different solutions is a challenge.
``test_correct()`` and ``test_or()`` allow you to add logic to your SCT in two distinct ways.
Normally, your SCT is simply a script with subsequent ``pythonwhat`` function calls, all of which have to pass.
``test_correct()`` and ``test_or()`` allow you to bypass this.

test_correct
============

To explain the concept of ``test_correct()``, consider this example:

.. code::

    # setup
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5, 6])

    # calculate result
    result = np.mean(arr)

You want the SCT to pass when the student manages to store the correct value in the object ``result``.
How ``result`` was calculated, does not matter to you: as long as ``result`` is correct, the SCT should accept the submission.
If something about ``result`` is not correct, you want to dig a little deeper and see if the student used the ``np.mean()`` function correctly.
The following SCT will do just that:

.. code::

    Ex().test_correct(
            check_object("result").has_equal_value(),
            check_function("numpy.mean").check_args("a").has_equal_value()
         )


Inside ``test_correct()``, two SCT chains are specified, separated by a comma:

- A ``check`` chain, that has to pass in all cases, but when it fails, it doesn't immediately stop the SCT execution and fail the exercise.
- A ``diagnose`` chain, that is only execute if the ``check`` chain failed silently.

In the example, we're checking the end value of ``result`` first. Only if this is not correct, will the ``check_function()`` chain be run,
to verify if the student used ``numpy.mean``. If the ``diagnose`` chain does not fail, the ``check``` chain is executed again 'loudly'.

Let's see what happens in case of different student submissions:

- The student submits ``result = np.mean(arr)``

  - ``test_correct()`` runs the ``check_object()`` chain. 
  - This test passes, so ``test_correct()`` stops. 
  - The SCT passes.

- The student submits ``result = np.sum(arr) / arr.size``

  - ``test_correct()`` runs the ``check_object()`` chain.
  - This test passes, so ``test_correct()`` stops before running ``check_fucntion()``.
  - The entire SCT passes even though ``np.mean()`` was not used.

- The student submits ``result = np.mean(arr + 1)``

  - ``test_correct()`` runs the ``check_object()`` chain.
  - This test fails, so ``test_correct()`` continues with the ``diagnose`` part, running the ``check_function()`` chain.
  - This chain fails, since the argument passed to ``numpy.mean()`` in the student submission does not correspond to the argument passed in the solution.
  - A meaningful, specific feedback message is presented to the student: you did not correctly specify the arguments inside ``np.mean()``.

- The student submits ``result = np.mean(arr) + 1``

  - ``test_correct()`` runs the ``check_object()`` chain.
  - This test fails, so ``test_correct()`` continues with the ``diagnose`` part,  running the ``check_function()`` chain.
  - This function passes, because ``np.mean()`` is called in exactly the same way in the student code as in the solution.
  - Because there is something wrong - ``result`` is not correct - the ``check`` chain is executed again, and this time its feedback on failure is presented to the student.
  - The student gets the message that ``result`` does not contain the correct value.


Multiple functions in ``diagnose`` and `check`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is perfectly possible for your ``check`` and ``diagnose`` SCT chains to branch out into different sub-branches with ``multi()``:

.. code::

    Ex().test_correct(
            multi(check_object('a').has_equal_value(), # multiple check SCTs
                  check_object('b').has_equal_value()),
            check_function("numpy.mean").check_args("a").has_equal_value()
         )


Why use `test_correct()`
~~~~~~~~~~~~~~~~~~~~~~~~

You will find that ``test_correct()`` is an extremely powerful function to allow for different ways of solving the same problem.
You can use ``test_correct()`` to check the end result of a calculation.
If the end result is correct, you can go ahead and accept the entire exercise.
If the end result is incorrect, you can use the ``diagnose`` part of ``test_correct()`` to dig a little deeper.

It is also perfectly possible to use ``test_correct()`` inside another ``test_correct()``.

test_or
=======

``test_or()`` tests whether one of the SCTs you specify inside it passes. Suppose you want to check whether people correctly printed out any integer between 3 and 7. A solution could be:

.. code::
	
    print(4)
		

To test this in a robust way, you could use ``test_output_contains()`` with a suitable regular expression that covers everything,
or you can use ``test_or()`` with three separate ``test_output_contains()`` functions:

.. code::

	test_or(test_output_contains('4'),
            test_output_contains('5'),
            test_output_contains('6'))

You can consider ``test_or()`` a logic-inducing function. The different calls to ``pythonwhat`` functions that are in your SCT are actually all tests that _have_ to pass:
they are ``AND`` tests. With ``test_or()`` you can add chunks of ``OR`` tests in there.

