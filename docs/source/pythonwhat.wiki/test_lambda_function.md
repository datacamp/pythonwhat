test_lambda_function
--------------------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_lambda_function
    :members:
```

    def test_lambda_function(index,
                             arg_names=True,
                             arg_defaults=True,
                             body=None,
                             results=None,
                             errors=None,
                             not_called_msg=None,
                             nb_args_msg=None,
                             arg_names_msg=None,
                             arg_defaults_msg=None,
                             wrong_result_msg=None,
                             no_error_msg=None,
                             expand_message=True)

With `test_function_definition()`, you can only test user-defined functions that have a name. There is an important class of functions in Python that go by the name of lambda functions. These functions are anonymous, so they don't necessarily require a name. To be able to test user-coded lambda functions, the `test_lambda_function()` is available. If you're familiar with `test_function_definition()`, you'll notice some similarities. However, instead of the `name`, you now have to pass the `index`; this means you have to specify the lambda function definition to test by number (test the first, second, third ...). Also, because we don't necessarily have an object represents a lambda function (because it can be anonymous), some tricky things are required to correctly specify the arguments `errors` and `results`; the example will give more details.

### Example 1

Suppose we want the student to code a lambda function that takes two arguments, `word` and `echo`, the latter of which should have default value 1. The lambda function should return the product of `word` and `echo`. A solution to this challenge could be the following:

    *** =solution
    ```{python}
    echo_word = lambda word, echo = 1: word * echo
    ```

To test this lambda function definition, you can use the following SCT:

    *** =sct
    ```
    test_lambda_function(1,
                     body = lambda: test_student_typed('word'),
                     results = ["lam('test', 2)"],
                     errors = ["lam('a', '2')"])
    ```

With `1`, we tell `pythonwhat` to test the first lambda function it comes across. Through body, we can specify sub-SCTs to be tested on the body of the lambda function (similar to how `test_function_definition` does it). With `results` and `errors`, you can test the lambda function definition for different input arguments. Notice here that you have to specify a list of function calls as a string. The function you have to call is `lam()`; behind the scenes, this `lam` will be replaced by the actual lambda function the student and solution defined. This means that `lam('test', 2)` will be converted into:

    ```
    (lambda word, echo = 1: word * echo)('test', 2)
    ```

That way, the system can run the function call, and compare the results between function and solution. Things work the same way for `errors`.

As usual, the `test_lambda_function()` will generate a bunch of meaningful automated messages depending on which error the student made (you can override all these messages through the `*_msg` argument):

    submission: <empty>
    feedback: "The system wants to check the first lambda function you defined but hasn't found it."

    submission: echo_word = lambda wrd: wrd * 1
    feedback: "You should define the first lambda function with 2 arguments, instead got 1."

    submission: echo_word = lambda wrd, echo: wrd * echo
    feedback: "In your definition of the first lambda function, the first argument should be called <code>word</code>, instead got <code>wrd</code>."

    submission: echo_word = lambda word, echo = 2: word * echo
    feedback: "In your definition of the first lambda function, the second argument should have <code>1</code> as default, instead got <code>2</code>."

    submission: echo_word = lambda word, echo = 1: 2 * echo
    feedback: "In your definition of the first lambda function, could not find the correct pattern in your code."

    submission: echo_word = lambda word, echo = 1: word * echo + 1
    feedback: "Calling the the first lambda function with arguments <code>('test', 2)</code> should result in <code>testtest</code>, instead got an error."

    submission: echo_word = lambda word, echo = 1: word * echo * 2
    feedback = "Calling the first lambda function with arguments <code>('test', 2)</code> should result in <code>testtest</code>, instead got <code>testtesttesttest"

    submission: echo_word = lambda word, echo = 1: word * int(echo)
    feedback: "Calling the first lambda function with the arguments <code>('a', '2')</code> doesn't result in an error, but it should!"

    submission: echo_word = lambda word, echo = 1: word * echo
    feedback: "Great job!" (pass)


### What about testing usage?

This is practically impossible to do in a robust way; we suggest you do this in an indirect way (checking the output that should be generated, checking the object that should be created, etc).

**NOTE**: Behind the scenes, `pythonwhat` has to fetch the value of objects from sub-processes. The required 'dilling' and 'undilling' can cause issues for exotic objects. For more information on this and possible errors that can occur, read the [Processes article](../expression_tests.md).
