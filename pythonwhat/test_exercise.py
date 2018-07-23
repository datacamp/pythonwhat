from pythonwhat.State import State
from pythonwhat.utils import check_str, check_dict, check_process
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import TestFail
from pythonwhat.utils import include_v1
from functools import partial
import os

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

        tree, sct_cntxt = prep_context()

        # Actually execute SCTs
        exec(sct, sct_cntxt)

        # Run remaining nodes on tree (v1 only)
        if tree:
            for test in tree.crnt_node:
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

def prep_context():
    cntxt = { 'success_msg': success_msg }
    from pythonwhat.check_syntax import v2_check_functions
    from pythonwhat.probe import build_probe_context
    imports = ["from inspect import Parameter as param",
               "from pythonwhat.signatures import sig_from_params, sig_from_obj",
               "from pythonwhat.State import set_converter",
               "from pythonwhat.check_syntax import F, Ex"]
    [ exec(line, None, cntxt) for line in imports ]

    # only if PYTHONWHAT_V2_ONLY is not set, support v1
    if include_v1():
        tree, probe_cntxt = build_probe_context()
        cntxt.update(probe_cntxt)
    else :
        tree = None

    cntxt.update(v2_check_functions)
    return tree, cntxt
