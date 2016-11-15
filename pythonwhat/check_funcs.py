from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test
from pythonwhat.Feedback import Feedback
from pythonwhat.utils import get_ord
from functools import partial
import copy

def part_to_child(stu_part, sol_part, append_message, state):
    # stu_part and sol_part will be accessible on all templates
    append_message['kwargs'].update({'stu_part': stu_part, 'sol_part': sol_part})

    # if the parts are dictionaries, use to deck out child state
    if all(isinstance(p, dict) for p in [stu_part, sol_part]):
        return state.to_child_state(stu_part['node'], sol_part['node'],
                                    stu_part.get('target_vars'), sol_part.get('target_vars'),
                                    stu_part, sol_part,
                                    highlight = stu_part.get('highlight'),
                                    append_message = append_message)

    # otherwise, assume they are just nodes
    return state.to_child_state(stu_part, sol_part, append_message = append_message)


def check_part(name, part_msg, state=None, missing_msg="", expand_msg=""):
    """Return child state with name part as its ast tree"""
    rep = Reporter.active_reporter

    if not part_msg: part_msg = name
    append_message = {'msg': expand_msg, 'kwargs': {'part': part_msg,}}

    has_part(name, missing_msg, state, append_message['kwargs'])

    stu_part = state.student_parts[name]
    sol_part = state.solution_parts[name]

    return part_to_child(stu_part, sol_part, append_message, state)

def check_part_index(name, index, part_msg,
                     missing_msg="Define more {part}.",
                     state=None, expand_msg=""):
    """Return child state with indexed name part as its ast tree"""

    rep = Reporter.active_reporter

    # create message
    ordinal = "" if isinstance(index, str) else get_ord(index+1)

    append_message = {'msg': expand_msg,
                      'kwargs': {'part': part_msg, 'index': index, 'ordinal': ordinal}}

    # check there are enough parts for index
    stu_parts = state.student_parts[name]
    try: stu_parts[index]
    except (KeyError, IndexError):
        _msg = state.build_message(missing_msg, append_message['kwargs'])
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    # get part at index
    stu_part = state.student_parts[name][index]
    sol_part = state.solution_parts[name][index]

    # return child state from part
    return part_to_child(stu_part, sol_part, append_message, state)

MSG_MISSING = "The system wants to check the {ordinal} {typestr} you defined but hasn't found it."
MSG_PREPEND = "Check your code in the {child[part]} of the {ordinal} {typestr}. "
def check_node(name, index, typestr, missing_msg=MSG_MISSING, expand_msg=MSG_PREPEND, state=None):
    rep = Reporter.active_reporter
    stu_out = getattr(state, 'student_'+name)
    sol_out = getattr(state, 'solution_'+name)

    # check if there are enough nodes for index
    fmt_kwargs = {'ordinal': get_ord(index+1) if isinstance(index, int) else "",
                  'typestr': typestr}

    # test if node can be indexed succesfully
    try: stu_out[index]
    except (KeyError, IndexError):                  # TODO comment errors
        _msg = state.build_message(missing_msg, fmt_kwargs)
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    # get node at index
    stu_part = stu_out[index]
    sol_part = sol_out[index]

    append_message = {'msg': expand_msg,
                      'kwargs': fmt_kwargs
                      }

    return part_to_child(stu_part, sol_part, append_message, state)

def has_part(name, msg, state=None, fmt_kwargs=None):
    rep = Reporter.active_reporter
    d = {'sol_part': state.solution_parts,
         'stu_part': state.student_parts,
         **fmt_kwargs
         }

    try: 
        part = state.student_parts[name]
        if part is None: raise KeyError
    except (KeyError, IndexError):
        _msg = state.build_message(msg, d)
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    return state


def has_equal_part(name, msg, state):
    rep = Reporter.active_reporter
    d = {'stu_part': state.student_parts,
         'sol_part': state.solution_parts,
         'name': name}

    if d['stu_part'][name] != d['sol_part'][name]:
        _msg = state.build_message(msg, d)
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    return state


def has_equal_part_len(name, insufficient_msg, state=None):
    rep = Reporter.active_reporter
    d = dict(stu_len = len(state.student_parts[name]),
             sol_len = len(state.solution_parts[name]))

    if d['stu_len'] != d['sol_len']:
        _msg = state.build_message(insufficient_msg, d)
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    return state

