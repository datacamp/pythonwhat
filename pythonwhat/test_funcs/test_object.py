from protowhat.sct_syntax import link_to_state
from pythonwhat.tasks import getColumnsInProcess
from pythonwhat.checks.check_object import check_object, check_df, check_keys
from pythonwhat.checks.has_funcs import has_equal_value

# this is done by the chain for v2
# it's only needed when a new state is created and (possibly) used elsewhere
check_object = link_to_state(check_object)
check_df = link_to_state(check_df)
check_keys = link_to_state(check_keys)


def test_object(
    state,
    name,
    eq_condition="equal",
    eq_fun=None,
    do_eval=True,
    undefined_msg=None,
    incorrect_msg=None,
):

    expand_msg = "" if undefined_msg or incorrect_msg else None
    child = check_object(state, name, undefined_msg, expand_msg=expand_msg)

    if do_eval:
        has_equal_value(child, incorrect_msg)


def test_data_frame(
    state,
    name,
    columns=None,
    undefined_msg=None,
    not_data_frame_msg=None,
    undefined_cols_msg=None,
    incorrect_msg=None,
):
    """Test a pandas dataframe.
    """

    expand_msg = (
        ""
        if undefined_msg or not_data_frame_msg or undefined_cols_msg or incorrect_msg
        else None
    )

    child = check_df(
        state,
        name,
        undefined_msg,
        not_instance_msg=not_data_frame_msg,
        expand_msg=expand_msg,
    )

    # if columns not set, figure them out from solution
    if columns is None:
        columns = getColumnsInProcess(name, child.solution_process)

    for col in columns:
        colstate = check_keys(child, col, missing_msg=undefined_cols_msg)
        has_equal_value(colstate, incorrect_msg=incorrect_msg)
