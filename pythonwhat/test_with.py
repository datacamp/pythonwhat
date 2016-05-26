import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedTest, EqualTest, Test

from pythonwhat import utils

def test_with(index):
    """Test a with statement.


    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_with")

    state.extract_withs()
    solution_defs = state.solution_withs
    student_defs = state.student_withs

    try:
        solution_def = solution_defs[name]
    except KeyError:
        raise NameError("%s not in solution environment" % name)


def context_env_update(context_list, env):
    env_update = {}
    for context in context_list:
        context_obj = eval(
            compile(context['context_expr'], '<context_eval>', 'eval'),
            env).__enter__()
        context_keys = context['optional_vars']
        if context_key is None:
            continue
        elif len(context_key) == 1:
            env_update[context_key] = context_obj
        else:
            if len(context_keys) != len(context_obj)
            for context_key in context_keys:

