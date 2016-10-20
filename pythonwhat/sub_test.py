from pythonwhat.Feedback import Feedback
import inspect
from functools import wraps, partial
from pythonwhat.State import State

def sub_test(state, rep, closure, subtree_student=None, subtree_solution=None, incorrect_part="",
                student_context=None, solution_context=None, expand_message=""):

    expand_message = expand_message if expand_message else ""
    append_message = {'msg': expand_message, 'kwargs': dict(incorrect_part = incorrect_part)}
    # checking if a child_state is even necessary...
    if any([subtree_student, subtree_solution, student_context, solution_context, expand_message]):
        # if subtree_student and solution are None, state will copy set the other attributes on
        # a copy, rather than # creating a new instance
        child = state.to_child_state(subtree_student, subtree_solution,
                                        student_context, solution_context,
                                        append_message = append_message)
    else:
        child = state
    # recurse for a list of tests
    if hasattr(closure, '__len__'):
        for c in closure: 
            sub_test(child, rep, c, None, None, incorrect_part, None, None)
        return
    # otherwise, call a single test
    elif closure:
        # prefix message
        # TODO: can the line below be removed?
        # need to set child state if there are subtrees
        descend_to_child = subtree_student and subtree_solution
        # check if it has a state argument, set if not
        pars = inspect.signature(closure).parameters
        no_state = lambda arg: arg.default is None and arg.name == "state"
        has_no_state = any(map(no_state, pars.values()))
        if has_no_state: 
            #import pdb; pdb.set_trace()
            closure = partial(closure, state=child)

        # run sub test
        prefix = child.build_message()
        prev_msg = rep.failure_msg
        rep.do_test(closure, prefix, child.student_tree)
        rep.failure_msg = prev_msg
