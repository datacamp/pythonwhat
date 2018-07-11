Checking objects
----------------

In ``pythonbackend``, both the student's submission as well as the solution code are executed, in separate processes.
``check_object()`` looks at these processes and checks if the referenced object is available in the student process.
Next, you can use ``has_equal_value()`` to check whether the objects in the student and solution process correspond.

.. note::

    For more information how DataCamp's coding backends run code, check out `this article <https://authoring.datacamp.com/courses/exercises/technical-details/sct.html>`_

Basic example
=============

Consider the following solution, and corresponding SCT:

.. code::

    # solution
    x = 15

    # sct option 1
    Ex().check_object("x").has_equal_value()

    # submissions that will pass this sct
    x = 10
    x = 12 + 3
    x = 3; x += 12


- ``check_object()`` will check if the variable ``x`` is defined in the student process.
- ``has_equal_value()`` will check whether the value of ``x`` in the solution process is the same as in the student process.


.. note::

    If you only use ``Ex().check_object("x")`` without ``has_equal_value()``, you are only checking whether the object is defined.

.. caution::

    ``has_equal_value()`` only looks at **end result** of a variable in the student process. In the example, how the object ``x`` came about in the student's submission, does not matter.    

Exotic objects
==============

pythonwhat compares the objects in the student and solution process with the ``==`` operator.
For basic objects, this ``==`` is operator is properly implemented, so that the objects can be effectively compared.
For more complex objects that are produced by third-party packages, however, it's possible that this equality operator is not implemented in a way you'd expect.
Often, for these object types the ``==`` will compare the actual object instances.

.. code::

    # pre exercise code
    class Number():
        def __init__(self, n):
            self.n = n

    # solution
    x = Number(1)

    # sct that won't work
    Ex().check_object().has_equal_value()

    # sct
    Ex().check_object().has_equal_value(expr_code = 'x.n')

    # submissions that will pass this sct
    x = Number(1)
    x = Number(2 - 1)
    
The basic SCT like in the previous example won't work here.
Notice how we used the ``expr_code`` argument to _override_ which value `has_equal_value()` is checking.
Instead of checking whether `x` corresponds between student and solution process, it's now executing the expression ``x.n``
and seeing if the result of running this expression in both student and solution process match.
