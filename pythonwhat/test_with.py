import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedTest, EqualTest, Test

from pythonwhat import utils

def test_with(index,
              body=None,
              undefined_msg=None):
    """Test a with statement.


    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_with")

    state.extract_withs()
    solution_withs = state.solution_withs
    student_withs = state.student_withs

    try:
        solution_with = solution_withs[name]
    except KeyError:
        raise NameError("not enough with statements in solution environment" % name)

    try:
        student_with = student_withs[index]
    except:
        rep.do_test(Test(undefined_msg or "Define more `with` statements."))
        return

    if body is not None:
        subtree_solution = solution_with['body']
        subtree_student = student_with['body']
        failed_before = rep.failed_test
        child = state.to_child_state(subtree_student, subtree_solution)
        child.context_solution = [arg[0] for arg in args_solution]
        child.context_student = [arg[0] for arg in args_student]
        body()
        child.to_parent_state()
        if expand_message and (failed_before is not rep.failed_test):
            rep.feedback_msg = ("In the `with` statement on line %d, " % student_with['lineno']) + \
                rep.feedback_msg
    if rep.failed_test:
        return

def context_env_update(context_list, env):
    env_update = {}
    for context in context_list:
        context_obj = eval(
            compile(context['context_expr'], '<context_eval>', 'eval'),
            env).__enter__()
        context_keys = context['optional_vars']
        if context_keys is None:
            continue
        elif len(context_keys) == 1:
            env_update[context_keys[0]] = context_obj
        else:
            assert len(context_keys) == len(context_obj)
            for (context_key, current_obj) in zip(context_keys, context_obj):
                env_update[context_key] = current_obj
    return env_update

