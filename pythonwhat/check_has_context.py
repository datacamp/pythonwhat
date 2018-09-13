from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test, EqualTest
from pythonwhat.Feedback import Feedback, InstructorError
from pythonwhat.State import State
from functools import singledispatch
from pythonwhat.check_funcs import check_part_index

MSG_INCORRECT_LOOP = "Have you used the correct iterator variable names? Was expecting `{{sol_vars}}` but got `{{stu_vars}}`."
MSG_INCORRECT_WITH = "Make sure to use the correct context variable names. Was expecting `{{sol_vars}}` but got `{{stu_vars}}`."

def has_context(incorrect_msg=None, exact_names=False, state=None):
    # call _has_context, since the built-in singledispatch can only use 1st pos arg
    return _has_context(state, incorrect_msg, exact_names)

def _test(state, incorrect_msg, exact_names, tv_name, highlight_name):
    rep = Reporter.active_reporter
    # get parts for testing from state
    # TODO: this could be rewritten to use check_part_index -> has_equal_part, etc..
    stu_vars = state.student_parts[tv_name]
    sol_vars = state.solution_parts[tv_name]

    child_state = state.to_child_state(student_subtree = state.student_parts.get(highlight_name),
                                       solution_subtree = state.solution_parts.get(highlight_name))

    # variables exposed to messages
    d = { 'stu_vars': stu_vars, 
          'sol_vars': sol_vars, 
          'num_vars': len(sol_vars)}

    if exact_names:
        # message for wrong iter var names
        _msg = state.build_message(incorrect_msg, d)
        # test
        rep.do_test(EqualTest(stu_vars, sol_vars, Feedback(_msg, child_state)))
    else:
        # message for wrong number of iter vars
        _msg = state.build_message(incorrect_msg, d)
        # test
        rep.do_test(EqualTest(len(stu_vars), len(sol_vars), Feedback(_msg, child_state)))

    return state


@singledispatch
def _has_context(state, incorrect_msg, exact_names):
    raise InstructorError("first argument to _has_context must be a State instance or subclass")

@_has_context.register(State)
def has_context_state(*args, **kwargs):
    return _test(*args, tv_name='target_vars', highlight_name='highlight', **kwargs)

@_has_context.register(State.SUBCLASSES['for_loops'])
@_has_context.register(State.SUBCLASSES['whiles'])
@_has_context.register(State.SUBCLASSES['dict_comps'])
@_has_context.register(State.SUBCLASSES['generator_exps'])
@_has_context.register(State.SUBCLASSES['list_comps'])
def has_context_loop(state, incorrect_msg, exact_names):
    """When dispatched on loops, has_context the target vars are the attribute _target_vars.

    Note: This is to allow people to call has_context on a node (e.g. for_loop) rather than
          one of its attributes (e.g. body). Purely for convenience.
    """
    return _test(state, incorrect_msg or MSG_INCORRECT_LOOP, exact_names,
                        tv_name='_target_vars', highlight_name='target')

@_has_context.register(State.SUBCLASSES['withs'])
def has_context_with(state, incorrect_msg, exact_names):
    """When dispatched on with statements, has_context loops over each context manager.

    Note: This is to allow people to call has_context on the with statement, rather than
          having to manually loop over each context manager.

          e.g. Ex().check_with(0).has_context() vs Ex().check_with(0).check_context(0).has_context()
    """

    for i in range(len(state.solution_parts['context'])):
        ctxt_state = check_part_index('context', i, '{{ordinal}} context', state=state)
        _has_context(ctxt_state, incorrect_msg or MSG_INCORRECT_WITH, exact_names)

    return state
