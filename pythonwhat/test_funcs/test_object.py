from pythonwhat.Reporter import Reporter
from pythonwhat.has_funcs import has_equal_value
from pythonwhat.check_object import check_object
from pythonwhat.Reporter import Reporter
from pythonwhat.tasks import getColumnsInProcess
from pythonwhat.check_object import check_object, is_instance, has_equal_key, has_key
import pandas as pd

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

    # check if variable exists
    child = check_object(name, undefined_msg, expand_msg=expand_msg, state=state, typestr="pandas DataFrame")

    # check if instance correct
    is_instance(pd.DataFrame, not_data_frame_msg, state=child)

    # if columns not set, figure them out from solution
    if columns is None:
        columns = getColumnsInProcess(name, child.solution_process)
        if columns is None:
            raise ValueError("Something went wrong in figuring out the columns for %s in the solution process" % name)

    for col in columns:
        # check if column available
        has_equal_key(col, incorrect_msg, undefined_cols_msg, state=child)
