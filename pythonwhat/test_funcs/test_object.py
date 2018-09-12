from pythonwhat.tasks import getColumnsInProcess
from pythonwhat.check_object import check_object, check_df, check_keys
from pythonwhat.has_funcs import has_equal_value
from pythonwhat.Feedback import InstructorError

def test_object(name,
                eq_condition="equal",
                eq_fun=None,
                do_eval=True,
                undefined_msg=None,
                incorrect_msg=None,
                state=None):

    expand_msg = "" if undefined_msg or incorrect_msg else None
    child = check_object(name, undefined_msg, expand_msg=expand_msg, state=state)

    if do_eval:
        has_equal_value(incorrect_msg, state=child)

def test_data_frame(name,
                    columns=None,
                    undefined_msg=None,
                    not_data_frame_msg=None,
                    undefined_cols_msg=None,
                    incorrect_msg=None,
                    state=None):
    """Test a pandas dataframe.
    """

    expand_msg = "" if undefined_msg or not_data_frame_msg or undefined_cols_msg or incorrect_msg else None

    child = check_df(name, undefined_msg, not_instance_msg=not_data_frame_msg, expand_msg=expand_msg, state=state)

    # if columns not set, figure them out from solution
    if columns is None:
        columns = getColumnsInProcess(name, child.solution_process)

    for col in columns:
        colstate = check_keys(col, missing_msg=undefined_cols_msg, state=child)
        has_equal_value(incorrect_msg=incorrect_msg, state=colstate)
