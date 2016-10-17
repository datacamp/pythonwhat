from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedProcessTest, InstanceProcessTest, DefinedCollProcessTest, EqualValueProcessTest
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isDefinedInProcess, isInstanceInProcess, getColumnsInProcess, getValueInProcess, ReprFail
from .test_object import check_object
from .test_dictionary import is_instance, test_key, has_key

import pandas as pd

MSG_UNDEFINED = "Are you sure you defined the pandas DataFrame: `{name}`?"
MSG_NOT_INSTANCE = "`{name}` is not a pandas DataFrame."
MSG_KEY_MISSING = "There is no column `{key}` inside `{name}`."
MSG_INCORRECT_VAL = "Column `{key}` of your pandas DataFrame, `{name}`, is not correct."

def test_data_frame(name,
                    columns=None,
                    undefined_msg=MSG_UNDEFINED,
                    not_data_frame_msg=MSG_NOT_INSTANCE,
                    undefined_cols_msg=MSG_KEY_MISSING,
                    incorrect_msg=MSG_INCORRECT_VAL,
                    state=None):
    """Test a pandas dataframe.
    """

    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_data_frame")

    sol_cols = check_df(name, undefined_msg, not_data_frame_msg, state=state)

    # set columns or check if manual columns are valid
    if columns is None: columns = sol_cols

    for col in columns:
        # check if column available
        test_key(name, col, incorrect_msg, undefined_cols_msg, sol_cols, state=state)

# Check functions -------------------------------------------------------------

def check_df(name, undefined_msg, not_instance_msg, state=None):
    rep = Reporter.active_reporter

    # Check if defined
    undefined_msg = undefined_msg.format(name=name)

    # check but don't get solution object representation
    state = check_object(name, undefined_msg, state=state)

    is_instance(name, pd.DataFrame, not_instance_msg, state=state)

    sol_keys = getColumnsInProcess(name, state.solution_process)

    if sol_keys is None:
        raise ValueError("Something went wrong in figuring out the columns for %s in the solution process" % name)

    return sol_keys

