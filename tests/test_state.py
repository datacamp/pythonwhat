import pytest
from pythonwhat.State import State
from pythonwhat.Feedback import InstructorError

def test_pec_parsing_error():
    with pytest.raises(InstructorError):
        State(
            student_code = 'parses',
            solution_code = 'parses',
            pre_exercise_code = 'does not parse',
        )
