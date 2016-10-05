import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.Test import BiggerTest, Test, DefinedCollTest
from pythonwhat.utils import get_ord, get_num

from .sub_test import sub_test
from functools import partial

def test_try_except(index=1,
                    not_called_msg=None,
                    body=None,
                    handlers={},
                    except_missing_msg = None,
                    orelse=None,
                    orelse_missing_msg=None,
                    finalbody=None,
                    finalbody_missing_msg=None,
                    expand_message=True,
                    state=None):
    """Test a try except construct
    """

    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_try_except")

    state.extract_try_excepts()

    student_try_excepts = state.student_try_excepts
    solution_try_excepts = state.solution_try_excepts

    # raise error if not enough solution_try_excepts
    try:
        solution_try_except = solution_try_excepts[index - 1]
    except KeyError:
        raise NameError("There aren't %s try-except blocks in the solution code" % get_num(index))

    # check if enough student_lambdas
    c_not_called_msg = not_called_msg or \
        ("The system wants to check the %s try-except block you defined but hasn't found it." % get_ord(index))
    rep.do_test(BiggerTest(len(student_try_excepts), index - 1, Feedback(c_not_called_msg)))

    student_try_except = student_try_excepts[index - 1]

    prepend_fmt = "Check your code in the {incorrect_part} of the %s try-except block. " % (get_ord(index))

    psub_test = partial(sub_test, state, rep, 
            expand_message = expand_message and prepend_fmt)

    psub_test(body, student_try_except['body'], solution_try_except['body'], "body")

    for key,value in handlers.items():
        if key == 'all':
            patt = "general"
        else:
            patt = "`%s`" % key
        incorrect_part = "%s `except` block" % patt
        try:
            solution_except = solution_try_except['handlers'][key]
        except:
            raise ValueError("Make sure that you actually specify a %s in your solution code." % incorrect_part)

        c_except_missing_msg = except_missing_msg or \
            ("Have you included a %s in your %s try-except block?" % (incorrect_part, get_ord(index)))

        rep.do_test(DefinedCollTest(key, student_try_except['handlers'],
            Feedback(c_except_missing_msg, student_try_except['try_except'])))

        student_except = student_try_except['handlers'][key]

        psub_test(value, student_except.body, solution_except.body, incorrect_part, student_except.name, solution_except.name)

    def test_part(el, incorrect_part, missing_msg, test):
        if len(solution_try_except[el]) == 0:
            raise ValueError("Make sure that you actually specify a %s in your solution code" % incorrect_part)

        c_missing_msg = missing_msg or \
            ("Have you included a %s in your %s try-except block?" % (incorrect_part, get_ord(index)))
        if len(student_try_except[el]) == 0:
            rep.do_test(Test(Feedback(c_missing_msg, student_try_except['try_except'])))
            return

        psub_test(test, student_try_except[el], solution_try_except[el], incorrect_part)

    if orelse is not None:
        test_part("orelse", "`else` part", orelse_missing_msg, orelse)

    if finalbody is not None:
        test_part("finalbody", "`finally` part", finalbody_missing_msg, finalbody)
