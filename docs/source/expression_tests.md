Expressions
===========

Expression tests run pieces of the student and solution code, and then check the resulting value, printed output, or errors they produce.

`has_equal` Syntax
------------------

Once student/submission code has been selected using a check test, we can run it using one of three functions.
They all take the same arguments, and run the student and submission code in the same way.
However, they differ in how they compare the outcome:

* has_equal_value - compares the value returned by the code.
* has_equal_output - compares printed output.
* has_equal_error - compares any errors raised.

```eval_rst
.. autofunction:: pythonwhat.check_funcs.has_expr
```

### Basic Usage

#### Running the whole code submission 

In the example below, we re-run the entire student and submission code, and check that they print out the same output.


    *** =solution
    ```{python}
    x = [1,2,3]
    print(x)
    ```

    *** =sct
    ```{python}
    # run all code and compare output
    Ex().has_equal_output()
    # equivalent to
    # Ex().test_output_contains('[1,2,3]')
    ```

Note that while we could have used `test_output_contains` to verify that the student printed `"[1, 2, 3]"`,
using `has_equal_output` simply requires that the student output matches the solution output.

#### Running part of the code

Combining an expression test with part checks will run only a piece of the submitted code.
The example below first uses `has_equal_value` to run an entire if expression, and then to run only its body.

    *** =solution
    ```{python}
    x = [1,2,3]
    sum(x) if x else None
    ```
    
    *** =sct
    ```{python}
    # test body of if expression
    (Ex().check_if_exp(0)     # focus on if expression
         .has_equal_value()   # run entire if expression, check value
         .check_body()        # focus on body "sum(x)"
         .has_equal_value()   # run body, check value
         )
    ```
    
Note that commands chaining off of `has_equal_value` behave as they would have if `has_equal_value` weren't used.
In this sense, the `check_body` behaves the same in

```python
Ex().check_if_exp(0).has_equal_value().check_body()
```

and

```python
Ex().check_if_exp(0).check_body()
```

in that it gets "sum(x)" in the solution code (and its corresponding code in the submission).

###  Context Values

Suppose we want the student to define a function, that loops over the elements in a dictionary, and prints out each key and value, as follows:

    *** =solution
    ```{python}
    def print_dict(my_dict):
        for key, value in my_dict.items():
            print(key + " - " + str(value))
    ```

