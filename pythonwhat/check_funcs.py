from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test
from pythonwhat.Feedback import Feedback
from pythonwhat.utils import get_ord
from functools import partial

def check_part(name, part_msg, state=None):
    """Return child state with name part as its ast tree"""
    if not part_msg: part_msg = name
    child = state.to_child_state(state.student_parts[name], state.solution_parts[name],
                                 append_message = {'msg': "", 'kwargs': {'part': part_msg}})
    return child

def check_part_index(name, index, part_msg, 
                     missing_msg="Define more {part}.", 
                     state=None):
    """Return child state with indexed name part as its ast tree"""

    rep = Reporter.active_reporter

    # create message
    append_message = {'msg': "", 
                      'kwargs': {'part': get_ord(index+1) + " " + part_msg}}

    # check there are enough parts for index
    stu_parts = state.student_parts[name]
    try: stu_parts[index]
    except (KeyError, IndexError): 
        _msg = state.build_message(missing_msg, append_message['kwargs'])
        rep.do_test(Test(Feedback(_msg, state.student_tree)))

    # get part at index
    stu_part = state.student_parts[name][index]
    sol_part = state.solution_parts[name][index]
    
    # return child state
    child = state.to_child_state(stu_part, sol_part,
                                 append_message = append_message)
    return child

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
    child = state.to_child_state(stu_part['node'], sol_part['node'],
                                 stu_part.get('target_vars'), sol_part.get('target_vars'), 
                                 stu_part, sol_part,
                                 append_message)
    return child

def has_equal_part_len(name, insufficient_msg, state=None):
    rep = Reporter.active_reporter
    d = dict(stu_len = len(state.student_parts[name]),
             sol_len = len(state.solution_parts[name]))

    if d['stu_len'] != d['sol_len']:
        _msg = state.build_message(insufficient_msg, d)
        rep.do_test(Test(Feedback(_msg, state.student_tree)))

    return state

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