def has_equal_value(msg, state=None):
    from pythonwhat.tasks import getResultInProcess, ReprFail
    from pythonwhat.Test import EqualTest
    rep = Reporter.active_reporter
    eval_solution, str_solution = getResultInProcess(tree = state.solution_tree,
                                                     context = state.solution_context,
                                                     process = state.solution_process)
    if str_solution is None:
        raise ValueError("Evaluating a default argument in the solution environment raised an error")
    if isinstance(eval_solution, ReprFail):
        raise ValueError("Couldn't figure out the value of a default argument: " + eval_solution.info)

    eval_student, str_student = getResultInProcess(tree = state.student_tree,
                                                   context = state.student_context,
                                                   process = state.student_process)

    _msg = state.build_message(msg, {'stu_part': state.student_parts, 'sol_part': state.solution_parts})
    feedback = Feedback(_msg, state.highlight)
    if isinstance(str_student, Exception):
        rep.do_test(Test(feedback))
    else:
        rep.do_test(EqualTest(eval_student, eval_solution, feedback))

    return state

def extend(*args, state=None):
    """Run multiple subtests in sequence, each using the output state of the previous."""

    # when input is a single list of subtests
    args = args[0] if len(args) == 1 and hasattr(args[0], '__iter__') else args

    for test in args: state = test(state=state)  # run tests sequentially
    return state                                 # return final state for chaining

def multi(*args, state=None):
    """Run multiple subtests. Return original state (for chaining)."""
    if any(args):
        rep = Reporter.active_reporter

        # when input is a single list of subtests
        args = args[0] if len(args) == 1 and isinstance(args[0], (list, tuple)) else args

        for test in args:
            # assume test is function needing a state argument
            # partial state so reporter can test
            # TODO: it seems clear the reporter doesn't need to hold state anymore
            closure = partial(test, state=state)
            # message from parent checks
            prefix = state.build_message()
            # resetting reporter message until it can be refactored
            prev_msg = rep.failure_msg
            rep.do_test(closure, prefix, state.highlight)
            rep.failure_msg = prev_msg

    # return original state, so can be chained
    return state

def quiet(n = 0, state=None):
    """Turn off prepended messages. Defaults to turning all off."""
    cpy = copy.copy(state)
    hushed = [{**m, 'msg': ""} for m in cpy.messages]
    cpy.messages = hushed
    return cpy

from pythonwhat.tasks import setUpNewEnvInProcess, breakDownNewEnvInProcess
def with_context(*args, state=None):
    # set up context in processes
    solution_res = setUpNewEnvInProcess(process = state.solution_process,
                                        context = state.solution_parts['with_items'])
    if isinstance(solution_res, Exception):
        raise Exception("error in the solution, running test_with() on with %d: %s" % (index - 1, str(solution_res)))

    student_res = setUpNewEnvInProcess(process = state.student_process,
                                       context = state.student_parts['with_items'])
    if isinstance(student_res, AttributeError):
        rep.do_test(Test(Feedback("In your %s `with` statement, you're not using a correct context manager." % (get_ord(index)), child.highlight)))

    if isinstance(student_res, (AssertionError, ValueError, TypeError)):
        rep.do_test(Test(Feedback("In your %s `with` statement, the number of values in your context manager " + \
            "doesn't correspond to the number of variables you're trying to assign it to." % (get_ord(index)), child.highlight)))

    # run subtests
    try:
        multi(*args, state=state)
    finally:
        # exit context
        if breakDownNewEnvInProcess(process = state.solution_process):
            raise Exception("error in the solution, closing the %s with fails with: %s" %
                (get_ord(index), close_solution_context))

        if breakDownNewEnvInProcess(process = state.student_process):

            rep.do_test(Test(Feedback("Your %s `with` statement can not be closed off correctly, you're " + \
                            "not using the context manager correctly." % (get_ord(index)), state.highlight)),
                        fallback_ast = state.highlight)
    return state

def set_context(*args, state=None, **kwargs):
    stu_crnt = state.student_context.context
    sol_crnt = state.solution_context.context
    # set args specified by pos ----
    upd_stu = stu_crnt.update(dict(zip(sol_crnt.keys(), args)))
    upd_sol = sol_crnt.update(dict(zip(stu_crnt.keys(), args)))

    # set args specified by keyword ----
    out_sol = upd_sol.update(kwargs)
    # need to match keys in kwargs with corresponding keys in stu context
    # in case they used, e.g., different loop variable names
    match_keys = dict(zip(sol_crnt.keys(), stu_crnt.keys()))
    out_stu = upd_stu.update({match_keys[k]: v for k,v in kwargs.items()})

    return state.to_child_state(student_subtree = None, solution_subtree = None,
                                student_context = out_stu, solution_context = out_sol)


def check_arg(name, missing_msg='check the argument `{part}`, ', state=None):
    if name in ['*args', '**kwargs']:
        return check_part(name, name, state=state, missing_msg = missing_msg)
    else: 
        return check_part_index('args', name, name, state=state, missing_msg = missing_msg)
