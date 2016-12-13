test comprehensions
-------------------

    def test_list_comp(index=1,
                       not_called_msg=None,
                       comp_iter=None,
                       iter_vars_names=False,
                       incorrect_iter_vars_msg=None,
                       body=None,
                       ifs=None,
                       insufficient_ifs_msg=None,
                       expand_message=True)

    def test_generator_exp(index=1,
                           not_called_msg=None,
                           comp_iter=None,
                           iter_vars_names=False,
                           incorrect_iter_vars_msg=None,
                           body=None,
                           ifs=None,
                           insufficient_ifs_msg=None,
                           expand_message=True)

    def test_dict_comp(index=1,
                       not_called_msg=None,
                       comp_iter=None,
                       iter_vars_names=False,
                       incorrect_iter_vars_msg=None,
                       key=None,
                       value=None,
                       ifs=None,
                       insufficient_ifs_msg=None,
                       expand_message=True)

Currently, functionality to test list comprehensions, generator expressions and dictionary comprehensions is implemented. If you look at the signatures, you'll see that the arguments for `test_list_comp()` and `test_generator_exp()` are identical. Syntactically, there is close to no difference between list comprehensions and generator expressions, so all tests and settings apply for both cases. For `test_dict_comp()` there's only a small difference: the arguments `key` and `value` instead of the `body` argument, so that you can test the `key` part of the dictionary comprehension seperately from the `value` comprehension.

The above functions work pretty similarly to `test_for_loop()`, with some additions and customizations here and there. Let's go over the argments:

