import pytest
from pythonwhat.test_exercise import setup_state
from protowhat.failure import TestFail as TF
import tests.helper as helper


@pytest.mark.parametrize(
    "stu, correct",
    [
        ("print(1, 2, 3)", True),
        ("print('1 2 3')", True),
        ("print('1', '2 3')", True),
        ("print(1, '2 3')", True),
        ("print('1 2', '3')", True),
        ("print('1 2', 3)", True),
        ("print(1, 2)", False),
        ("print('1 2')", False),
        ("print('1 3 2')", False),
        ("print(1, 3, 2)", False),
        ("print(1, 2, 4, 3)", False),
        ("print('1 2 4 3')", False),
        ("print('1 2', 4, 3)", False),
    ],
)
def test_basic_has_printout(stu, correct):
    sol = "print(1, 2, 3)"
    s = setup_state(stu_code=stu, sol_code=sol)
    with helper.verify_sct(correct):
        s.has_printout(0)


def test_basic_has_printout_failing_custom():
    sol = "print(1, 2, 3)"
    stu = "print(1, 2)"
    s = setup_state(stu_code=stu, sol_code=sol)
    with pytest.raises(TF, match="wrong"):
        s.has_printout(0, not_printed_msg="wrong")


@pytest.mark.parametrize(
    "stu",
    [
        "print(1, 2, 3)",
        "print('1 2 3')",
        "print('1', '2 3')",
        "print(1, '2 3')",
        "print('1 2', '3')",
        "print('1 2', 3)",
    ],
)
def test_has_printout_multiple(stu):
    sol = 'print("randomness")\nprint(1, 2, 3)'
    s = setup_state(stu_code=stu, sol_code=sol)
    helper.passes(s.has_printout(1))
