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
    import matplotlib.pyplot as pltttt

    # failing submissions
    import matplotlib as mpl

By default, ``has_import()`` allows for different ways of aliasing the imported package or function. If you want to make sure the correct alias was used to refer to the package or function that was imported, set ``same_as=True``.

.. code::

    # solution
    import matplotlib.pyplot as plt

    # sct
    Ex().has_import("matplotlib.pyplot", same_as=True)

    # passing submissions
    import matplotlib.pyplot as plt
    from matplotlib import pyplot as plt

    # failing submissions
    import matplotlib.pyplot as pltttt
