from pythonwhat.State import State
from pythonwhat.utils import check_str, check_dict, check_process
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import TestFail
from pythonwhat.sub_test import state_decorator
from pythonwhat.probe import create_test_probes

# utilities for signatures
cntxt = {}
exec("from pythonwhat.test_funcs import *", None, cntxt)
for t in cntxt: cntxt[t] = state_decorator(cntxt[t])


imports = """
from inspect import Parameter as param
from pythonwhat.signatures import sig_from_params, sig_from_obj
from pythonwhat.State import set_converter
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

    rep = Reporter()
    Reporter.active_reporter = rep

    state = State(
        student_code = check_str(student_code),
        solution_code = check_str(solution_code),
        full_student_code = check_str(student_code),
        full_solution_code = check_str(solution_code),
        pre_exercise_code = check_str(pre_exercise_code),
        student_process = check_process(student_process),
        solution_process = check_process(solution_process),
        raw_student_output = check_str(raw_student_output))

    State.set_active_state(state)
    State.TEST_TOP_LEVEL = True
    
    tree, sct_cntxt = create_test_probes(cntxt)
    exec(sct, sct_cntxt)

    # check if no fails yet (can be because of syntax and indentation errors)
    if not rep.failed_test:
        for test in tree.descend(): test.update_child_calls()
        try:
            #import pdb; pdb.set_trace()
            for test in tree.crnt_node: 
                test()
        except TestFail: pass

    return(rep.build_payload(error))


def success_msg(message):
    """
    Set the succes message of the sct. This message will be the feedback if all tests pass.
    Args:
            message (str): A string containing the feedback message.
    """
    rep = Reporter.active_reporter
    rep.set_success_msg(message)


def allow_errors():
    rep = Reporter.active_reporter
    rep.allow_errors()

cntxt['success_msg'] = success_msg
