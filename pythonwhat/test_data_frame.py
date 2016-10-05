from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedProcessTest, InstanceProcessTest, DefinedCollProcessTest, EqualValueProcessTest
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isDefinedInProcess, isInstanceInProcess, getColumnsInProcess, getValueInProcess, ReprFail

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

    solution_process = state.solution_process
    student_process = state.student_process

    if not isDefinedInProcess(name, solution_process):
        raise NameError("%r not in solution environment" % name)

    if  not isInstanceInProcess(name, pd.DataFrame, solution_process):
        raise ValueError("%r is not a pandas.DataFrame in the solution environment" % name)


    # Check if defined
    if not undefined_msg:
        undefined_msg = "Are you sure you defined the pandas DataFrame: `%s`?" % name
    rep.do_test(DefinedProcessTest(name, student_process, Feedback(undefined_msg)))

    if not not_data_frame_msg:
        not_data_frame_msg = "`%s` is not a pandas DataFrame." % name
    rep.do_test(InstanceProcessTest(name, pd.DataFrame, student_process, Feedback(not_data_frame_msg)))

    sol_columns = getColumnsInProcess(name, solution_process)
    if sol_columns is None:
        raise ValueError("Something went wrong in figuring out the columns for %s in the solution process" % name)

    # set columns or check if manual columns are valid
    if columns is None:
        columns = sol_columns
    elif set(columns) > set(sol_columns):
        raise NameError("Not all columns you specified are actually columns in %s in the solution process" % name)

    for column in columns:

        # check if column available
        if not undefined_cols_msg:
            msg = "There is no column `%s` inside `%s`." % (column, name)
        else:
            msg = undefined_cols_msg
        rep.do_test(DefinedCollProcessTest(name, column, student_process, Feedback(msg)))

        sol_value = getValueInProcess(name, column, solution_process)
        if isinstance(sol_value, ReprFail):
            raise NameError("Value from %r can't be fetched from the solution process: %s" % c(name, sol_value.info))

        # check if actual column ok
        if not incorrect_msg:
            msg = "Column `%s` of your pandas DataFrame, `%s`, is not correct." % (column, name)
        else:
            msg = incorrect_msg
        rep.do_test(EqualValueProcessTest(name, column, student_process, sol_value, Feedback(msg)))
