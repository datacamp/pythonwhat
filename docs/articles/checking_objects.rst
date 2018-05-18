Checking objects
----------------

``check_object()`` is the start of your SCT chains to check whether students have correctly defined objects.

In ``pythonbackend``, both the student's submission as well as the solution code are executed, in separate processes.
``check_object()`` looks at these processes and checks if the object specified in ``name`` is available in the student process.
Next, through ``has_equal_value()``, you can assert whether the objects in the student and solution process correspond.

Example 1: Basic
================

Consider the following solution:

.. code::

    # Create a variable x
    x = 15

You don’t care too much about how ``x`` was created, as long as it’s defined and refers to the correct value. To test this robustly, you can use check_object() in your SCT:

.. code::

    Ex().check_object("x").has_equal_value()

``check_object()`` will check if the variable ``x`` is defined in the student process. ``has_equa_value()`` will check whether its value is the same as in the solution process. 

All of the following student submissions will be accepted by check_object():

- ``x = 15``
- ``x = 12 + 3``
- ``x = 3; x += 12``

.. note::

    ``has_equal_value()`` only looks at **end result** of a variable in the student process. In the example, how the object ``x`` came about in the student's submission, does not matter.

    
Example 2: Check existence
==========================

Say that you want the student to create an object ``x``, but you don't care what the contents of the variable are:

.. code::

    # Create an arbitrary object x
    x <- 123

Simply drop the ``check_equal()`` bit in your SCT:

.. code::

    Ex().check_object("x")
    

Example 3: Exotic objects
=========================

Python objects are compared using the ``==`` operator and objects can overwrite its implementation to fit the object's needs. 
Internally, ``test_object()`` uses the ``==`` operation to compare objects, this means you could encounter undesirable behaviour. 
For more complex objects,  ``==`` just compares the actual object instances, and objects which are semantically alike won't be according to ``has_equal_value()``.

The the following example solution:

.. code::

    # Pre exercise code
    from urllib.request import urlretrieve
    fn1 = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite'
    urlretrieve(fn1, 'Chinook.sqlite')
    from sqlalchemy import create_engine
    import pandas as pd

    # Create engine: engine
    engine = create_engine('sqlite:///Chinook.sqlite')

    # Open engine connection
    con = engine.connect()

An SCT for this exercise could be the following:

.. code::

    Ex().check_object("engine").has_equal_value()

Now, if the student enters the exact same code as the solution, the SCT will still fail. That is because

.. code::

    create_engine('sqlite:///Chinook.sqlite') == create_engine('sqlite:///Chinook.sqlite')
    
will return ``False``. You can work around this by manually defining a so-called converter. To learn more about this, visit the `Processes article <processes.html>`_.

Example 4: Pandas Data Frames
=============================

``check_object()`` has several utility functions associated with it that enable you to only look at parts of the object. A common use case for this are pandas data frames. Consider the following example:

.. code::

    import pandas as pd
    my_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

The following SCT checks that `my_df` is a `DataFrame`, that column `a` is specified, and that column `b` is specified and correct:

.. code::

    import pandas as pd
    Ex().check_df("my_df").multi(
        has_key("a"),
        has_equal_key("b")
    )

Notice that you had to explicitly import the pandas package so you could use its class definition to check if the instance was correct.