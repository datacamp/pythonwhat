from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat import utils
from pythonwhat.utils import get_ord, get_num
from pythonwhat.Test import BiggerTest, EqualTest

def test_list_comp(index=1,
                   not_called_msg=None,
                   comp_iter=None,
                   iter_vars_names=False,
                   incorrect_iter_vars_msg=None,
                   body=None,
                   ifs=None,
                   insufficient_ifs_msg=None,
                   expand_message=True):
    """Test list comprehension.
    """

    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_list_comp")

    state.extract_list_comps()
    student_comp_list = state.student_list_comps
    solution_comp_list = state.solution_list_comps
    test_comp(comp_type = "list", **(locals()))

def test_generator_exp(index=1,
                       not_called_msg=None,
                       comp_iter=None,
                       iter_vars_names=False,
                       incorrect_iter_vars_msg=None,
                       body=None,
                       ifs=None,
                       insufficient_ifs_msg=None,
                       expand_message=True):
    """Test generator expressions
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_generator_exp")

    state.extract_generator_exps()
    student_comp_list = state.student_generator_exps
    solution_comp_list = state.solution_generator_exps
    test_comp(comp_type = "gen", **(locals()))


def test_dict_comp(index=1,
                   not_called_msg=None,
                   comp_iter=None,
                   iter_vars_names=False,
                   incorrect_iter_vars_msg=None,
                   key=None,
                   value=None,
                   ifs=None,
                   insufficient_ifs_msg=None,
                   expand_message=True):
    """Test dict comprehension.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_dict_comp")

    state.extract_dict_comps()
    student_comp_list = state.student_dict_comps
    solution_comp_list = state.solution_dict_comps

    test_comp(comp_type = "dict", **(locals()))


def test_comp(comp_type, **kwargs):

    if comp_type not in ['list', 'dict', 'gen']:
        raise ValueError("comp_type not valid")
    typestr = {'list':'list comprehension', 'dict': 'dictionary comprehension', 'gen': 'generator expression'}[comp_type]

    state = kwargs['state']
    rep = kwargs['rep']

    solution_comp_list = kwargs['solution_comp_list']
    student_comp_list = kwargs['student_comp_list']
    index = kwargs['index']

    # raise error if not enough solution comps
    try:
        solution_comp = solution_comp_list[index - 1]
    except KeyError:
        raise NameError("There aren't %s %ss in the solution environment" % (get_num(index), typestr))

    # check if enough student comps
    c_not_called_msg = kwargs['not_called_msg'] or \
        ("The system wants to check the %s %s you defined but hasn't found it." % (get_ord(index), typestr))
    rep.do_test(BiggerTest(len(student_comp_list), index - 1, Feedback(c_not_called_msg)))
    if rep.failed_test:
        return

    student_comp = student_comp_list[index - 1]

    def sub_test(closure, subtree_student, subtree_solution, incorrect_part):
        if closure:
            child = state.to_child_state(subtree_student, subtree_solution)
            child.student_context = student_comp['target_vars']
            child.solution_context = solution_comp['target_vars']
            closure()
            child.to_parent_state()
            if rep.failed_test:
                if kwargs['expand_message']:
                    rep.feedback.message = ("Check your code in the %s of the %s %s. " %
                        (incorrect_part, get_ord(index), typestr)) + rep.feedback.message
                if not rep.feedback.line_info:
                    rep.feedback = Feedback(rep.feedback.message, subtree_student)

    # test iterable
    sub_test(kwargs['comp_iter'], student_comp['iter'], solution_comp['iter'], "iterable part")
    if rep.failed_test:
        return

    # test iterator variable names, if required
    if kwargs['iter_vars_names']:
        c_incorrect_iter_vars_msg = kwargs['incorrect_iter_vars_msg'] or \
            ("Have you used the correct iterator variables in the %s %s? Make sure you use the correct names!" % (get_ord(index), typestr))
        rep.do_test(EqualTest(student_comp['target_vars'], solution_comp['target_vars'],
            Feedback(c_incorrect_iter_vars_msg, student_comp['target'])))
    else:
        c_incorrect_iter_vars_msg = kwargs['incorrect_iter_vars_msg'] or \
            ("Have you used %s iterator variables in the %s %s?" % (len(solution_comp['target_vars']), get_ord(index), typestr))
        rep.do_test(EqualTest(len(student_comp['target_vars']), len(solution_comp['target_vars']),
            Feedback(c_incorrect_iter_vars_msg, student_comp['target'])))
    if rep.failed_test:
        return


    if comp_type in ['list', 'gen'] :
        sub_test(kwargs['body'], student_comp['body'], solution_comp['body'], "body")
        if rep.failed_test:
            return
    else :
        sub_test(kwargs['key'], student_comp['key'], solution_comp['key'], "key part")
        if rep.failed_test:
            return
        sub_test(kwargs['value'], student_comp['value'], solution_comp['value'], "value part")
        if rep.failed_test:
            return

    # test ifs, one by one
    if kwargs['ifs'] is not None:
        c_insufficient_ifs_msg = kwargs['insufficient_ifs_msg'] or \
            ("Have you used %s ifs inside the %s %s?" % (len(solution_comp['ifs']), get_ord(index), typestr))
        rep.do_test(EqualTest(len(student_comp['ifs']), len(solution_comp['ifs']),
            Feedback(c_insufficient_ifs_msg, student_comp['list_comp'])))
        if rep.failed_test:
            return

        if len(kwargs['ifs']) != len(solution_comp['ifs']):
            raise ValueError("If you specify tests for the ifs, pass a list with the same length as the number of ifs in the solution")

        for i, if_test in enumerate(kwargs['ifs']):
            sub_test(if_test, student_comp['ifs'][i], solution_comp['ifs'][i], ("%s if") % get_ord(i + 1))
            if rep.failed_test:
                return
