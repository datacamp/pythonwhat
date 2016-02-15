import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, EquivalentTest

from pythonwhat import utils

from contextlib import contextmanager

import copy


@contextmanager
def capture_output():
    import sys
    from io import StringIO
    oldout, olderr = sys.stdout, sys.stderr
    out = [StringIO(), StringIO()]
    sys.stdout, sys.stderr = out
    yield out
    sys.stdout, sys.stderr = oldout, olderr
    out[0] = out[0].getvalue()
    out[1] = out[1].getvalue()


def test_expression_output(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           eq_condition="equal",
                           pre_code=None,
                           keep_objs_in_env=None):
    state = State.active_state
    rep = Reporter.active_reporter

    eq_map = {"equal": EqualTest, "equivalent": EquivalentTest}

    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)

    student_expr = state.student_tree
    solution_expr = state.solution_tree

    student_env = utils.copy_env(state.student_env, keep_objs_in_env)
    solution_env = utils.copy_env(state.solution_env, keep_objs_in_env)

    if extra_env is not None:
        student_env.update(extra_env)
        solution_env.update(extra_env)

    if context_vals is not None:
        if len(state.context_student) > 1:
            student_env.update({key: value for (key, value) in zip(
                state.context_student, context_vals)})
        else:
            student_env.update({state.context_student[0]: (
                context_vals[0] if len(context_vals) == 1 else context_vals)})

        if len(state.context_solution) > 1:
            solution_env.update({key: value for (key, value) in zip(
                state.context_solution, context_vals)})
        else:
            solution_env.update({state.context_solution[0]: (
                context_vals[0] if len(context_vals) == 1 else context_vals)})

    try:
        with capture_output() as out:
            if pre_code is not None:
                exec(pre_code)
            exec(compile(student_expr, "<student>", "exec"), student_env)
        out_student = out[0].strip()
    except:
        out_student = None

    with capture_output() as out:
        if pre_code is not None:
            exec(pre_code)
        exec(compile(solution_expr, "<solution>", "exec"), solution_env)

    out_solution = out[0].strip()

    if incorrect_msg is not None:
        feedback_msg = incorrect_msg
    else:
        feedback_msg = "Unexpected expression output: expected `%s`, got `%s` with values" + \
            ((" " + str(extra_env)) if extra_env else ".")
        feedback_msg = feedback_msg % (utils.shorten_str(
            str(out_solution)), utils.shorten_str(str(out_student)))

    Reporter.active_reporter.do_test(
        eq_map[eq_condition](
            out_solution,
            out_student,
            feedback_msg))
