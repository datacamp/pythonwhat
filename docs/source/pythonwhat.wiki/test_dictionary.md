test_dictionary
---------------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_dictionary.test_dictionary
```

    def test_dictionary(name,
                        keys=None,
                        undefined_msg=None,
                        not_dictionary_msg=None,
                        key_missing_msg=None,
                        incorrect_value_msg=None)

Test a dictionary. Consider this function an advanced version of `test_object`, where you can specify messages that are explicit to test dictionaries. `test_dictionary` takes a step-by-step approach to checking the correspondence of the dictionary between student and solution process:

- Step 1: Is the object specified in `name` actually defined?
- Step 2: Is the object specified in `name` actually a dictionary?
- Step 3: For each key, is the key specified in the dictionary?
- Step 4: For each key, is the value corresponding to the key correct when comparing to the solution?

For Step 3 and Step 4, you can control which keys have to be tested through the `keys` argument. If you don't specify this argument, `test_dictionary()` will look for all keys and compare the values that are specified in the corresponding dictionary in the solution process.

### Example: step by step

Suppose you want the student to create a dictionary `x`, that contains three keys: `"a"`, `"b"` and `"c"`. The following solution and sct could be used for this:

	*** =solution
	```{python}
	x = {'a': 123, 'b':456, 'c':789}
	```

	*** =sct
	```{python}
	test_dictionary('x')
	```

- Step 1: if the student submits an empty script, the feedback _Are you sure you defined the dictionary `x`?_ will be presented. You can override this by specifying `undefined_msg` yourself.
- Step 2: if the student submits `x = 123`, the feedback _`x` is not a dictionary._ will be presented. You can override this message by specifying `not_dictionary_msg` yourself.
- Step 3: if the student submits `x = {'a':123, 'b':456, 'd':78}`, the feedback _Have you specified a key `c` inside `x`?_ will be presented. You can override this by specifying `key_missing_msg` yourself.
- Step 4: if the student submits `x = {'a':123, 'b':456, 'c':78}`, the feedback _Have you specified the correct value for the key `c` inside `x`?_ will be presented. You can override this by specifying `incorrect_value_msg` yourself.

**NOTE**: Behind the scenes, `pythonwhat` has to fetch the value of objects from sub-processes. The required 'dilling' and 'undilling' can cause issues for exotic objects. For more information on this and possible errors that can occur, read the [Processes article](../expression_tests.md).
