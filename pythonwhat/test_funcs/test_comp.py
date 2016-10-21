from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.Test import Test, BiggerTest, EqualTest, InstanceTest
from pythonwhat.tasks import getTreeResultInProcess, getTreeErrorInProcess, ReprFail
from pythonwhat.utils import get_ord, get_num
from pythonwhat.check_funcs import check_part, multi


MSG_NOT_CALLED = "The system wants to check the {ordinal} {typestr} you defined but hasn't found it."
MSG_INCORRECT_ITER_VARS = "Have you used the correct iterator variables in the {ordinal} {typestr}? Make sure you use the correct names!"
MSG_INCORRECT_NUM_ITER_VARS = "Have you used {num_vars} iterator variables in the {ordinal} {typestr}?"
MSG_INSUFFICIENT_IFS = "Have you used {num_ifs} ifs inside the {ordinal} {typestr}?"
MSG_PREPEND = "Check your code in the {part} of the {ordinal} {typestr}. "

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
    rep.set_tag("fun", "test_list_comp")

    test_comp("list comprehension", 'list_comps', **(locals()))

def test_generator_exp(index=1,
                       not_called_msg=None,
                       comp_iter=None,
                       iter_vars_names=False,
                       incorrect_iter_vars_msg=None,
                       body=None,
                       ifs=None,
                       insufficient_ifs_msg=None,
                       expand_message=True,
                       state=None):
    """Test generator expressions
    """
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_generator_exp")

    test_comp("generator expression", 'generator_exps', **(locals()))


def test_dict_comp(index=1,
                   not_called_msg=None,
                   comp_iter=None,
                   iter_vars_names=False,
                   incorrect_iter_vars_msg=None,
                   key=None,
                   value=None,
                   ifs=None,
                   insufficient_ifs_msg=None,
                   expand_message=True,
                   state=None):
    """Test dict comprehension.
    """
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_dict_comp")

    test_comp("dictionary comprehension", 'dict_comps', **(locals()))


def test_comp(typestr, comptype, index, iter_vars_names,
              not_called_msg, insufficient_ifs_msg, incorrect_iter_vars_msg,
              comp_iter, ifs, key=None, body=None, value=None,
              expand_message = True,
              rep=None, state=None):

    # if true, set expand_message to default (for backwards compatibility)
    expand_message = MSG_PREPEND if expand_message is True else (expand_message or "")

    # get comprehension
    state = check_comp(typestr, comptype, index, not_called_msg, 
                       expand_message, state)

    # test comprehension iter and its variable names (or number of variables)
    if comp_iter: multi(comp_iter, state=check_iter("iterable part", state))
    has_iter_vars(incorrect_iter_vars_msg, iter_vars_names, state=state)

    # test the main expressions.
    if body:   multi(body,  state=check_body("body", state))        # list and gen comp
    if key:    multi(key,   state=check_key("key part", state))     # dict comp
    if value:  multi(value, state=check_value("value part", state)) # ""

    # test a list of ifs. each entry corresponds to a filter in the comprehension.
    for i, if_test in enumerate(ifs or []):
        multi(if_test, state=check_ifs(i, insufficient_ifs_msg, state=state))

def check_comp(typestr, comptype, index, not_called_msg, 
               expand_message=MSG_PREPEND, 
               state=None):

    rep = Reporter.active_reporter

    # select comprehension of appropriate type
    solution_comp_list = getattr(state, 'solution_'+comptype)
    student_comp_list = getattr(state, 'student_'+comptype)

    try:
        solution_comp = solution_comp_list[index - 1]
    except KeyError:
        raise NameError("There aren't %s %ss in the solution environment" % (get_num(index), typestr))

    # dictionary of variables to pass to string templating
    fmt_kwargs = {
            'ordinal': get_ord(index), 
            'typestr': typestr, 
            'num_ifs':  len(solution_comp['ifs']), 
            'num_vars': len(solution_comp['target_vars'])
            }

    # check that the comprehension exists
    _msg = (not_called_msg or MSG_NOT_CALLED).format(**fmt_kwargs)
    rep.do_test(BiggerTest(len(student_comp_list), index - 1, Feedback(_msg)))

    # select comprehension
    student_comp = student_comp_list[index - 1]

    # return child state for comprehension
    return state.to_child_state(student_comp['node'], solution_comp['node'],
                                student_comp['target_vars'], solution_comp['target_vars'],
                                student_parts = student_comp, solution_parts = solution_comp,
                                append_message={'msg': expand_message, 'kwargs': fmt_kwargs})

def check_body(part_msg, state=None):
    return check_part('body', part_msg, state=state)

def check_iter(part_msg, state=None):
    return check_part('iter', part_msg, state=state)

def check_key(part_msg, state=None):
    return check_part('key', part_msg, state=state)

def check_value(part_msg, state=None):
    return check_part('value', part_msg, state=state)

def check_ifs(index, insufficient_ifs_msg=None, part_msg=None, state=None):
    """Return a child state with if filter at position index as its ast tree."""
    # this function differs from other check_part functions, in that it needs
    # to get a specific index. Note that it runs a test to see if it can be
    # TODO: can likely be made general (check_part_index)
    rep = Reporter.active_reporter
    sol_ifs = state.solution_parts['ifs']
    stu_ifs = state.student_parts['ifs']

    # TODO this is here because we need to get {ordinal} and {typestr} from the comp state
    fmt_kwargs = state.messages[-1]['kwargs']

    _msg = (insufficient_ifs_msg or MSG_INSUFFICIENT_IFS) \
            .format(**fmt_kwargs)
    # test
    rep.do_test(EqualTest(len(stu_ifs), len(sol_ifs),
        Feedback(_msg, state.student_tree)))

    if len(stu_ifs) != len(sol_ifs):
        raise ValueError("If you specify tests for the ifs, pass a list with the same length as the number of ifs in the solution")

    if part_msg is None: part_msg = get_ord(index+1) + ' if'
    child = state.to_child_state(stu_ifs[index], sol_ifs[index])
    # TODO this adds the part name {part} to the message in check_comp state
    import copy
    msg = copy.copy(child.messages[-2])
    msg.update(kwargs = {**msg['kwargs'], 'part': part_msg})
    child.messages[-2] = msg
    return child
    
def has_iter_vars(incorrect_iter_vars_msg, exact_names=False, state=None):
    rep = Reporter.active_reporter
    # get parts for testing from state
    stu_tv, sol_tv = state.student_parts['target_vars'], state.solution_parts['target_vars']
    stu_target = state.student_parts['target']

    fmt_kwargs = typestr = state.messages[-1]['kwargs']

    if exact_names:
        # message for wrong iter var names
        _msg = (incorrect_iter_vars_msg or MSG_INCORRECT_ITER_VARS).format(**fmt_kwargs)
        # test
        rep.do_test(EqualTest(stu_tv, sol_tv, Feedback(_msg, stu_target)))
    else:
        # message for wrong number of iter vars
        _msg = (incorrect_iter_vars_msg or MSG_INCORRECT_NUM_ITER_VARS).format(**fmt_kwargs)
        # test
        rep.do_test(EqualTest(len(stu_tv), len(sol_tv), Feedback(_msg, stu_target)))

    return state