- `index`: the number of the comprehension in the submission to test. (this is specific to each comprehension, if there's one list and one dict comprehension you need `index=1` twice.)
- `not_called_msg`: Custom message in case the comprehension was not coded (or there weren't enough comprehensions).
- `comp_iter`: sub SCT to check the sequence part of the comprehension. Specify this through another function definition or a lambda function.
- `iter_vars_names`: whether or not the iterator variables should match the ones in the solution.
- `incorrect_iter_vars_msg`: Custom message in case the iterator variables don't match the solution (if `iter_vars_names` is `True`) or if the number of iterator variables doesn't correspond to the solution.
- `body`, `key`, `value`: sub SCTs to check the body part (for list comps and generator expressions) or the key and value part of a dictionary comprehension.
- `ifs`: list of sub-SCTs to check each of the ifs specified inside the comprehension. If you specify `ifs`, make sure that the number of sub-SCTs corresponds exactly to the number of ifs that are in the solution.
- `insufficient_ifs`: custom message in case the student coded less ifs than the corresponding comp in the solution.
- `expand_message`: whether or not to expand feedback messages from sub-SCTs with more information about where in the list comprehension they occur.

### Example 1: List comprehension

Suppose you want the student to code a list comprehension like below:

    *** =solution
    ```{python}
    x = {'a': 2, 'b':3, 'c':4, 'd':'test'}
    [key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int)]
    ```

The following SCT will test several parts of this list comprehension, and relies on automatic feedback messages everywhere:

    *** =sct
    ```{python}
    test_list_comp(index=1,
               comp_iter=lambda: test_expression_result(),
               iter_vars_names=True,
               body=lambda: test_expression_result(context_vals = ['a', 2]),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False]),
                    lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False])])
    ```

By setting `iter_vars_names` to `True`, `pythonwhat` will check that the student actually used the iterator variables `key` and `val`. Notice that in the sub SCT for the body, `context_vals` are used to set the `key` and `val` iterator variables before the expression is tested. This is similar to how things work in `test_for_loop()`. Notice also that inside the list of if sub-SCTs, `do_eval` is false, because the values `key` and `val` are not available there (setting context vals is currently only possible inside `test_expression_*()` functions).

`test_list_comp()` will generate a bunch of meaningful automated messages depending on which error the student made:

    submission: <empty>
    feedback: "The system wants to check the first list comprehension you defined but hasn't found it."

    submission: [key for key in x.keys()]
    feedback: "Check your code in the iterable part of the first list comprehension. Unexpected expression: expected `dict_items([('a', 2), ('b', 3), ('c', 4), ('d', 'test')])`, got `dict_keys(['a', 'b', 'c', 'd'])` with values."

    submission: [a + str(b) for a,b in x.items()]
    feedback: "Have you used the correct iterator variables in the first list comprehension? Make sure you use the correct names!"

    submission: [key + '_' + str(val) for key,val in x.items()]
    feedback: "Check your code in the body of the first list comprehension. Unexpected expression: expected `a2`, got `a_2` with values."

    submission: [key + str(val) for key,val in x.items()]
    feedback: "Have you used 2 ifs inside the first list comprehension?"

    submission: [key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test')]
    feedback: "Check your code in the first if of the first list comprehension. Have you called `isinstance()`?"

    submission: [key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test')]
    feedback: "Check your code in the second if of the first list comprehension. Have you called `isinstance()`?"

    submission: [key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str)]
    feedback: "Check your code in the second if of the first list comprehension. Did you call `isinstance()` with the correct arguments?"

    submission: [key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]
    feedback: "Great work!"

NOTE: the "check your code in the ... of the first list comprehension" parts are included because `expand_message = True`.

You can also update SCT to override all automatically generated messages, either inside `test_list_comp()` itself or inside the sub-SCTs:

    *** =sct
    ```{python}
    test_list_comp(index=1,
               not_called_msg='notcalled',
               comp_iter=lambda: test_expression_result(incorrect_msg = 'iterincorrect'),
               iter_vars_names=True,
               incorrect_iter_vars_msg='incorrectitervars',
               body=lambda: test_expression_result(context_vals = ['a', 2], incorrect_msg = 'bodyincorrect'),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False], not_called_msg = 'notcalled1', incorrect_msg = 'incorrect2'),
                    lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False], not_called_msg = 'notcalled2', incorrect_msg = 'incorrect2')],
               insufficient_ifs_msg='insufficientifs')
    ```

In this case, you get the following feedback for different submissions:

    submission:
    feedback: "notcalled"

    submission: [key for key in x.keys()]
    feedback: "Check your code in the iterable part of the first list comprehension. iterincorrect"

    submission: [a + str(b) for a,b in x.items()]
    feedback: "incorrectitervars"

    submission: [key + '_' + str(val) for key,val in x.items()]
    feedback: "Check your code in the body of the first list comprehension. bodyincorrect"

    submission: [key + str(val) for key,val in x.items()]
    feedback: "insufficientifs"

    submission: [key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test')]
    feedback: "Check your code in the first if of the first list comprehension. notcalled1"

    submission: [key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test')]
    feedback: "Check your code in the second if of the first list comprehension. notcalled2"

    submission: [key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str)]
    feedback: "Check your code in the second if of the first list comprehension. incorrect2"

    submission: [key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]
    feedback: "Great work!"


### Example 2: Generator Expressions

An example here won't be necessary, because it works the exact same way as in Example 1, with the only difference that in automated feedback, "list comprehension" is replaced with "generator expression".

### Example 3: Dictionary Comprehensions

Suppose you want the student to code a dictionary comprehension like below:

    *** =solution
    ```{python}
    x = {'a': 2, 'b':3, 'c':4, 'd':'test'}
    [key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int)]
    ```

The following SCT will test several parts of this list comprehension, and relies on automatic feedback messages everywhere:

    *** =sct
    ```{python}
    test_list_comp(index=1,
               comp_iter=lambda: test_expression_result(),
               iter_vars_names=True,
               body=lambda: test_expression_result(context_vals = ['a', 2]),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False]),
                    lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False])])
    ```

Again, customized messages are generated for different cases:

    submission:
    feedback: "The system wants to check the first dictionary comprehension you defined but hasn't found it."

    submission: { a:a for a in lst[1:2] }
    feedback: "Check your code in the iterable part of the first dictionary comprehension. Unexpected expression: expected `['this', 'is', 'a', 'list']`, got `['is']` with values."

    submission: { a:a for a in lst }
    feedback: "Have you used the correct iterator variables in the first dictionary comprehension? Make sure you use the correct names!"

    submission: { el + 'a':str(el) for el in lst }
    feedback: "Check your code in the key part of the first dictionary comprehension. Unexpected expression: expected `a`, got `aa` with values."

    submission: { el:str(el) for el in lst }
    feedback: "Check your code in the value part of the first dictionary comprehension. Unexpected expression: expected `1`, got `a` with values."

    submission: { el:len(el) for el in lst }
    feedback: "Have you used 1 ifs inside the first dictionary comprehension?"

    submission: { el:len(el) for el in lst if isinstance('a', str)}
    feedback: "Check your code in the first if of the first dictionary comprehension. Did you call `isinstance()` with the correct arguments?"

    submission: { el:len(el) for el in lst if isinstance(el, str)}
    feedback: "Great work!"


