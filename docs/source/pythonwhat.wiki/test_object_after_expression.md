test_object_after_expression
----------------------------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_object_after_expression
    :members:
```

    test_object_after_expression(name,
                                 extra_env=None,
                                 context_vals=None,
                                 undefined_msg=None,
                                 incorrect_msg=None,
                                 eq_condition="equal",
                                 pre_code=None,
                                 keep_objs_in_env=None)

`test_object_after_expression()` is a function that is primarily used to check the correctness of the body of control statements. Through `extra_env` and `context_vals` you can adapt the student/solution environment with manual elements. Next, the 'currently active expression tree', such as the body of a for loop, is executed, and the resulting environment is inspected. This is done for both the student and the solution code, and afterwards the value of the object that you specify in `name` is checked for equality. With pre_code, you can prepend the execution of the default expression tree with some extra code, for example to set some variables.

### Example 1: Function defintion

Suppose you want to student to code up a function `shout()`, that adds three exclamation marks to every word you pass it:

    *** =solution
    ```{python}
    def shout(word):
        shout_word = word + '!!!'
        return shout_word
    ```

To test whether the student did this appropriately, you want to first test whether `shout` is a user-defined function, and then whether inside the function, a new variable `shout_word` is created. Finally, you also want to check whether the result of calling `shout('hello')` is correct. The following SCT will do that for us:

    *** =sct
    ```{python}
    test_function_definition('shout',
                             body = test_object_after_expression('shout_word', context_vals = ['anything']),
                             results = [('hello')])
    ```

Let's focus on the `body` argument of `test_function_definition()` here, that uses `test_object_after_expression()`. For the other elements, refer to the [`test_function_definition()`](https://github.com/datacamp/pythonwhat/wiki/test_function_definition) article.

The first argument of `test_object_after_expression()` tells the system to check the value of `shout_word` after executing the body of the function definition. Which part of the code to execute, the 'expression', is implicitly specified by `pythonwhat`. However, to run correctly, this expression has to know what `word` is. You can specify a value of `word` through the `context_vals` argument. It's a simple list: the first element of the list will be the value for the first argument of the function definition, the second element of the list will be the value for the second argument of the list, and so on. Here, there's only one argument, so a list with a single element, a string (that will be the value of the `word` variable), suffises.

`test_object_after_expression()` will execute the expression, and run it on the solution side and the student side. On the solution side, the value of `shout_word` after the execution will be `'anything!!!'`. If the value on the student code is the same, we can rest assured that `shout_word` has been appropriately defined by the student and the test passes.

### Example 2: for loop

Suppose you want the student to build up a dictionary of word counts based on a list, as follows:

    *** =solution
    ```{python}
    words = ['it', 'is', 'a', 'the', 'is', 'the', 'a', 'the', 'it']
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    ```

To check whether the `counts` list was correctly built, you can simply use `test_object()`, but you can also go deeper if it goes wrong. This calls for a `test_correct()` in combination with `test_object()` and `test_for()`, that in its turn uses `test_object_after_expression()`:


    ``` =solution
    def check_test():
        test_object('counts')

    def diagnose_test():
        body_test():
            test_object_after_expression('counts',
                                         extra_env = {'counts': {'it': 1}},
                                         context_vals = ['it'])
            test_object_after_expression('counts',
                                         extra_env = {'counts': {'it': 1}},
                                         context_vals = ['is'])
        test_for_loop(index = 1,
                      test = test_expression_result(), # Check if correct iterable used
                      body = body_test)

    test_correct(check_test, diagnose_test)
    ```

Let's focus on the `body_test` for the for loop. Here, we're using `test_object_after_expression()` twice.

In the first function call, we override the environment so that `counts` is a dictionary with a single key and value. Also, the context value, `word` in this case (the iterator of the `for` loop), is set to `it`. In this case, the body of the for loop - making abstraction of the if-else test - should increment the value of the value, without adding a new key.

In the second function call, we override the environment so that `counts` is again a dictionary with a single key and value. This time, the context value is set to `is`, so a value that is not yet in the `counts` dictionary, so this should lead to a `counts` dictionary with two elements.

As in the first example, `test_object_after_expression()` sets the environment variables and context values, runs the expression (in this case the entire body of the `for` loop), and then inspects the value of `counts` after this expression. The combination of the two `test_object_after_expression()` calls here, will indirectly check whether both the if and else part of the body has been correctly implemented.


