import pytest
from protowhat.Reporter import Reporter
from pythonwhat.State import State
from protowhat.failure import InstructorError


def test_pec_parsing_error():
    with pytest.raises(InstructorError):
        State(
            student_code="parses",
            solution_code="parses",
            pre_exercise_code="does not parse",
            student_process=None,
            solution_process=None,
            reporter=Reporter(),
            raw_student_output=None,
        )
