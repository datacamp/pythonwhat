import pytest
import tests.helper as helper
from pythonwhat.test_exercise import setup_state


@pytest.mark.parametrize(
    "student_code, passes",
    [
        ('print("Hi, there!")', True),
        ('print("hi  there!")', True),
        ('print("Hello there")', False),
    ],
)
def test_has_output_basic(student_code, passes):
    s = setup_state(student_code, "")
    with helper.verify_sct(passes):
        s.has_output(r"[H|h]i,*\s+there!")


@pytest.mark.parametrize(
    "student_code, passes",
    [
        ('print("Hi, there!")', True),
        ('print("hi  there!")', False),
        ('print("Hello there")', False),
    ],
)
def test_has_output_pattern(student_code, passes):
    s = setup_state(student_code, "")
    with helper.verify_sct(passes):
        s.has_output("Hi, there!", pattern=False)


@pytest.mark.parametrize(
    "student_code, passes",
    [
        ('print("Hi, there!")', True),
        ('print("hi  there!")', True),
        ('print("Hello there")', False),
    ],
)
def test_test_output_contains(student_code, passes):
    s = setup_state(student_code, "")
    with helper.verify_sct(passes):
        s.test_output_contains(r"[H|h]i,*\s+there!")
