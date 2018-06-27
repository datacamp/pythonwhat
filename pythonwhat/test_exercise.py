from pythonwhat.State import State
from pythonwhat.utils import check_str, check_dict, check_process
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import TestFail
from pythonwhat.probe import create_test_probes
from pythonwhat.check_syntax import spec_2_context
from functools import partial

# utilities for signatures
cntxt = {}
exec("from pythonwhat.test_funcs import *", None, cntxt)

imports = """
from inspect import Parameter as param
from pythonwhat.signatures import sig_from_params, sig_from_obj
from pythonwhat.State import set_converter
# spec v2 functions
from pythonwhat.check_syntax import F, Ex
"""
exec(imports, None, cntxt)

def test_exercise(sct,
                  student_code,
                  solution_code,
                  pre_exercise_code,
                  student_process,
                  solution_process,
                  raw_student_output,
                  ex_type,
                  error):
    """
    Point of interaction with the Python backend.
    Args:
            sct (str): The solution corectness test as a string of code.
            student_code (str): The code which is entered by the student.
            solution_code (str): The code which is in the solution.
            pre_exercise_code (str): The code which is executed pre exercise.
            student_process (Process): Process in which the student code was executed.
            solution_process (Process): Process in which the solution code was executed.
            raw_student_output (str): The output which is given by executing the student's program.
            ex_type (str): The type of the exercise.
            error (tuple): A tuple with some information on possible errors.
    Returns:
            dict: Returns dict with correct - whether the SCT passed, message - the feedback message and
              tags - the tags belonging to the SCT execution.
    """

    rep = Reporter(error)
    Reporter.active_reporter = rep

    try:
        state = State(
            student_code = check_str(student_code),
            solution_code = check_str(solution_code),
            pre_exercise_code = check_str(pre_exercise_code),
            student_process = check_process(student_process),
            solution_process = check_process(solution_process),
            raw_student_output = check_str(raw_student_output)
        )

        State.root_state = state

        # Populate sct context with 'old' functions (in terms of probes) and check functions.
        tree, sct_cntxt = create_test_probes(cntxt)
        sct_cntxt.update(spec_2_context)

        # Actually execute SCTs
        exec(sct, sct_cntxt)         # Spec v2 tests run immediately
        for test in tree.crnt_node:  # Spec v1 tests run after
            test(state)

    except TestFail as e:
        return e.payload

    return rep.build_final_payload()


def success_msg(message):
    """
    Set the succes message of the sct. This message will be the feedback if all tests pass.
    Args:
            message (str): A string containing the feedback message.
    """
    rep = Reporter.active_reporter
    rep.success_msg = message

def allow_errors():
    rep = Reporter.active_reporter
    rep.errors_allowed = True

cntxt['success_msg'] = success_msg
