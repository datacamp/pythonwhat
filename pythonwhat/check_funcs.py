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
                                    append_message = append_message)
    
    # otherwise, assume they are just nodes
    return state.to_child_state(stu_part, sol_part, append_message = append_message)


def check_part(name, part_msg, state=None, missing_msg=""):
    """Return child state with name part as its ast tree"""
    rep = Reporter.active_reporter

    if not part_msg: part_msg = name
    append_message = {'msg': "", 'kwargs': {'part': part_msg,}}

    has_part(name, missing_msg, state, append_message['kwargs'])

    stu_part = state.student_parts[name]
    sol_part = state.solution_parts[name]
    
    return part_to_child(stu_part, sol_part, append_message, state)

def check_part_index(name, index, part_msg, 
                     missing_msg="Define more {part}.", 
                     state=None):
    """Return child state with indexed name part as its ast tree"""

    rep = Reporter.active_reporter

    # create message
    ordinal = "" if isinstance(index, str) else get_ord(index+1)

    append_message = {'msg': "", 
                      'kwargs': {'part': part_msg, 'index': index, 'ordinal': ordinal}}

    # check there are enough parts for index
    stu_parts = state.student_parts[name]
    try: stu_parts[index]
    except (KeyError, IndexError): 
        _msg = state.build_message(missing_msg, append_message['kwargs'])
        rep.do_test(Test(Feedback(_msg, state.student_tree)))

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
        rep.do_test(Test(Feedback(_msg, state.student_tree)))

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

    if not d['stu_part'][name] is not None:
        _msg = state.build_message(msg, d)
        rep.do_test(Test(Feedback(_msg, state.student_tree)))

    return state


def has_equal_part(name, msg, state):
    rep = Reporter.active_reporter
    d = {'stu_part': state.student_parts,
         'sol_part': state.solution_parts,
         'name': name}

    if d['stu_part'][name] != d['sol_part'][name]:
        _msg = state.build_message(msg, d)
        rep.do_test(Test(Feedback(_msg, state.student_tree)))

    return state


def has_equal_part_len(name, insufficient_msg, state=None):
    rep = Reporter.active_reporter
    d = dict(stu_len = len(state.student_parts[name]),
             sol_len = len(state.solution_parts[name]))

    if d['stu_len'] != d['sol_len']:
        _msg = state.build_message(insufficient_msg, d)
        rep.do_test(Test(Feedback(_msg, state.student_tree)))

    return state

def has_equal_value(msg, state=None):
    from pythonwhat.tasks import getTreeResultInProcess
    from pythonwhat.Test import EqualTest
    rep = Reporter.active_reporter
    eval_solution, str_solution = getTreeResultInProcess(tree = state.solution_tree,
                                                        process = state.solution_process)
    #if str_solution is None:
    #    raise ValueError("Evaluating a default argument in the solution environment raised an error")
    #if isinstance(eval_solution, ReprFail):
    #    raise ValueError("Couldn't figure out the value of a default argument: " + eval_solution.info)

    eval_student, str_student = getTreeResultInProcess(tree = state.student_tree, 
                                                    process = state.student_process)

    _msg = state.build_message(msg, {'stu_part': state.student_parts, 'sol_part': state.solution_parts})
    feedback = Feedback(_msg, state.student_tree)
    if str_student is None:
        rep.do_test(Test(feedback))
    else :
        rep.do_test(EqualTest(eval_student, eval_solution, feedback))


def multi(*args, state=None):
    """Run multiple subtests. Return original state (for chaining)."""
    if any(args):
        rep = Reporter.active_reporter
        # when input is a single list of subtests
        args = args[0] if len(args) == 1 and hasattr(args[0], '__iter__') else args

        for test in args:
            # assume test is function needing a state argument
            # partial state so reporter can test
            # TODO: it seems clear the reporter doesn't need to hold state anymore
            closure = partial(test, state=state)
            # message from parent checks
            prefix = state.build_message()
            # resetting reporter message until it can be refactored
            prev_msg = rep.failure_msg
            rep.do_test(closure, prefix, state.student_tree)
            rep.failure_msg = prev_msg
 
    # return original state, so can be chained
    return state

def quiet(n = 0, state=None):
    """Turn off prepended messages. Defaults to turning all off."""
    cpy = copy.copy(state)
    hushed = [{**m, 'msg': ""} for m in cpy.messages]
    cpy.messages = hushed
    return cpy