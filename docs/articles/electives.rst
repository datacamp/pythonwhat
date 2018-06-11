Electives
---------

Success message
===============

When all tests in an SCT pass, ``pythonwhat`` will automatically generate a congratulatory message to present to the student. If you want to override this 'success message', you can use the ``success_msg()`` function.

.. code::

    Ex().check_object("x").has_equal_value()
    Ex().success_msg("You are a hero when it comes to variable assignment!")


`This article <https://authoring.datacamp.com/courses/exercises/all-exercise-types/success-message.html>`_ on the authoring docs describes how to write good success messages.


Multiple choice exercises
=========================

Multiple choice exercises are straightforward to test.
Use ``test_mc()`` to provide tailored feedback for both the incorrect options, as the correct option.
Below is the markdown source for a multiple choice exercise example, with an SCT that uses ``test_mc``:

.. code-block:: none

    ## The author of Python
    
    ```yaml
    type: MultipleChoiceExercise
    ```
    
    Who is the author of the Python programming language?
    
    `@instructions`
    
    - Roy Co
    - Ronald McDonald
    - Guido van Rossum
    
    `@sct`

    ```{python}
    test_mc(correct = 3, 
            msgs = ["That's someone who makes soups.",
                    "That's a clown who likes burgers.",
                    "Correct! Head over to the next exercise!"])
    ```

The first argument of ``test_mc()``, ``correct``, should be the number of the correct answer in this list.
Here, the correct answer is Guido van Rossum, corresponding to 3.
The ``msgs`` argument should be a list of strings with a length equal to the number of options.
We encourage you to provide feedback messages that are informative and tailored to the (incorrect) option that people selected.
Make sure to correctly order the feedback message such that it corresponds to the possible answers that are listed in the instructions tab.
Notice that there's no need for ``success_msg()`` in multiple choice exercises, as you have to specify the success message inside ``test_mc()``,
along with the feedback for incorrect options.

Capabilities of multi
=====================

``multi()`` is always used to 'branch' different chains of SCT functions, so that the same state is passed to two sub-chains. There are different ways

Comma separated arguments
~~~~~~~~~~~~~~~~~~~~~~~~~

Most commonly, ``multi()`` is used to convert this code

.. code::

    Ex().check_if_exp().check_body().has_equal_value()
    Ex().check_if_exp().check_test().has_equal_value()


into this equivalent (and more performant) SCT:

.. code::

    Ex().check_if_exp().multi(
            check_body().has_equal_value(),
            check_test().has_equal_value()
            )

List or generator of subtests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rather than one or more subtest args, multi can take a single list or generator of subtests.
For example, the code below checks that the body of a list comprehension has equal value
for 10 possible values of the iterator variable, ``i``.

.. code::

    Ex().check_list_comp()
        .check_body()
        .multi(set_context(i=x).has_equal_value() for x in range(10))

Chaining off multi
~~~~~~~~~~~~~~~~~~

Multi returns the same state, or focus, it was given, so whatever comes after multi will run 
the same as if multi wasn't used. For example, the code below tests a list comprehension's body,
followed by its iterator.

.. code::

    Ex().check_list_comp() \
        .multi(check_body().has_equal_value()) \
        .check_iter().has_equal_value()

has_context
===========

Tests whether context variables defined by the student match the solution, for a selected block of code.
A context variable is one that is defined in a looping or block statement.
For example, ``ii`` in the code below.

.. code::

    [ii + 1 for ii in range(3)]

By default, the test fails if the submission code does not have the same number of context variables.
This is illustrated below.

.. code::

    # solution
    # ii and ltr are context variables
    for ii, ltr in enumerate(['a']): pass

    # sct
    Ex().check_for_loop().check_body().has_context()

    # passing submission
    # still 2 variables, just different names
    for jj, Ltr in enumerate(['a']): pass

    # failing submission
    # only 1 variable
    for ii in enumerate(['a']): pass

.. note::
   
   If you use ``has_context(exact_names = True)``, then the submission must use the same names for the context variables,
   which would cause the passing submission above to fail.

set_context
===========

Sets the value of a temporary variable, such as ``ii`` in the list comprehension below.

.. code::

    [ii + 1 for ii in range(3)]

Variable names may be specified using positional or keyword arguments.


Example
~~~~~~~

.. code::

    # solution
    ltrs = ['a', 'b']
    for ii, ltr in enumerate(ltrs):
        print(ii)

    # sct
    Ex().check_for_loop().check_body() \
        .set_context(ii=0, ltr='a').has_equal_output() \
        .set_context(ii=1, ltr='b').has_equal_output()

Note that if a student replaced ``ii`` with ``jj`` in their submission, ``set_context`` would still work.
It uses the solution code as a reference. While we specified the target variables ``ii`` and ``ltr``
by name in the SCT above, they may also be given by position..

.. code::

    Ex().check_for_loop().check_body().set_context(0, 'a').has_equal_output()


Instructor Errors
~~~~~~~~~~~~~~~~~

If you are unsure what variables can be set, it's often easiest to take a guess.
When you try to set context values that don't match any target variables in the solution code,
``set_context()`` raises an exception that lists the ones available.


with_context
============

.. autofunction:: pythonwhat.check_funcs.with_context
    :noindex:

Runs subtests after setting the context for a ``with`` statement.

This function takes arguments in the same form as ``multi``.

Context Managers Explained
~~~~~~~~~~~~~~~~~~~~~~~~~~

With statements are special in python in that they enter objects called a context manager at the beginning of the block,
and exit them at the end. For example, the object returned by ``open('fname.txt')`` below is a context manager.

.. code::

    with open('fname.txt') as f:
        print(f.read())

This code runs by

1. assigning ``f`` to the context manager returned by ``open('fname.txt')``
2. calling ``f.__enter__()``
3. running the block
4. calling ``f.__exit__()``

``with_context`` was designed to emulate this sequence of events, by setting up context values as in step (1), 
and replacing step (3) with any sub-tests given as arguments.


fail
====

.. autofunction:: pythonwhat.check_funcs.fail

Fails. This function takes a single argument, ``msg``, that is the feedback given to the student.
Note that this would be a terrible idea for grading submissions, but may be useful while writing SCTs.
For example, failing a test will highlight the code as if the previous test/check had failed.

As a trivial SCT example,

.. code::

    Ex().check_for_loop().check_body().fail()     # fails boo

This can also be helpful for debugging SCTs, as it can be used to stop testing as a given point.


