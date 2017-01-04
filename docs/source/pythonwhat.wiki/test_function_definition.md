test_function_definition
------------------------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_function_definition
    :members:
```

    def test_function_definition(name,
                                 arg_names=True,
                                 arg_defaults=True,
                                 body=None,
                                 results=None,
                                 outputs=None,
                                 errors=None,
                                 not_called_msg=None,
                                 nb_args_msg=None,
                                 other_args_msg=None,
                                 arg_names_msg=None,
                                 arg_defaults_msg=None,
                                 wrong_result_msg=None,
                                 wrong_output_msg=None,
                                 no_error_msg=None,
                                 wrong_error_msg=None,
                                 expand_message=True):


In more advanced courses, you'll sometimes want students to define their own functions. With `test_function_definition()` it is possible to test such user-defined functions in a robust way. This function allows you to test four things:

1. The argument names of the function (including if the correct defaults are used)
2. The body of the functions (does it output correctly, are the correct functions used)
3. The return value with a certain input
4. The output value with a certain input

### Example 1

Say you want a student to write a very basic function to set numbers in a base from 1 up until 9 to a decimal. To not overcomplicate things you just ask them to implement the basic functionality; they don't have to catch any exceptions. A solution to the exercise can like like this:

    *** =solution
    ```{python}
    def to_decimal(number, base = 2):
        print("Converting %d from base %s to base 10" % (number, base))
        number_str = str(number)
        number_range = range(len(number_str))
        multipliers = [base ** ((len(number_str) - 1) - i) for i in number_range]
        decimal = sum([int(number_str[i]) * multipliers[i] for i in number_range])
        return decimal
    ```

You could test the function like this:

    *** =sct
    ```{python}
    # All of the following test_function_definition() functions are done on the same
    # function definition.

    # Test the function, see that the defaults of the arguments are the same.
    # For this function, we don't care about the argument names of the function.
    # Note: generally, we DO care about the names of the arguments, since they can
    # be used as keywords. arg_defaults and arg_names will be set to True by default.

    test_function_definition("to_decimal", arg_defaults = True, arg_names = False)

    # Here, a feedback message will be generated. You can overwrite this feedback
    # message by using:
    # test_function_definition("to_decimal", arg_defaults = True, arg_names = False,
    #     arg_defaults_msg = "Use the correct default argument values!")
    # In the following tests, I'll always use the standard feedback messages, remember they
    # can almost always be overwritten.

    # We want to test whether the function returns the correct things with certain inputs.

    test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
        results = [
            [1001101, 2],
            ]1212357, 8]
    )

    # This will run to_decimal(1001101, 2) and to_decimal(1212357, 8) in student and solution
    # process, and match the results. If they don't match, a feedback message will be generated.
    # Note: here we've set arg_defaults to False, because we already tested this in the first
    # test_function_definition.

    # We want to test the output of the function with certain inputs.

    test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
        outputs = [
            [1234, 6],
            [8888888, 9]
    )

    # This will run to_decimal(1234, 6) and to_decimal(8888888, 9) in solution and student
    # process and compare their printed output.

    # Finally, we might want them to use a certain function. For this we can do tests specifically
    # on the body of the function. Remember you can use lambda functions or custom functions for this
    # (also see wiki about test_if_else(), test_for_loop() and test_while_loop().

    test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
        body = lambda: test_function("sum", args = [], incorrect_msg = "you should use the `sum()` function."))

    # This will test the body of the function definition, and see if the function sum() is used.
    # Note that the generated feedback will be preceded by: 'In your definition of `to_decimal()`, ...'
    # So if the last test doesn't pass, this feedback will be generated:
    #     In your definition of `to_decimal()`, you should use the `sum()` function.
    ```

Pitfall: you have to watch out when using `test_function()` in a body test, you should never test arguments
that are only defined within the scope of the function (e.g. function parameters). This is the reason why
we used `args = []` in the last test, because the argument used in `sum()` can not be calculated to verify
in the global scope. This is something which would require architectural changes in the `pythonwhat` package.


### Example 2: User-defined errors

In some cases, you'll want the student to code resilience against incorrect inputs or behavior. To test this, you can use the `errors`, `no_error_msg` and `wrong_error_msg` arguments. The first is similar to `results`, and specifies the input arguments as a list of tuples or a list of lists, that have to generate an error. With `no_error_msg` you can control the message that is presented if running one of these argument sets does not generate an error, while it should. With `wrong_error_msg`, you control the message that is presented if the type of the error (or exception) that is thrown does not correspond to the type that is thrown when the function is called in the solution process.

Suppose you want the student to code up a function `inc`, that increments a number if it's positive. If it's not, you want the function to raise a `ValueError`. A solution could look like this:

    *** =solution
    ```{python}
    def inc(num):
        if num < 0:
            raise ValueError('num is negative')
        return(num + 1)
    ```

To test this, we can use the following SCT (we're only focussing on the `errors` part here; of course you can extend the `test_function_definition()` call with more checks on arguments, `results`, body, etc.):

    *** =sct
    ```{python}
    test_function_definition("inc", errors = [[-1]])
    ```

If the student submits the following code:

```
def inc(num):
    return(num + 1)
