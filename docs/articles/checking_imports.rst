Checking imports
----------------

Python features many ways to import packages. All of these different methods revolve around the ``import``, ``from`` and ``as`` keywords.
``has_import()`` provides a robust way to check whether a student correctly imported a certain package.

Take this example to check whether a studnet imported ``matplotlib.pyplot`` as ``plt``:

.. code::

    # solution
    import matplotlib.pyplot as plt

    # sct
    Ex().has_import("matplotlib.pyplot")

    # passing submissions
    import matplotlib.pyplot as plt
    from matplotlib import pyplot as plt

    # failing submissions
    import matplotlib.pyplot as pltttt

Note that by default ``has_import()`` also checks whether the correct alias was used to refer to the package after it is imported. If you want to give more liberty to the student, you can set ``same_as`` to ``False``:

.. code::

    # solution
    import matplotlib.pyplot as plt

    # sct
    Ex().has_import("matplotlib.pyplot", same_as=False)

    # passing submissions
    import matplotlib.pyplot as plt
    from matplotlib import pyplot as plt
    import matplotlib.pyplot as pltttt
