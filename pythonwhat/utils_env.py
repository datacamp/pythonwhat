import copy

# def set_extra_env(student_env=None, solution_env=None, extra_env=None):
#     state = State.active_state

#     student_env = student_env or state.student_env
#     solution_env = solution_env or state.solution_env

#     if extra_env is not None:
#         student_env.update(copy.deepcopy(extra_env))
#         solution_env.update(copy.deepcopy(extra_env))

# def set_context_vals(student_env=None, solution_env=None, context_vals=None):
#     state = State.active_state

#     student_env = student_env or state.student_env
#     solution_env = solution_env or state.solution_env

#     if context_vals is not None and context_vals is not []:
#         if len(state.context_student) > 1:
#             student_env.update({key: value for (key, value) in zip(
#                 state.context_student, context_vals)})
#         else:
#             student_env.update({state.context_student[0]: (
#                 context_vals[0] if len(context_vals) == 1 else context_vals)})

#         if len(state.context_solution) > 1:
#             solution_env.update({key: value for (key, value) in zip(
#                 state.context_solution, context_vals)})
#         else:
#             solution_env.update({state.context_solution[0]: (
#                 context_vals[0] if len(context_vals) == 1 else context_vals)})

def set_context_vals(env, context, context_vals = None):
    if context_vals is not None and context_vals is not []:
        if len(context) > 1:
            env.update({key: value for (key, value) in zip(context, context_vals)})
        else:
            env.update({context[0]: (context_vals[0] if len(context_vals) == 1 else context_vals)})
