Glossary
--------

TODO add more

Check object
~~~~~~~~~~~~

.. code::

    # solution
    x = 10
    
    # sct
    Ex().check_object('x').has_equal_value()


Check function call
~~~~~~~~~~~~~~~~~~~

.. code::

    # solution
    import pandas as pd
    pd.DataFrame([1, 2, 3], columns=['a'])

    # sct
    Ex().check_function('pandas.DataFrame')\
        .multi(
            check_args('data').has_equal_value(),
            check_args('columns').has_equal_value()
        )

Check object created through function call
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # pec
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5, 6])

    # solution
    result = np.mean(arr)

    # sct
    Ex().test_correct(
        check_object("result").has_equal_value(),
        check_function("numpy.mean").check_args("a").has_equal_value()
        )
    
Check output
~~~~~~~~~~~~

.. code::

    # solution
    print("This is some weird stuff")

    # sct
    Ex().test_output_contains(r"This is some \w* stuff")

Check list comprehensions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # solution
    L2 = [ i*2 for i in range(0,10) if i>2 ]

    # sct
    Ex().check_list_comp(0).multi(
        check_body().test_student_typed('i\*2'),
        check_iter().has_equal_value(),
        check_ifs(0).multi([has_equal_value(context_vals=[i]) for i in range(0,10)])
    )

