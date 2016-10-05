from pythonwhat.Feedback import Feedback
from pythonwhat.State import State
import inspect

def sub_test(state, rep, closure, subtree_student=None, subtree_solution=None, incorrect_part="",
                student_context=None, solution_context=None, expand_message=""):
    # recurse for a list of tests
    if hasattr(closure, '__len__'):
        for c in closure: 
            sub_test(state, rep, c, subtree_student, subtree_solution, incorrect_part,
                    student_context, solution_context, expand_message)
        return
    # otherwise, call a single test
    elif closure:
        # check if it's using the old closure syntax
        pars = inspect.signature(closure).parameters
        state_arg = lambda arg: arg.default == arg.empty and arg.name == "state"
        n_pos_args = sum(map(state_arg, pars.values()))
        if n_pos_args == 0: State.TEST_CLOSURE_SYNTAX = True

        # need to set child state so, if it is a closure that calls sub-tests
        # they can get the state they need off the State class
        descend_to_child = subtree_student and subtree_solution
        if descend_to_child:
            child = state.to_child_state(subtree_student, subtree_solution)
        else:
            # TODO set child to state
            child = State.active_state

        if student_context is not None:
            child.student_context = student_context
        if solution_context is not None:
            child.solution_context = solution_context
        
        prefix = expand_message.format(incorrect_part=incorrect_part) if expand_message else ""
        rep.do_test(closure, prefix, subtree_student)

        if descend_to_child: 
            child.to_parent_state()
        State.TEST_CLOSURE_SYNTAX = False


from functools import wraps, partial
def state_decorator(f):
    """
    Decorate test_* functions, to inject state when run in test closures.
    
    This decorator works around the old approach of implicitly passing a mutable 
    state between a parent test_* function and its sub tests. It allows the new
    syntax where state is part of the signature (and TODO immutable).
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        ba = inspect.signature(f).bind(*args, **kwargs)
        ba.apply_defaults()
        if ba.arguments.get('state'):
            return f(*args, **kwargs)
        elif State.TEST_TOP_LEVEL:
            State.TEST_TOP_LEVEL = False
            res = f(*args, **kwargs, state=State.active_state)
            State.TEST_TOP_LEVEL = True
            return res
        elif State.TEST_CLOSURE_SYNTAX:   # old style test closure
            return f(*args, **kwargs, state=State.active_state)
        else:                           # poor man's currying when state is None
            return partial(f, *args, **kwargs)
    
    return wrapper
