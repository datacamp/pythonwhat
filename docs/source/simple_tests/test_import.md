test_import
-----------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_import
    :members:
```

		def test_import(name,
		                same_as=True,
		                not_imported_msg=None,
		                incorrect_as_msg=None):

With `test_import` you can test whether a student correctly imported a certain package. As an option, you can also specify whether or not the same alias should be used.

Python features many ways to import packages. All of these different methods revolve around the `import`, `from` and `as` keywords. Suppose you want students to import `matplotlib.pyplot` as `plt` (the common way of importing the plotting tools in `matplotlib`. A possible solution of your exercises could be the following:

		*** =solution
		```{python}
		# Import plotting tools
		import matplotlib.pyplot as plt
		```

Below is a possible SCT for this exercise:

		*** =sct
		```{python}
		test_import("matplotlib.pyplot")
		success_msg("You nailed it!")
		```

Here, `test_import` will parse both the student's submission as well as the solution, and figure out which packages were imported and how. Next, it checks if the `matplotlib.pyplot` package was imported and under which alias. If the student did this and imported it as `plt`, all is good. If, however, the student submitted `import matplotlib` (import entire package instead of module) or `import matplotlib.pyplot as pppplot` (incorrect alias), `test_import()` will fail and generate the appropriate messages. 

As usual, you can override these messages with your own:

		*** =sct
		```{python}
		test_import("matplotlib.pyplot"),
								not_imported_msg = "You can import pyplot by using `import matplotlib.pyplot`.",
								incorrect_as_msg = "You should set the correct alias for `matplotlib.pyplot`, import it `as plt`.")
		success_msg("You nailed it!")
		```

With `same_as`, you can control whether or not the alias should be exactly the same. By default `same_as=True`, so the alias (`plt` in the example) should also be used by student. If you set it to `False`:

		*** =sct
		```{python}
		test_import("matplotlib.pyplot", same_as=False)
		success_msg("You nailed it!")
		```

The SCT will also pass if the student uses `import matplotlib.pyplot as pppplot`, a submission that wouldn't be accepted if `same_as=True`.
