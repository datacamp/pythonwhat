Quickstart Guide
================

Course Setup
------------

This guide will cover the basics of creating submission correctness tests (SCTs) for DataCamp exercise. SCTs deal with the running and testing code submissions, in order to give useful feedback. For help on the entire exercise creation process, check out https://www.datacamp.com/teach/documentation. If this is your first time creating a course, see their [Getting Started screencast](https://www.datacamp.com/teach/documentation#tab_getting_started) and [Code Exercises article](https://www.datacamp.com/teach/documentation#tab_code_exercises).

Your First Exercise
-------------------

As a basic example, suppose we have an exercise that requires the student to print a variable named `x`. This exercise could look something like this:


``````python
	*** =pre_exercise_code
	```{python}
	x = 5
	```

	*** =sample_code
	```{python}
	# Print x
	
	```

	*** =solution
	```{python}
	# Print x
	print(x)
	```

	*** =sct
	```{python}
	Ex().check_object('x').has_equal_value()
	Ex().test_output_contains('5')
	success_msg('Great job!')
	```
``````

The SCT uses three `pythonwhat` chains to test the correctness of the student's submission. 

1. `check_object` is used to test whether `x` was defined in the submission. In addition, the `has_equal_value()` statement tests whether the value of `x` is equal between the submission and solution.
2. `test_output_contains()` tests whether the student printed out `x` correctly. The function looks at the output the student generated with his or her submission, and then checks whether the string '5' is found in this output.
3. `success_msg()` is used to give positive feedback when all `pythonwhat` tests passed. If you do not use `success_msg()`, `pythonwhat` will generate a kind message itself :).

In all the test statements above, feedback messages will be automatically generated when something goes wrong. However, it is possible to manually set these feedback messages. For example, in the code below,

```python
Ex().check_object(undefined_msg="`x` is undefined!") \
    .has_equal_value(incorrect_msg="wrong value for `x`")
```

the automatic messages for when `x` is undefined or incorrect are replaced with manual feedback. Now, if students submit `x = 4` instead of `x = 5`, they will see the message, "wrong value for `x`". Finally, notice that you can use Markdown syntax inside the strings here.

The same holds for `test_output_contains()`: you can use the `no_output_msg` argument to specify a custom message. For more information on all the different arguments you can set in the different `pythonwhat` functions, have a look at the articles in this wiki, describing them in detail.

Next Steps
----------

Test functions in pythonwhat are broken into 4 groups:

* [Simple tests](simple_tests/index.rst): look at, e.g., the output produced by an entire code submission.
* [Part checks](part_checks.rst): focus on specific pieces of code, like a particular for loop.
* [Expression tests](expression_tests.md): combined with part checks, these run pieces of code and evaluate the outcome.
* [Logic tests](logic_tests/index.rst): these allow logic like an or statement to be used with SCTs.
