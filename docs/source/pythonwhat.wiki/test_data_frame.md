test_data_frame
---------------

    def test_data_frame(name,
                        columns=None,
                        undefined_msg=None,
                        not_data_frame_msg=None,
                        undefined_cols_msg=None,
                        incorrect_msg=None)

Test a pandas DataFrame. This methods makes it possible to test the columns of a DataFrame object independently. Only the contents will be tested. Customisable error messages are possible for when there is no object in the process with name `name`, for when that object is no pandas DataFrame, when there are columns you want to test for which are not defined and when some columns contain bad values. `columns` contains a list of column names, and defaults to `None`. If it's `None`, all columns that are found in the data frame created by the solution will be tested.

### Example 1

Suppose we have the following solution:

    *** =solution
    ```{python}
    # import pandas
    import pandas as pd

    # Create dataframe with columns a and b
    my_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5,  6]})
    ```

To test this we simply use:

    *** =sct
    ```{python}
    test_import("pandas")
    test_data_frame("my_df", columns = ["a", "b"])
    success_msg("Great job!")
    ```

This SCT will first test if `pandas` is correctly imported, and will then check if the student created a Pandas DataFrame called `my_df`. If it was not defined, a message is generated that you can override with `undefined_msg`. If the object was defined but it isn't a Pandas DataFrame, as message is generated that you can override wiht `not_data_frame_msg`. If `my_df` is a Pandas DataFrame, `test_data_frame()` goes on to check if all columns that are specified in the `columns` argument are defined in the data frame, and next whether these columns are correct. The messages that are generated in case of an incorrect submission can be overrided with `undefined_cols_msg` and `incorrect_msg`, respectively.

**NOTE**: Behind the scenes, `pythonwhat` has to fetch the value of objects from sub-processes. The required 'dilling' and 'undilling' can cause issues for exotic objects. For more information on this and possible errors that can occur, read the [Processes article](../expression_tests.rst).
