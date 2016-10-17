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
        test_col(name, col, incorrect_msg, undefined_cols_msg, sol_cols, state=state)

def check_df(name, undefined_msg, not_data_frame_msg, state=None):
    rep = Reporter.active_reporter

    # Check if defined
    if not undefined_msg:
        undefined_msg = "Are you sure you defined the pandas DataFrame: `%s`?" % name

    # check but don't get solution df representation
    state = check_object(name, undefined_msg, state=state)

    is_df(name, not_data_frame_msg, state=state)

    sol_columns = getColumnsInProcess(name, state.solution_process)

    if sol_columns is None:
        raise ValueError("Something went wrong in figuring out the columns for %s in the solution process" % name)

    return sol_columns

def is_df(name, not_data_frame_msg, state=None):
    rep = Reporter.active_reporter

    if  not isInstanceInProcess(name, pd.DataFrame, state.solution_process):
        raise ValueError("%r is not a pandas.DataFrame in the solution environment" % name)

    if not not_data_frame_msg:
        not_data_frame_msg = "`%s` is not a pandas DataFrame." % name
    rep.do_test(InstanceProcessTest(name, pd.DataFrame, state.student_process, Feedback(not_data_frame_msg)))

def has_col(name, col, undefined_cols_msg, sol_columns = None, state=None):
    rep = Reporter.active_reporter

    if sol_columns is None:
        sol_columns = getColumnsInProcess(name, state.solution_process)

    if not col in sol_columns:
        raise NameError("Not all columns you specified are actually columns in %s in the solution process" % name)

    # check if col available
    if not undefined_cols_msg:
        msg = "There is no column `%s` inside `%s`." % (col, name)
    else:
        msg = undefined_cols_msg
    rep.do_test(DefinedCollProcessTest(name, col, state.student_process, Feedback(msg)))

def test_col(name, col, incorrect_msg, undefined_cols_msg, sol_cols, state=None):
    rep = Reporter.active_reporter

    has_col(name, col, undefined_cols_msg, sol_cols, state=state)
    
    sol_value = getValueInProcess(name, col, state.solution_process)
    if isinstance(sol_value, ReprFail):
        raise NameError("Value from %r can't be fetched from the solution process: %s" % c(name, sol_value.info))

    # check if actual column ok
    msg = incorrect_msg or \
          "Column `%s` of your pandas DataFrame, `%s`, is not correct." % (col, name)

    rep.do_test(EqualValueProcessTest(name, col, state.student_process, sol_value, Feedback(msg)))
