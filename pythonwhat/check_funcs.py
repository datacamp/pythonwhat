from pythonwhat.Reporter import Reporter
from functools import partial

def check_part(name, part_msg, state=None):
    """Return child state with name part as its ast tree"""
    if not part_msg: part_msg = name
    child = state.to_child_state(state.student_parts[name], state.solution_parts[name])
    # TODO this is a hack to add the part name {part} to the messages in the previous check_* state
    import copy
    msg = copy.copy(child.messages[-2])
    msg.update(kwargs = {**msg['kwargs'], 'part': part_msg})
    child.messages[-2] = msg
    return child

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

