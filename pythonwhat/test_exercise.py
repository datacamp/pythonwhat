from pythonwhat.State import State
from pythonwhat.utils import check_str, check_dict, check_process
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import TestFail

# explicitly import all functions so that they can be used in SCT
from pythonwhat.test_mc import test_mc
from pythonwhat.test_or import test_or
from pythonwhat.test_with import test_with
from pythonwhat.test_comp import test_list_comp
from pythonwhat.test_comp import test_dict_comp
from pythonwhat.test_comp import test_generator_exp
from pythonwhat.test_import import test_import
from pythonwhat.test_object import test_object
from pythonwhat.test_correct import test_correct
from pythonwhat.test_if_else import test_if_else
from pythonwhat.test_if_else import test_if_exp
from pythonwhat.test_for_loop import test_for_loop
from pythonwhat.test_function import test_function
from pythonwhat.test_function import test_print
from pythonwhat.test_function import test_function_v2
from pythonwhat.test_operator import test_operator
from pythonwhat.test_try_except import test_try_except
from pythonwhat.test_data_frame import test_data_frame
from pythonwhat.test_dictionary import test_dictionary
from pythonwhat.test_while_loop import test_while_loop
from pythonwhat.test_student_typed import test_student_typed
from pythonwhat.test_object_accessed import test_object_accessed
from pythonwhat.test_output_contains import test_output_contains
from pythonwhat.test_lambda_function import test_lambda_function
from pythonwhat.test_expression_result import test_expression_result
from pythonwhat.test_expression_output import test_expression_output
from pythonwhat.test_function_definition import test_function_definition
from pythonwhat.test_object_after_expression import test_object_after_expression

# utilities for signatures
from inspect import Parameter as param
from pythonwhat.signatures import sig_from_params, sig_from_obj
from pythonwhat.State import set_converter


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

    # check if no fails yet (can be because of syntax and indentation errors)
    if not rep.failed_test:
        try: 
            exec(sct)
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
