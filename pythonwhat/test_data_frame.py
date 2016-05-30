from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedTest, EqualTest, Test

import pandas as pd

def test_data_frame(name,
                    columns=None,
                    undefined_msg=None,
                    not_data_frame_msg=None,
                    undefined_cols_msg=None,
                    incorrect_msg=None):
    """Test a pandas dataframe.


    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_data_frame")

    index = index - 1

    solution_env = state.solution_env
    student_env = state.student_env

    try:
      solution_df = solution_env[name]
      assert isinstance(solution_df, pd.DataFrame)
    except KeyError:
      raise NameError("%r not in solution environment" % name)
    except AssertionError:
      raise ValueError("%r is not a pandas.DataFrame in the solution environment" % name)

    rep.do_test(DefinedTest(name, student_env,
      undefined_msg or "Are you sure you defined the pandas DataFrame: %s?" % name))
    if rep.failed_test:
        return
    student_df = student_env[name]
    rep.do_test(EqualTest(student_df.__class__, pd.DataFrame,
      not_data_frame_msg or "The object you defined as `%s` is not pandas DataFrame." % name))
    if rep.failed_test:
      return

    columns = columns or list(solution_dff.columns)

    for column in columns:
        try:
            solution_column = solution_df[column]
        except KeyError:
            raise NameError("%r is not a column in the %r DataFrame in the solution environment" % (column, name))

        rep.do_test(DefinedTest(column, student_df,
            undefined_cols_msg or "You did not define column `%s` in the pandas DataFrame, `%s`" % (column, name)))
        if rep.failed_test:
            return

        rep.do_test(EqualTest(solution_column, student_column,
            incorrect_msg or "Column `%s` of your pandas DataFrame, `%s`, is not correct."))
        if rep.failed_test:
            return

