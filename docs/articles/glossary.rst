Glossary
--------

This article lists some example solutions. For each of these solutions, an SCT
is included, as well as some example student submissions that would pass and fail. In all of these,
a submission that is identical to the solution will evidently pass.

.. note::

    These SCT examples are not golden bullets that are perfect for your situation.
    Depending on the exercise, you may want to focus on certain parts of a statement, or be
    more accepting for different alternative answers.

Check object
~~~~~~~~~~~~

.. code::

    # solution
    x = 10
    
    # sct
    Ex().check_object('x').has_equal_value()

    # passing submissions
    x = 5 + 5
    x = 6 + 4
    y = 4; x = y + 6


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

    # passing submissions
    pd.DataFrame([1, 1+1, 3], columns=['a'])
    pd.DataFrame(data=[1, 2, 3], columns=['a'])
    pd.DataFrame(columns=['a'], data=[1, 2, 3])

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
    
    # passing submissions
    result = np.mean(arr)
    result = np.sum(arr) / arr.size

Check DataFrame
~~~~~~~~~~~~~~~

.. code::

    # solution
    import pandas as pd
    my_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    # sct
    import pandas as pd
    Ex().check_df("my_df").multi(has_key("a"), has_equal_key("b"))

    # passing submissions
    my_df = pd.DataFrame({"a": [1, 1 + 1, 3], "b": [4, 5, 6]})
    my_df = pd.DataFrame({"b": [4, 5,  6], "a": [1, 2, 3]})


Check output
~~~~~~~~~~~~

.. code::

    # solution
    print("This is weird stuff")

    # sct
    Ex().check_output(r"This is \w* stuff")

    # passing submissions
    print("This is weird stuff")
    print("This is fancy stuff")
    print("This is cool stuff")

    # failing submissions
    print("this is weird stuff")
    print("Thisis weird stuff")

Check import
~~~~~~~~~~~~

.. code::

    # solution
    import matplotlib.pyplot as plt

    # sct
    Ex().check_import("matplotlib.pyplot", same_as=False)

    # passing submissions
    import matplotlib.pyplot as plt
    import matplotlib.pyplot as ppplt

    # failing submissions
    import matplotlib as mpl


Check if statement
~~~~~~~~~~~~~~~~~~

.. code::

    # solution
    x = 4
    if x > 0:
        print("x is positive")

    # sct
    Ex().check_if_else().multi(
        check_test().multi([ has_equal_value(extra_env = {'x': i}) for i in [4, -1, 0, 1] ]),
        check_body().check_function('print', 0).check_args('value').has_equal_value()
        )

    # passing submission
    x = 4
    if 0 < x:
        print("x is positive")


Check list comprehensions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # solution
    L2 = [ i*2 for i in range(0,10) if i>2 ]

    # sct
    Ex().check_list_comp(0).multi(
        check_body().check_code('i\*2'),
        check_iter().has_equal_value(),
        check_ifs(0).multi([has_equal_value(context_vals=[i]) for i in range(0,10)])
    )

Check Multiple Choice
~~~~~~~~~~~~~~~~~~~~~

.. code::

    # solution (implicit)
    # 3 is the correct answer

    # sct
    test_mc(correct = 3,
            msgs = ["That's someone who makes soups.",
                    "That's a clown who likes burgers.",
                    "Correct! Head over to the next exercise!"])