An appropriate SCT for this exercise could be the following (for clarity, we're not using any default messages):

    *** =sct
    ```{python}
    # get for loop code, set context for my_dict argument
    for_loop = (Ex()
         .check_function_def('print_dict')          # ensure 'print_dict' is defined
         .check_body()                              # get student/solution code in body
         .set_context(my_dict = {'a': 2, 'b': 3})   # set print_dict's my_dict arg
         .check_for_loop(0)                         # ensure for loop is defined
         )
    
    # test for loop iterator
    for_loop.check_iter().has_equal_value()         # run iterator (my_dict.items())
    # test for loop body
    for_loop.check_body().set_context(key = 'c', value = 3).has_equal_value()

    ```

Assuming the student coded the function in the exact same way as the solution, the following things happen:

- checks whether `print_dict` is defined, then gets the code for the function definition body.
- because `print_dict` takes an argument `my_dict`, which would be undefined if we ran the body code, `set_context` defines what `my_dict` should be when running the code. Note that its okay if the submitted code named the argument `my_dict` something else, since set_context matches submission / solution arguments up by position.

When running the bottom two SCTs for the for_loop

- `for_loop.check_iter().has_equal_value()` - runs the code for the iterator, `my_dict.items()` in the solution and its corresponding code in the submission, and compares the values they return.
- `for_loop.check_body().set_context(key = 'c', value = 3).has_equal_value()` - runs the code in the for loop body, `print(key + " - " + str(value))` in the solution, and compares outputs. 
  Since this code may use variables the for loop defined, `key` and `value`, we need to define them using `set_context`.

### How are Context Values Matched?

Context values are matched by position. For example, the submission and solution codes...

   *** =solution
   ```{python}
   for ii, x in enumerate(range(3)): print(ii)
   ```
   
   *** =submission
   ```{python}
   for jj, y in enumerate(range(3)): print(jj)
   ```

Using `Ex().check_for_loop(0).check_body().set_context(...)` will do the following...

```eval_rst
====================== ======================= ==========================
 statement              solution (ii, x)        submission (jj, y)
====================== ======================= ==========================
set_context(ii=1, x=2)  ii = 1, x = 2           jj = 1, y = 2
set_context(ii=1)       ii = 1, x is undefined  jj = 1, y is undefined
set_context(x=2)        ii is undefined, x = 2  jj is undefined, y = 2
====================== ======================= ==========================

.. note:: 
   
   If ::set_context:: does not define a variable, nothing is done with it.
   This means that in the code examples above, running the body of the for loop would call print with ::ii:: or ::jj:: left at 2 (the values they have in the solution/submission environments).
```

### pre_code: fixing mutations

Python code commonly mutates, or changes values within an object. 
For example, the variable `x` points to an object that is mutated every time a function is called.

```python
x = {'a': 1}

def f(d): d['a'] += 1

f(x)     # x['a'] == 2 now
f(x)     # x['a'] == 3 now
```

In this case, when `f` is run, it changes the contents of `x` as a side-effect and returns None.
When using SCTs that run expressions, mutations in either the solution or submission environment can cause very confusing results.
For example, calling `np.random.random()` will advance numpy's random number generator.
In the code below the random seed is set to 42, but the solution code advances the random generator further than the submission code. As a result the SCT will fail.

    *** =pre_exercise_code
    ```{python}
    import numpy as np
    np.random.seed(42)               # set random generator seed to 42
    ```

    *** =solution
    ```{python}
    if True: np.random.random()      # 1st random call: .37
    
    np.random.random()               # 2nd random call: .95
    ```
   
    *** =submission
    ```{python}
    if True: np.random.random()      # 1st random call: .37
     
    # forgot 2nd call to np.random.random()
    ```
   
    *** =sct
    ```{python}
    # Should pass but fails, because random generator has advanced
    # twice in solution, but only once in submission
    Ex().check_if_else(0).check_body().has_equal_value()
    ```

In order to test random code, the random generator needs to be at the same state between submission and solution environments.
Since their generators can be thrown out of sync, the most reliable way to do this is to set the seed using the `pre_code` argument to `has_equal_value`.
In the case above, the sct may be fixed as follows

   *** =sct
   ```{python}
   Ex().check_if_else(0).check_body().has_equal_value(pre_code = "np.random.seed(42)")
   ```

More generally, it can be helpful to define a pre_code variable to use before expression tests...

   *** =sct
   ```{python}
   pre_code = """
   np.random.seed(42)
   """
   
   Ex().has_equal_output(pre_code=pre_code)
   Ex().check_if_else(0).check_body().has_equal_value(pre_code = pre_code)
   ```

### extra_env: fixing slow SCTs

The `extra_env` argument is similar to `pre_code`, in that you can (re)define objects in the student and submission environment before running an expression.
The difference is that, rather than passing a string that is executed in each environment, extra_env lets you pass objects directly.
For example, the two SCTs below are equivalent...

   *** =sct
   ```{python}
   Ex().has_equal_value(pre_code="x = 10")
   Ex().has_equal_value(extra_env = {'x': 10})
   ```

In practice they can often be used interchangably.
However, one area where `extra_env` may shine is in mocking up data objects before running tests.
For example, if the SCT below didn't use extra_env, then it would take a long time to run.

   *** =pre_exercise_code
   ```{python}
   a_list = list(range(10000000))
   ```

   *** =solution
   ```{python}
   print(a_list[1])
   ```

   *** =sct
   ```{python}
   extra_env = {'a_list': list(range(10))}
   Ex().has_equal_output(extra_env = extra_env)
   ```
   
The reason extra_env is important here, is that pythonwhat tries to make a deepcopy of lists, so that course developers don't get bit by unexpected mutations.
However, the larger the list, the longer it takes to make a deepcopy.
If an SCT is running slowly, there's a good chance it uses a very large object that is being copied for every expression test.

### name: run tests after expression

### expr_code: change expression

The `expr_code` argument takes a string, and uses it to replace the code that would be run by an expression test.
For example, the following SCT simply runs `len(x)` in the solution and student environments.
   
    *** =solution
    ```{python}
    # keep x the same length
    x = [1,2,3]
    ```

    *** =SCT
    ```{python}
    Ex().has_equal_value(expr_code="len(x)")
    ```
   
```eval_rst
.. note::

   Using `expr_code` does not change how expression tests perform highlighting. 
   This means that `Ex().for_loop(0).has_equal_value(expr_code="x[0]")` would highlight the body of the checked for loop.
```

`call` Syntax
-------------

Testing a function definition or lambda may require calling it with some arguments.
In order to do this, use the `call()` SCT.
There are two ways to tell it what arguments to pass to the function/lambda,

* `call("f (1, 2, x = 3)")` - as a string, where `"f"` gets substituted with the function's name.
* `call([1,2,3])` - as a list of positional arguments.

Below, two alternative ways of specifying the arguments to pass are shown.

    *** =solution
    ```{python}
    def my_fun(x, y = 4, z = ('a', 'b'), *args, **kwargs):
        return [x, y, *z, *args]
    ```
 
    *** =sct
    ```{python}
    Ex().check_function_def('my_fun').call("f(1, 2, (3,4), 5, kw_arg='ok')")  # as string
    Ex().check_function_def('my_fun').call([1, 2, (3,4), 5])                  # as list
    ```

```eval_rst
.. note::

   Technically, you can get crazy and replace the list approach with a dictionary of the form ``{'args': [POSARG1, POSARG2], 'kwargs': {KWARGS}}``.
```

### Additional Parameters

In addition to its first argument, `call()` accepts all the parameters that the expression tests above can (i.e. `has_equal_value`, `has_equal_error`, `has_equal_output`).
The function call is run at the point where these functions would evaluate an expression.
Moreover, setting the argument `test` to either "value", "output", or "error" controls which expression test it behaves like.

For example, the SCT below shows how to run some `pre_code`, and then evaluate the output of a call.

```
Ex().check_function_def('my_fun').call("f(1, 2)", test="output", pre_code="x = 1")
```

```eval_rst
.. _managing-processes:
```


Managing Processes
-----------------

As mentioned on the [Homepage](Home.md), DataCamp uses two separate processes. One process to run the solution code, and one process to run the student's submission. This way, `pythonwhat` has access to the 'ideal ending scenario' of an exercises; this makes it easier to write SCTs. Instead of having to specify which value an object should be, we can have `test_object()` look into the solution process and compare the object in that process with the object in the student process.

### Problem

Fetching Python objects or the results of running expressions inside a process is not straightforward. To be able to pull data from a process, Python needs to 'pickle' and 'unpickle' files: it converts the Python objects to a byte representation (pickling) that can be passed between processes, and then, inside the process that you want to work with the object, builds up the object from the byte representation again (unpickling).

For the majority of Python objects, this conversion to and from a byte representation works fine, but for some objects, it doesn't. Even `dill`, and improved implementation of `pickle` that's being used in `pythonwhat`, doesn't flawlessly convert all Python objects out there.

If you're writing an SCT with functions that require work in the solution process, such as `test_object()`, `test_function()`, and `test_function_definition()`, and then upload the exercise and test it on DataCamp, that you get backend errors that look like this:

        ... dilling inside process failed - write manual converter
        ... undilling of bytestream failed - write manual converter

The first error tells you that 'dilling' - or 'pickling', converting the object to a bytestream representation, failed. The second error tells you that 'undilling' - or 'unpickling', converting the byte representation back to a Python object, failed. These errors will typically occur if you're dealing with exotic objects, such as objects that interface to files, connections to databases, etc.

### Solution

To be able to handle these errors, `pythonwhat` allows you to write your own converters for Python objects. Say, for example, that you're writing an exercise to import Excel data into Python, and you're using the `pandas` package. This is the solution and the corresponding SCT:

        *** =solution
        ```{python}
        import pandas as pd
        xl = pd.ExcelFile('battledeath.xlsx')
        ```

        *** =sct
        ```{python}
        Ex().test_object('xl')
        ```

Suppose now that objects such as `xl`, which are of the type `pandas.io.excel.ExcelFile`, can't be properly dilled and undilled. (Note: because of hardcoded converters inside `pythonwhat`, they can, see below). To make sure that you can still use `test_object('xl')` to test the equality of the `xl` object between student and solution process, you can manually define a converter with the `set_converter()` function. You can extend the SCT as follows:

        *** =sct
        ```
        def my_converter(x):
            return(x.sheet_names)
        set_converter(key = "pandas.io.excel.ExcelFile", fundef = my_converter)
        Ex().test_object('xl')
        ```

With a lambda function, it's even easier:

        *** =sct
        ```
        set_converter(key = "pandas.io.excel.ExcelFile", fundef = lambda x: x.sheet_names)
        Ex().test_object('xl')
        ```

The first arguemnt of `set_converter()`, the `key` takes the type of the object you want to add a manual converter for as a string. The second argument, `fundef`, takes a function definition, taking one argument and returning a single object. This function definition converts the exotic object into something more standard. In this case, the function converts the object of type `pandas.io.excel.ExcelFile` into a simple list of strings. A list of strings is something that can easily be converted into a bytestream and back into a Python object again, hence solving the problem.

If you want to reuse the same manual converter over different exercises, you'll have to use `set_converter()` in every SCT.

### Hardcoded converters

Some converters will be required often. For example, the result of calling `.keys()` and `.items()` on dictionaries can't be dilled and undilled without extra work. To handle these common yet problematic situations, `pythonwhat` features a list of hardcoded converters. This list is [available in the source code](https://github.com/datacamp/pythonwhat/blob/master/pythonwhat/converters.py); feel free to do a pull request if you want to add more converts to this list. This will reduce the amount of code duplication you have to do if you want to reuse the same converter in different exercises.

### Custom Equality

The `set_converter()` function opens up possibilities for objects that can actually be dilled and undilled perfectly fine. Say you want to test a `numpy` array, but you only want to check only if the dimensions of the array the student codes up match those in the solution process. You can easily write a manual converter that overrides the typical dilling and undilling of Numpy arrays, implementing your custom equality behavior:

        *** =solution
        ```{python}
        import numpy as np
        my_array = np.array([[1,2], [3,4], [5,6]])
        ```

        *** =sct
        ```
        set_converter(key = "numpy.ndarray", fundef = lambda x: x.shape)
        Ex().test_object('my_array')
        ```

Both of the following submissions will be accepted by this SCT:

- `my_array = np.array([[1,2], [3,4], [5,6]])`
- `my_array = np.array([[0,0], [0,0], [5,6]])`




