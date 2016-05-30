from pythonwhat.State import State

import copy

def set_extra_env(student_env=None, solution_env=None, extra_env=None):
    state = State.active_state

    student_env = student_env or state.student_env
    solution_env = solution_env or state.solution_env

    if extra_env is not None:
        student_env.update(copy.deepcopy(extra_env))
        solution_env.update(copy.deepcopy(extra_env))
