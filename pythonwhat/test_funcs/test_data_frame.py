from pythonwhat.Reporter import Reporter
from pythonwhat.tasks import getColumnsInProcess
from .test_object import check_object
from .test_dictionary import is_instance, test_key, has_key

import pandas as pd

MSG_UNDEFINED = "Are you sure you defined the pandas DataFrame: `{parent[sol_part][name]}`?"
MSG_NOT_INSTANCE = "`{parent[sol_part][name]}` is not a pandas DataFrame."
MSG_KEY_MISSING = "There is no column `{key}` inside `{parent[sol_part][name]}`."
MSG_INCORRECT_VAL = "Column `{key}` of your pandas DataFrame, `{parent[sol_part][name]}`, is not correct."

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
    rep.set_tag("fun", "test_data_frame")

    child = check_df(name, undefined_msg or MSG_UNDEFINED, not_data_frame_msg or MSG_NOT_INSTANCE, state=state)

    sol_cols = getColumnsInProcess(name, child.solution_process)
    if sol_cols is None:
        raise ValueError("Something went wrong in figuring out the columns for %s in the solution process" % name)

    # set columns or check if manual columns are valid
    if columns is None: columns = sol_cols

    for col in columns:
        # check if column available
        test_key(name, col, incorrect_msg or MSG_INCORRECT_VAL, undefined_cols_msg or MSG_KEY_MISSING, state=child)

# Check functions -------------------------------------------------------------

def check_df(name, undefined_msg=MSG_UNDEFINED, not_instance_msg=MSG_NOT_INSTANCE, state=None):

    child = check_object(name, undefined_msg, state=state)          # test defined
    is_instance(name, pd.DataFrame, not_instance_msg, state=child)  # test instance

    return child
