Test to Check
-------------

If you are looking at the SCTs of old DataCamp courses, you'll notice they use ``test_x()`` functions instead of ``check_x()`` functions,
and there is no usage of ``Ex()``. The ``test_x()`` way of doing things has now been phased out in terms of the more verbose,
but more transparent and composable ``check_x()`` functions that start with ``Ex()`` and are chained together with the ``.`` operator.

Whenever you come across an SCT that uses ``test_x()`` functions,
you'll make everybody's life easier by converting it to a ``check_x()``-based SCT.
Below are the most common cases you will encounter, together with instructions on how to translate from one to the other.

Something you came across that you didn't find in this list?
Just create an issue on GitHub. Content Engineering will explain how to translate the SCT and update this article.

``test_student_typed``
======================

.. code::

    # Solution
    y = 1 + 2 + 3

    # old SCT
    test_student_typed(r'1\s*\+2\s*\+3')

    # new SCT
    Ex().has_code(r'1\s*\+2\s*\+3')
    

``test_object``
===============

.. code::

    # Solution
    x = 4

    # old SCT (checks equality by default)
    test_object('x')

    # new SCT
    Ex().check_object('x').has_equal_value()

.. code::

    # Solution
    x = 4

    # old SCT
    test_object('x', do_eval=False)

    # new SCT
    Ex().check_object('x')


``test_function``
=================

.. code::

    # Solution
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5])
    np.mean(arr)

    # old SCT (checks all args specified in solution)
    test_function('numpy.array')

    # new SCT
    Ex().check_function('numpy.array').check_args('a').has_equal_value()


.. code::

    # Solution
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5])
    np.mean(arr)
    np.mean(arr + arr)

    # old SCT (1-based indexed)
    test_function('numpy.array', index=1)
    test_function('numpy.array', index=2)

    # new SCT (0-based indexed)
    Ex().check_function('numpy.array', index=0).check_args('a').has_equal_value()
    Ex().check_function('numpy.array', index=1).check_args('a').has_equal_value()


``test_function_v2``
====================

.. code::

    # Solution
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5])
    np.mean(arr)

    # old SCT (explicitly specify args)
    test_function_v2('numpy.array', params=['a'], index=1)

    # new SCT
    Ex().check_function('numpy.array', index=0).check_args('a').has_equal_value()

``test_correct``
================

.. code::

    # Solution
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5])

    # old SCT (use lambdas to defer execution)
    test_correct(lambda: test_object('arr'),
                 labmda: test_function('numpy.array'))

    # new SCT (no need for lambdas)
    Ex().test_correct(check_object('arr').has_equal_value(),
                      check_function('numpy.array').check_args('a').has_equal_value())