```

the SCT will see it's incorrect and throw the message: _Calling `inc(-1)` doesn't result in an error, but it should!_

If the student submits the following code:

```
def inc(num):
    if num < 0:
        raise NameError('num is negative')
    return(num + 1)
```

the SCT will see it's incorrect and throw the message: _Calling `inc(-1)` should result in a `ValueError`, instead got a `NameError`._

Currently, there isn't a way to test the actual message you pass with errors you raise.

### Example 3: `*args` and `**kwargs`

When defining a function in Python, it also possible to specify so-called 'unordered non-keyword arguments', with a `*`, and 'unordered keyword arguments'. Typically, these are called `args` and `kwargs` respectively, but this is not required.

Have a look at the following example:

    *** =solution
    ```{python}
    def my_fun(x, y = 4, z = ['a', 'b'], *args, **kwargs):
        k = len(args)
        l = len(kwargs)
        print("just checking")
        return k + l
    ```

An SCT to check this function definition:

    *** =sct
    ```{python}
    def inner_test():
        context = ['r', 's', ['c', 'd'], ['t', 'u'], {'a': 2, 'b': 3, 'd':4}]
        test_object_after_expression('k', context_vals = context)
        test_object_after_expression('l', context_vals = context)
    test_function_definition("my_fun", body = inner_test,
            results = [{'args': ['r', 's', ['c', 'd'], 't', 'u', 'v'], 'kwargs': {'a': 2, 'b': 3, 'd': 4}}],
            outputs = [{'args': ['r', 's', ['c', 'd'], 't', 'u', 'v'], 'kwargs': {'a': 2, 'b': 3, 'd': 4}}])
    ```

There are different things to note:

- By default, the names of the `*` argument and the `**` argument are checked, if they are defined in the solution. This is controlled through `arg_names`, just like for 'regular' arguments. To override the automatic message that is thrown if the `*` or `**` arg is not specified or not appropriately named, use `other_args_msg`.
- The `*` and `**` args are also part of the context values that you can specify in 'inner tests'. They are appended to the normal arguments: first the `*`, then the `**` argument. You can see in the `context` object, that the penultimate element is used to specify the `*args` argument, and the last element, a dictionary, is used to specify the `**` argument.
- Before, you saw that `results`, `outputs`, and `errors` should be a list of lists, where the inner list is the list of arguments. To also cater for explicitly keyworded arguments, you can also specify a list of dictionaries. Each dictionary represents one call of the user-defined fucntion and should contain two elements: `'args'` and `'kwargs'`. Behind the scenes, the function will be called as: `my_fun([*d['args'], **d['kwargs']])`, where `d` is the two-key dictionary.


### Sidenote

Behind the scenes, `pythonwhat` has to fetch the value of objects from sub-processes. The required 'dilling' and 'undilling' can cause issues for exotic objects. For more information on this and possible errors that can occur, read the [Processes article](../expression_tests.md).
