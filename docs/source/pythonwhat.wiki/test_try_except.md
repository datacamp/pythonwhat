test_try_except
---------------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_try_except
    :members:
```

    def test_try_except(index=1,
                        not_called_msg=None,
                        body=None,
                        handlers={},
                        except_missing_msg = None,
                        orelse=None,
                        orelse_missing_msg=None,
                        finalbody=None,
                        finalbody_missing_msg=None,
                        expand_message=True)

With `test_try_except`, you can check whether the student correctly coded a `try-except` block.

As usual, `index` controls which try-except block to check. With `not_called_msg` you can choose a custom message to override the automatically defined message in case not enough try-except blocks weren't found in the student code. `body` is a sub-sct to test the code of the `try` block. `orelse` and `finalbody` work the same way, but here there are also `_msg` arguments to provide custom messages in case these parts ar missing. Finally, there's also `handlers` and `except_missing_msg`. `handlers` should be a dictionary, where the keys are the error classes you expect the student to capture (for the general `except:`, use `'all'`), and the values are sub-SCTs for each of these `except` blocks. An `except` block is only checked for existence and correctness if you mention it inside `handlers`. If it is not available, an automatic message will be generated, but this can ge overriden with `expect_missing_msg`.


Note: For more information on sub-SCTs, visit [part checks](../part_checks.rst).

### Example 1

Suppose you want to student to code up the following (completely useless) piece of Python code:

    *** =solution
    ```{python}
    try:
        x = max([1, 2, 'a'])
    except TypeError as e:
        x = 'typeerror'
    except ValueError:
        x = 'valueerror'
    except (ZeroDivisionError, IOError) as e:
        x = e
    except :
        x = 'someerror'
    else :
        passed = True
    finally:
        print('done')
    ```

To test each and every part of this model solution, you can use the following SCT:

    *** =sct
    ```{python}
    import collections
    handlers = collections.OrderedDict()
    handlers['TypeError'] = lambda: test_object_after_expression('x')
    handlers['ValueError'] = lambda: test_object_after_expression('x')
    handlers['ZeroDivisionError'] = lambda: test_object_after_expression('x', context_vals = ['anerror'])
    handlers['IOError'] = lambda: test_object_after_expression('x', context_vals = ['anerror'])
    handlers['all'] = lambda: test_object_after_expression('x')
    test_try_except(index = 1,
                    body = lambda: test_function("max"),
                    handlers = handlers,
                    orelse = lambda: test_object_after_expression('passed'),
                    finalbody = lambda: test_function('print'))
    ```

Notice that:

- We use the `OrderedDict()` from the `collections` module so that the dictionary we pass in the `handlers` argument is always gone through in the same order.
- We can use `context_vals` to initalize the context value, `e` in this case.

