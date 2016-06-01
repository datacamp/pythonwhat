from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

# explicitly import all functions so that they can be used in SCT
from pythonwhat.test_mc import test_mc
from pythonwhat.test_or import test_or
from pythonwhat.test_with import test_with
from pythonwhat.test_import import test_import
from pythonwhat.test_object import test_object
from pythonwhat.test_correct import test_correct
from pythonwhat.test_if_else import test_if_else
from pythonwhat.set_extra_env import set_extra_env
from pythonwhat.test_for_loop import test_for_loop
from pythonwhat.test_function import test_function
from pythonwhat.test_operator import test_operator
from pythonwhat.test_data_frame import test_data_frame
from pythonwhat.test_while_loop import test_while_loop
from pythonwhat.set_context_vals import set_context_vals
from pythonwhat.test_student_typed import test_student_typed
from pythonwhat.test_output_contains import test_output_contains
from pythonwhat.test_expression_result import test_expression_result
from pythonwhat.test_expression_output import test_expression_output
from pythonwhat.test_function_definition import test_function_definition
from pythonwhat.test_object_after_expression import test_object_after_expression

import markdown2
import re
# TODO (Vincent): Think about better package structure


def test_exercise(sct,
                  student_code,
                  solution_code,
                  pre_exercise_code,
                  student_environment,
                  solution_environment,
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
            student_environment (dict): A dictionary representing the ending environment of the student's program.
            solution_environment (dict): A dictionary representing the ending environment of the solution.
            raw_student_output (str): The output which is given by executing the student's program.
            ex_type (str): The type of the exercise.
            error (tuple): A tuple with some information on possible errors.
    Returns:
            dict: Returns dict with correct - whether the SCT passed, message - the feedback message and
              tags - the tags belonging to the SCT execution.
    """

    # Syntax errors will stop execution immediatly. Nothing to be tested.
    if (error):
        try:
            err_obj = error[1]
            if (issubclass(type(err_obj), SyntaxError)):
                if (issubclass(type(err_obj), IndentationError)):
                    feedback_msg = "Your code can not be excuted due to an error in the indentation: %s." % str(
                        err_obj)
                else:
                    feedback_msg = "Your code can not be excuted due to a syntax error: %s." % str(
                        err_obj)

                return({
                    "correct": False,
                    "message": feedback_msg,
                    "tags": {"fun": "syntax_error"}})
        except IndexError as e:
            # Something changed in the backend
            raise IndexError(
                "trying to find the error object but didn't find it")

    rep = Reporter()
    Reporter.active_reporter = rep
    state = State(
        student_code,
        solution_code,
        pre_exercise_code,
        student_environment,
        solution_environment,
        raw_student_output)
    # Standardly parse code
    state.parse_code()
    State.active_state = state

    if not rep.failed_test:
        exec(sct)

    if rep.failed_test:
        feedback_msg = rep.feedback_msg
    else:
        feedback_msg = rep.success_msg

    if (error and not rep.failed_test and not rep.allow_errors):
        feedback_msg = "Your code contains an error: " + str(error[1])
        return({
            "correct": False,
            "message": to_html(feedback_msg),
            "tags": rep.get_tags()})

    return({
        "correct": not rep.failed_test,
        "message": to_html(feedback_msg),
        "tags": rep.get_tags()})

def to_html(msg):
    return(re.sub("<p>(.*)</p>", "\\1", markdown2.markdown(msg)).strip())


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
