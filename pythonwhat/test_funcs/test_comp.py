import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.Test import Test, BiggerTest, EqualTest, InstanceTest
from pythonwhat import utils
from pythonwhat.utils import get_ord, get_num
from .test_function_definition import test_args, test_body
from pythonwhat.tasks import getTreeResultInProcess, getTreeErrorInProcess, ReprFail
from pythonwhat.sub_test import sub_test

from functools import partial

MSG_NOT_CALLED = "The system wants to check the {ordinal} {typestr} you defined but hasn't found it."
MSG_INCORRECT_ITER_VARS = "Have you used the correct iterator variables in the {ordinal} {typestr}? Make sure you use the correct names!"
MSG_INCORRECT_NUM_ITER_VARS = "Have you used {num_vars} iterator variables in the {ordinal} {typestr}?"
MSG_INSUFFICIENT_IFS = "Have you used {num_ifs} ifs inside the {ordinal} {typestr}?"
MSG_PREPEND = "Check your code in the {{incorrect_part}} of the {ordinal} {typestr}. "

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

    student_comp_list = state.student_list_comps
    solution_comp_list = state.solution_list_comps
    test_comp("list comprehension", **(locals()))

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

    student_comp_list = state.student_generator_exps
    solution_comp_list = state.solution_generator_exps
    test_comp("generator expression", **(locals()))


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

    student_comp_list = state.student_dict_comps
    solution_comp_list = state.solution_dict_comps

    test_comp("dictionary comprehension", **(locals()))


def test_comp(typestr, index,
              solution_comp_list, student_comp_list,
              not_called_msg, insufficient_ifs_msg, incorrect_iter_vars_msg,
              expand_message = True,
              rep=None, state=None, **kwargs):

    # raise error if not enough solution comps
    try:
        solution_comp = solution_comp_list[index - 1]
    except KeyError:
        raise NameError("There aren't %s %ss in the solution environment" % (get_num(index), typestr))

    # partial args to pass to string templating
    fmt_template = partial(str.format, 
                            ordinal = get_ord(index), 
                            typestr=typestr,
                            num_ifs=len(solution_comp['ifs']),
                            num_vars=len(solution_comp['target_vars']))

    # check if enough student comps
    _msg = fmt_template(not_called_msg or MSG_NOT_CALLED)
    rep.do_test(BiggerTest(len(student_comp_list), index - 1, Feedback(_msg)))

    student_comp = student_comp_list[index - 1]

    prepend_fmt = MSG_PREPEND if expand_message is True else (expand_message or "")

    psub_test = partial(sub_test, state, rep,
                       student_context = student_comp['target_vars'],
                       solution_context = solution_comp['target_vars'],
                       expand_message=expand_message and fmt_template(prepend_fmt))

    # test iterable
    psub_test(kwargs['comp_iter'], student_comp['iter'], solution_comp['iter'], "iterable part")

    # test iterator variable names, if required
    if kwargs['iter_vars_names']:
        # message
        _msg = fmt_template(incorrect_iter_vars_msg or MSG_INCORRECT_ITER_VARS)
        # test
        rep.do_test(EqualTest(student_comp['target_vars'], solution_comp['target_vars'],
            Feedback(_msg, student_comp['target'])))
    else:
        # message
        _msg = fmt_template(incorrect_iter_vars_msg or MSG_INCORRECT_NUM_ITER_VARS)
        # test
        rep.do_test(EqualTest(len(student_comp['target_vars']), len(solution_comp['target_vars']),
            Feedback(_msg, student_comp['target'])))

    if typestr != "dictionary comprehension":
        psub_test(kwargs['body'], student_comp['body'], solution_comp['body'], "body")
    else :
        psub_test(kwargs['key'], student_comp['key'], solution_comp['key'], "key part")
        psub_test(kwargs['value'], student_comp['value'], solution_comp['value'], "value part")

    # test ifs, one by one
    if kwargs['ifs'] is not None:
        ifs = kwargs['ifs']
        # message
        _msg = fmt_template(insufficient_ifs_msg or MSG_INSUFFICIENT_IFS)
        # test
        rep.do_test(EqualTest(len(student_comp['ifs']), len(solution_comp['ifs']),
            Feedback(_msg, student_comp['node'])))

        if len(ifs) != len(solution_comp['ifs']):
            raise ValueError("If you specify tests for the ifs, pass a list with the same length as the number of ifs in the solution")

        for i, if_test in enumerate(ifs):
            psub_test(if_test, student_comp['ifs'][i], solution_comp['ifs'][i], ("%s if") % get_ord(i + 1))

def check_list_comp(index, not_called_msg, 
                    iter_vars_names=None, incorrect_iter_vars_msg=MSG_INCORRECT_ITER_VARS,
                    expand_message=MSG_PREPEND, 
                    state=None):

    rep = Reporter.active_reporter

    student_comp_list = state.student_list_comps
    solution_comp_list = state.solution_list_comps

    try:
        solution_comp = solution_comp_list[index - 1]
    except KeyError:
        raise NameError("There aren't %s %ss in the solution environment" % (get_num(index), typestr))

    # partial args to pass to string templating
    fmt_kwargs = {
            'ordinal': get_ord(index), 
            'typestr': typestr, 
            'num_ifs':  len(solution_comp['ifs']), 
            'num_vars': len(solution_comp['target_vars'])
            }

    _msg = (not_called_msg or MSG_NOT_CALLED).format(*fmt_kwargs)
    rep.do_test(BiggerTest(len(student_comp_list), index - 1, Feedback(_msg)))

    student_comp = student_comp_list[index - 1]

    # test iterator variable names, if required TODO: can pull into separate function ----
    if iter_vars_names:
        # message
        _msg = fmt_template(incorrect_iter_vars_msg or MSG_INCORRECT_ITER_VARS)
        # test
        rep.do_test(EqualTest(student_comp['target_vars'], solution_comp['target_vars'],
            Feedback(_msg, student_comp['target'])))
    else:
        # message
        _msg = fmt_template(incorrect_iter_vars_msg or MSG_INCORRECT_NUM_ITER_VARS)
        # test
        rep.do_test(EqualTest(len(student_comp['target_vars']), len(solution_comp['target_vars']),
            Feedback(_msg, student_comp['target'])))

    # TODO: no way to prepend a message currently, should put on state
    return state.to_child_state(student_comp['node'], solution_comp['node'],
                                student_comp['target_vars'], solution_comp['target_vars'],
                                student_part = student_comp, solution_part = solution_comp,
                                append_message={'msg': expand_messages, 'kwargs': fmt_kwargs})

def check_part(name, state=None):
    return state.to_child_state(state.student_part[name], state.solution_part[name])

def check_body(state=None):
    return check_part('body', state=state)

def check_iter(state=None):
    return check_part('iter', state=state)

def check_key(state=None):
    return check_part('key', state=state)

def check_value(state=None):
    return check_part('value', state=state)

# from fn import F
# func = ex() >> check_list_comp() >> check_body() >> test_function('mean')
# func(state)
