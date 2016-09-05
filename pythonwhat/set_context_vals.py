from pythonwhat.State import State

def set_context_vals(student_env=None, solution_env=None, context_vals=None):
    state = State.active_state

    student_env = student_env or state.student_env
    solution_env = solution_env or state.solution_env

    if context_vals is not None and context_vals is not []:
        if len(state.student_context) > 1:
            student_env.update({key: value for (key, value) in zip(
                state.student_context, context_vals)})
        else:
            student_env.update({state.student_context[0]: (
                context_vals[0] if len(context_vals) == 1 else context_vals)})

        if len(state.solution_context) > 1:
            solution_env.update({key: value for (key, value) in zip(
                state.solution_context, context_vals)})
        else:
            solution_env.update({state.solution_context[0]: (
                context_vals[0] if len(context_vals) == 1 else context_vals)})
