from pythonwhat.Reporter import Reporter
from pythonwhat.tasks import getColumnsInProcess
from pythonwhat.check_object import check_object, is_instance, has_equal_key, has_key

MSG_UNDEFINED = "FMT:Are you sure you defined the pandas DataFrame: `{index}`?"
MSG_NOT_INSTANCE = "FMT:`{parent[sol_part][name]}` is not a pandas DataFrame."
MSG_KEY_MISSING = "FMT:There is no column `{key}` inside `{parent[sol_part][name]}`."
MSG_INCORRECT_VAL = "FMT:Column `{key}` of your pandas DataFrame, `{parent[sol_part][name]}`, is not correct."

import pandas as pd

def test_data_frame(name,
                    columns=None,
                    undefined_msg=None,
                    not_data_frame_msg=None,
                    undefined_cols_msg=None,
                    incorrect_msg=None,
                    state=None):
    """Test a pandas dataframe.
    """

    rep = Reporter.active_reporter

    child = check_object(name, undefined_msg or MSG_UNDEFINED, expand_msg="", state=state, typestr="pandas DataFrame")
    is_instance(pd.DataFrame, not_data_frame_msg or MSG_NOT_INSTANCE, state=child)  # test instance

    sol_cols = getColumnsInProcess(name, child.solution_process)
    if sol_cols is None:
        raise ValueError("Something went wrong in figuring out the columns for %s in the solution process" % name)

    # set columns or check if manual columns are valid
    if columns is None: columns = sol_cols

    for col in columns:
        # check if column available
        has_equal_key(col, incorrect_msg or MSG_INCORRECT_VAL, undefined_cols_msg or MSG_KEY_MISSING, state=child)


def check_df(name, undefined_msg=MSG_UNDEFINED, not_instance_msg=MSG_NOT_INSTANCE, state=None):

    # test defined
    child = check_object(name, undefined_msg, state=state, typestr="pandas DataFrame")
    is_instance(pd.DataFrame, not_instance_msg, state=child)  # test instance

    return child

