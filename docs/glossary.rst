Glossary
--------

This article lists some example solutions. For each of these solutions, an SCT
is included, as well as some example student submissions that would pass and fail. In all of these,
a submission that is identical to the solution will pass.

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

Check pandas chain (1)
~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # solution
    import pandas as pd
    df = pd.DataFrame([1, 2, 3], columns=['a'])
    df.a.sum()

    # sct
    Ex().check_function("df.a.sum").has_equal_value()

Check pandas chain (2)
~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # pec
    import pandas as pd
    df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'x', 'y']})

    # solution
    df.groupby('b').sum()

    # sct
    sig = sig_from_obj("df.groupby('b').sum")
    Ex().check_correct(
        # check if group by works
        check_function("df.groupby.sum", signature = sig).has_equal_value(),
        # check if group_by called correctly
        check_function("df.groupby").check_correct(
            has_equal_value(func = lambda x,y: x.keys == y.keys),
            check_args(0).has_equal_value()
        )
    )

    # passing submissions
    df.groupby('b').sum()
    df.groupby(['b']).sum()

    # failing submissions
    df               # Did you call df.groupby()?
    df.groupby('a')  # arg of groupby is incorrect
    df.groupby('b')  # did you call df.groupby.sum()?

Check pandas plotting
~~~~~~~~~~~~~~~~~~~~~

.. code::

    # pec
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    np.random.seed(42)
    df = pd.DataFrame({'val': np.random.rand(300) })

    # solution
    df.val.plot(kind='hist')
    plt.title('my plot')
    plt.show()
    plt.clf()

    # sct
    Ex().check_or(
        multi(
            check_function('df.val.plot').check_args('kind').has_equal_value(),
            check_function('matplotlib.pyplot.title').check_args(0).has_equal_value()
        ),
        override("df.val.plot(kind='hist', title='my plot')").check_function('df.val.plot').multi(
            check_args('kind').has_equal_value(),
            check_args('title').has_equal_value()
        ),
        override("df['val'].plot(kind = 'hist'); plt.title('my plot')").multi(
            check_function('df.plot').check_args('kind').has_equal_value(),
            check_function('matplotlib.pyplot.title').check_args(0).has_equal_value()
        ),
        override("df['val'].plot(kind='hist', title='my plot')").check_function('df.plot').multi(
            check_args('kind').has_equal_value(),
            check_args('title').has_equal_value()
        )
    )
    Ex().check_function('matplotlib.pyplot.show')
    Ex().check_function('matplotlib.pyplot.clf')


Check object created through function call
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # pec
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5, 6])

    # solution
    result = np.mean(arr)

    # sct
    Ex().check_correct(
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
    Ex().check_df("my_df").check_keys("a").has_equal_value()

    # passing submissions
    my_df = pd.DataFrame({"a": [1, 1 + 1, 3], "b": [4, 5, 6]})
    my_df = pd.DataFrame({"b": [4, 5,  6], "a": [1, 2, 3]})

Check printout
~~~~~~~~~~~~~~

.. code::

    # solution
    x = 3
    print(x)

    # sct
    Ex().has_printout(0)

    # passing submissions
    print(3)
    print(1 + 1)
    x = 4; print(x - 1)

Check output
~~~~~~~~~~~~

.. code::

    # solution
    print("This is weird stuff")

    # sct
    Ex().has_output(r"This is \w* stuff")

    # passing submissions
    print("This is weird stuff")
    print("This is fancy stuff")
    print("This is cool stuff")

    # failing submissions
    print("this is weird stuff")
    print("Thisis weird stuff")

Check Multiple Choice
~~~~~~~~~~~~~~~~~~~~~

.. code::

    # solution (implicit)
    # 3 is the correct answer

    # sct
    Ex().has_chosen(correct = 3, # 1-base indexed
                    msgs = ["That's someone who makes soups.",
                            "That's a clown who likes burgers.",
                            "Correct! Head over to the next exercise!"])

Recommended approach for testing train test splits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # solution
    # Perform the train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # sct
    Ex().check_correct(
        multi(
            check_object("X_train").has_equal_value(),
            check_object("X_test").has_equal_value(),
            check_object("y_train").has_equal_value(),
            check_object("y_test").has_equal_value()
        ),
        check_function("sklearn.model_selection.train_test_split").multi(
                check_args(["arrays", 0]).has_equal_value("Did you correctly pass in the feature variable to `train_test_split()`?"),
                check_args(["arrays", 1]).has_equal_value("Did you correctly pass in the target variable to `train_test_split()`?"),
                check_args(["options", "test_size"]).has_equal_value("Did you specify the correct train test split?"),
                check_args(["options", "random_state"]).has_equal_value("Don't change the `random_state` argument we set for you.")
        )
    )


Check import
~~~~~~~~~~~~

`See has_import doc <reference.html#pythonwhat.check_wrappers.has_import>`_

Check if statement
~~~~~~~~~~~~~~~~~~

`See check_if_else doc <reference.html#pythonwhat.check_wrappers.check_if_else>`_

Check function definition
~~~~~~~~~~~~~~~~~~~~~~~~~

`See check_function_def doc <reference.html#pythonwhat.check_wrappers.check_function_def>`_

Check list comprehensions
~~~~~~~~~~~~~~~~~~~~~~~~~

`See check_list_comp doc <reference.html#pythonwhat.check_wrappers.check_list_comp>`_
