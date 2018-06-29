from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.Test import EqualTest
from pythonwhat.utils import get_ord
from pythonwhat.check_funcs import check_node, check_part, check_part_index, multi, has_equal_part_len
from pythonwhat.check_has_context import has_context


MSG_NOT_CALLED = "FMT:The system wants to check the {typestr} but hasn't found it."
MSG_PREPEND = "FMT:Check the {typestr}. "

MSG_INCORRECT_ITER_VARS = "FMT:Have you used the correct iterator variables in the {parent[typestr]}? Be sure to use the correct names."
MSG_INCORRECT_NUM_ITER_VARS = "FMT:Have you used {num_vars} iterator variables in the {parent[typestr]}?"
MSG_INSUFFICIENT_IFS = "FMT:Have you used {sol_len} ifs inside the {parent[typestr]}?"

def test_list_comp(index=1,
                   not_called_msg=None,
                   comp_iter=None,
                   iter_vars_names=False,
                   incorrect_iter_vars_msg=None,
                   body=None,
                   ifs=None,
                   insufficient_ifs_msg=None,
                   expand_message=True,
                   state=None):
    """Test list comprehension.
    """

    rep = Reporter.active_reporter

    test_comp("{ordinal} list comprehension", 'list_comps', **(locals()))


def test_comp(typestr, comptype, index, iter_vars_names,
              not_called_msg, insufficient_ifs_msg, incorrect_iter_vars_msg,
              comp_iter, ifs, key=None, body=None, value=None,
              expand_message = True,
              rep=None, state=None):

    # if true, set expand_message to default (for backwards compatibility)
    expand_message = MSG_PREPEND if expand_message is True else (expand_message or "")
    # make sure other messages are set to default if None
    if insufficient_ifs_msg is None: insufficient_ifs_msg = MSG_INSUFFICIENT_IFS
    if not_called_msg is None: not_called_msg = MSG_NOT_CALLED

    # TODO MSG: function was not consistent with prepending, so use state w/o expand_message
    quiet_state = check_node(comptype, index-1, typestr, not_called_msg, expand_msg="", state=state)

    # get comprehension
    state = check_node(comptype, index-1, typestr, not_called_msg, expand_msg=None if expand_message else "", state=state)

    # test comprehension iter and its variable names (or number of variables)
    if comp_iter: multi(comp_iter, state=check_part("iter", "iterable part", state=state))

    # test iterator variables
    default_msg = MSG_INCORRECT_ITER_VARS if iter_vars_names else MSG_INCORRECT_NUM_ITER_VARS
    has_context(incorrect_iter_vars_msg or default_msg, iter_vars_names, state=quiet_state)

    # test the main expressions.
    if body:   multi(body,  state=check_part("body", "body", expand_msg=None if expand_message else "", state=state))        # list and gen comp
    if key:    multi(key,   state=check_part("key", "key part", expand_msg=None if expand_message else "",  state=state))    # dict comp
    if value:  multi(value, state=check_part("value", "value part", expand_msg=None if expand_message else "", state=state)) # ""

    # test a list of ifs. each entry corresponds to a filter in the comprehension.
    for i, if_test in enumerate(ifs or []):
        # test that ifs are same length
        has_equal_part_len('ifs', insufficient_ifs_msg, state=quiet_state)
        # test individual ifs
        multi(if_test, state=check_part_index("ifs", i, get_ord(i+1) + " if", state=state))

