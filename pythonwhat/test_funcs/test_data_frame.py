from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedProcessTest, InstanceProcessTest, DefinedCollProcessTest, EqualValueProcessTest
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isDefinedInProcess, isInstanceInProcess, getColumnsInProcess, getValueInProcess, ReprFail
from .test_object import check_object

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
    rep.set_tag("fun", "test_data_frame")

    sol_cols = check_df(name, undefined_msg, not_data_frame_msg, state=state)

    # set columns or check if manual columns are valid
    if columns is None: columns = sol_cols

    for col in columns:
        # check if column available
        test_key(name, col, incorrect_msg, undefined_cols_msg, sol_cols, state=state)

# Check functions -------------------------------------------------------------

MSG_UNDEFINED = "Are you sure you defined the pandas DataFrame: `{name}`?"
MSG_NOT_INSTANCE = "`{name}` is not a pandas DataFrame."
MSG_KEY_MISSING = "There is no column `{key}` inside `{name}`."
MSG_INCORRECT_VAL = "Column `{key}` of your pandas DataFrame, `{name}`, is not correct."

def check_df(name, undefined_msg, not_instance_msg, state=None):
    rep = Reporter.active_reporter

    # Check if defined
    if not undefined_msg:
        undefined_msg = MSG_UNDEFINED.format(name=name)

    # check but don't get solution object representation
    state = check_object(name, undefined_msg, state=state)

    is_instance(name, not_instance_msg, state=state)

    sol_keys = getColumnsInProcess(name, state.solution_process)

    if sol_keys is None:
        raise ValueError("Something went wrong in figuring out the columns for %s in the solution process" % name)

    return sol_keys

def is_instance(name, not_instance_msg, state=None):
    rep = Reporter.active_reporter

    if  not isInstanceInProcess(name, state.solution_object, state.solution_process):
        raise ValueError("%r is not a pandas.DataFrame in the solution environment" % name)

    if not not_instance_msg: not_instance_msg = MSG_NOT_INSTANCE.format(name=name)

    rep.do_test(InstanceProcessTest(name, pd.DataFrame, state.student_process, Feedback(not_instance_msg)))

def has_key(name, key, key_missing_msg, sol_keys=None, state=None):
    rep = Reporter.active_reporter

    if sol_keys is None:
        sol_keys = getColumnsInProcess(name, state.solution_process)

    if key not in sol_keys:
        raise NameError("Not all columns you specified are actually columns in %s in the solution process" % name)

    # check if key available
    if not key_missing_msg:
        msg = MSG_KEY_MISSING.format(key=key, name=name)
    else:
        msg = key_missing_msg
    rep.do_test(DefinedCollProcessTest(name, key, state.student_process, Feedback(msg)))

def test_key(name, key, incorrect_value_msg, key_missing_msg, sol_keys=None, state=None):
    rep = Reporter.active_reporter

    has_key(name, key, key_missing_msg, sol_keys, state=state)

    sol_value = getValueInProcess(name, key, state.solution_process)
    if isinstance(sol_value, ReprFail):
        raise NameError("Value from %r can't be fetched from the solution process: %s" % c(name, sol_value.info))

    # check if value ok
    msg = incorrect_value_msg or MSG_INCORRECT_VAL.format(key=key, name=name)

    rep.do_test(EqualValueProcessTest(name, key, state.student_process, sol_value, Feedback(msg)))
