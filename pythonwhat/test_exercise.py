from pythonwhat.State import State
from pythonwhat.Reporter import Reporter

from pythonwhat.test_mc import test_mc
from pythonwhat.test_import import test_import
from pythonwhat.test_object import test_object
from pythonwhat.test_if_else import test_if_else
from pythonwhat.test_for_loop import test_for_loop
from pythonwhat.test_function import test_function
from pythonwhat.test_operator import test_operator
from pythonwhat.test_while_loop import test_while_loop
from pythonwhat.test_student_typed import test_student_typed
from pythonwhat.test_output_contains import test_output_contains
from pythonwhat.test_expression_result import test_expression_result
from pythonwhat.test_expression_output import test_expression_output
from pythonwhat.test_object_after_expression import test_object_after_expression

import markdown2
import re
# TODO (Vincent): Have to move this shit


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
            tuple(bool,str): The first bool is true if the sct passed. The str contains the feedback message.
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

                return((
                    False,
                    feedback_msg,
                    None))
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
        return((
            False,
            to_html(feedback_msg),
            None))

    return((
        not rep.failed_test,
        to_html(feedback_msg),
        None))  # Implement challenge


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
