test_with
---------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_with.test_with
```
    
    def test_with(index,
                  context_vals=False,
                  context_tests=None,
                  body=None,
                  undefined_msg=None,
                  context_vals_len_msg=None,
                  context_vals_msg=None,
                  expand_message=True)

In Python, one can build so-called context managers with the `with` statement. 

Have a look at an example of such a context manager:

    with open('something.txt') as file1, open('something_else.csv') as file2: # the contexts
        # body of the with statement
        # do something with file1 and file2
        # ...

Two important parts can be distinguished: the contexts that are being opened and the body, in which operations are done with these contexts. In this example, two contexts are defined: `open('something.txt')` and `open('something_else.csv')`. The context can be given names (this is optional). In the example, the first one will be called `file1` after the `with` statement, and the second one `file2`. 

`test_with()` is written to allow you to test all these parts of the `with` statement separately.

### Example 1

Suppose you want the student to code something as follows:
    
    *** =solution
    ```{python}
    with open('moby_dick.txt') as moby, open('lotr.txt') as lotr:
        print("First line of Moby Dick: %r." % moby.readline())
        print("First line of The Lord of The Rings: The Two Towers: %r." % lotr.readline())


In this case you want to test two things: you want the student to open up the correct context and you want them to print out the correct information. Let's assume that how the context are named is not important to you. The solution uses `moby` and `lotr`, but the student can use any name he or she wants. Note these names will not be tested by default, but you can change that by setting `context_vals = True`. 

In the SCT, we specify a sub-SCT for `context_tests` and for `body`. The former tests the contexts, the latter tests the body. As before, you can specify these sub-SCTs through lambda functions or a separate function definition:

    *** =sct
    ```{python}
    def test_with_body():
        test_function('print', 1)
        test_function('print', 2)

    test_with(1,
              context_tests = [
                  lambda: test_function('open'),
                  lambda: test_function('open')
             ],
             body = test_with_body)
    ```

Different from before, htough, `context_tests` expects a list of lambda functions or customly defined functions. The index in this list of functions represents the context against which the SCTs will be tested. The first lambda/custom function in `context_tests` will be tested against the first context. The second lambda/custom function in `context_tests` will be tested against the second context. If only one function is given in `context_tests`, only the first context will be tested. The `body` argument requires one lambda/custom function to be passed, this contains the sub-SCT that is run against the `with` statements' body.
