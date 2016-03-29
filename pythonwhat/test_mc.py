
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest

MC_VAR_NAME = "selected_option"


def test_mc(correct, msgs):
    """Test multiple choice exercise.

    Test for a MultipleChoiceExercise. The correct answer (as an integer) and feedback messages
    are passed to this function.

    Args:
      correct (int): the index of the correct answer (should be an instruction). Starts at 1.
      msgs (list(str)): a list containing all feedback messages belonging to each choice of the
        student. The list should have the same length as the number of instructions.
    """
    if not issubclass(type(correct), int):
        raise ValueError("correct should be an integer")

    state = State.active_state
    student_env = state.student_env
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_mc")

    if MC_VAR_NAME not in student_env:
        raise NameError("%r not set in the student environment" % MC_VAR_NAME)
    else:
        selected_option = student_env[MC_VAR_NAME]
        if not issubclass(type(selected_option), int):
            raise ValueError("selected_option should be an integer")

        if selected_option < 1 or correct < 1:
            raise ValueError(
                "selected_option and correct should be greater than zero")

        if selected_option > len(msgs) or correct > len(msgs):
            raise ValueError("there are not enough feedback messages defined")

        feedback_msg = msgs[selected_option - 1]

        rep.set_success_msg(msgs[correct - 1])

        rep.do_test(EqualTest(selected_option, correct, feedback_msg))
