test_while_loop
---------------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_while_loop
    :members:
```

    test_while_loop(index=1,
                    test=None,
                    body=None,
                    orelse=None,
                    expand_message=True)

Since a lot of the logic of `test_if_else()` and `test_for_loop()` can be applied to `test_while_loop()`, this article is limited to an example. For more info see the wiki on `test_if_else()` and `test_for_loop()`, or the documentation of `test_while_loop()`.

    *** =solution
    ```{python}
    a = 10
    while a > 5:
      print("%s is bigger than 5" % a)
      a -= 1
    ```

    *** =sct
    ```{python}
    def sct_on_condition_test():
      test_expression_result({"a": 4})
      test_expression_result({"a": 5})
      test_expression_result({"a": 6})

    test_while_loop(index = 1,
                    test = sct_on_condition_test,
                    body = lambda: test_expression_output({"a":4}))    
    ```

    
