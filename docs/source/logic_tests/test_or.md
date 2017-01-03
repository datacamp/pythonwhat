test_or
-------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_or
    :members:
```

This function simply tests whether one of the SCTs you specify inside it passes. You should pass your SCTs within lambda expressions or custom defined functions (like you do for functions like `test_correct()`, `test_for_loop()`, or `test_function_definition`).

Suppose you want to check whether people correctly printed out any integer between 3 and 7. A solution could be:

		*** =solution
		```{python}
		print(4)
		```

To test this in a robust way, you could use `test_output_contains()` with a suitable regular expression that covers everything, or you can use `test_or()` with three separate `test_output_contains()` functions.

		*** =sct
		```{python}
		test_or(lambda: test_output_contains('4'),
		        lambda: test_output_contains('5'),
		        lambda: test_output_contains('6'))
		success_msg("Nice job!")
		```

You can consider `test_or()` a logic-inducing function. The different calls to `pythonwhat` functions that are in your SCT are actually all tests that _have_ to pass: they are `AND` tests. With `test_or()` you can add chunks of `OR` tests in there.
