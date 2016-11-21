Processes
=========

As mentioned on the [wiki Homepage](https://github.com/datacamp/pythonwhat/wiki), DataCamp uses two separate processes. One process to run the solution code, and one process to run the student's submission. This way, `pythonwhat` has access to the 'ideal ending scenario' of an exercises; this makes it easier to write SCTs. Instead of having to specify which value an object should be, we can have `test_object()` look into the solution process and compare the object in that process with the object in the student process.

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
        test_object('xl')
        ```

Suppose now that objects such as `xl`, which are of the type `pandas.io.excel.ExcelFile`, can't be properly dilled and undilled. (Note: because of hardcoded converters inside `pythonwhat`, they can, see below). To make sure that you can still use `test_object('xl')` to test the equality of the `xl` object between student and solution process, you can manually define a converter with the `set_converter()` function. You can extend the SCT as follows:

        *** =sct
        ```
        def my_converter(x):
            return(x.sheet_names)
        set_converter(key = "pandas.io.excel.ExcelFile", fundef = my_converter)
        test_object('xl')
        ```

With a lambda function, it's even easier:

        *** =sct
        ```
        set_converter(key = "pandas.io.excel.ExcelFile", fundef = lambda x: x.sheet_names)
        test_object('xl')
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
        test_object('my_array')
        ```

Both of the following submissions will be accepted by this SCT:

- `my_array = np.array([[1,2], [3,4], [5,6]])`
- `my_array = np.array([[0,0], [0,0], [5,6]])`




