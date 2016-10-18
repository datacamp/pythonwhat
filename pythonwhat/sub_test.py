from pythonwhat.Feedback import Feedback
import inspect
from functools import wraps, partial
from pythonwhat.State import State

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
        #import pdb; pdb.set_trace()
        # need to set child state if there are subtrees
        descend_to_child = subtree_student and subtree_solution
        if descend_to_child:
            child = state.to_child_state(subtree_student, subtree_solution)
        else:
            child = state

        # change contexts
        if student_context  is not None: child.student_context  = student_context
        if solution_context is not None: child.solution_context = solution_context

        # check if it has a state argument, set if not
        pars = inspect.signature(closure).parameters
        no_state = lambda arg: arg.default is None and arg.name == "state"
        has_no_state = any(map(no_state, pars.values()))
        if has_no_state: 
            #import pdb; pdb.set_trace()
            closure = partial(closure, state=child)

        # run sub test
        prefix = expand_message.format(incorrect_part=incorrect_part) if expand_message else ""
        rep.do_test(closure, prefix, child.student_tree)
