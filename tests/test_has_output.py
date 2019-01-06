import pytest
import helper
from pythonwhat.local import setup_state


@pytest.mark.parametrize(
    "stu, passes",
    [
        ('print("Hi, there!")', True),
        ('print("hi  there!")', True),
        ('print("Hello there")', False),
    ],
)
def test_has_output_basic(stu, passes):
    s = setup_state(stu, "")
    with helper.verify_sct(passes):
        s.has_output(r"[H|h]i,*\s+there!")


@pytest.mark.parametrize(
    "stu, passes",
    [
        ('print("Hi, there!")', True),
        ('print("hi  there!")', False),
        ('print("Hello there")', False),
    ],
)
def test_has_output_pattern(stu, passes):
    s = setup_state(stu, "")
    with helper.verify_sct(passes):
        s.has_output("Hi, there!", pattern=False)


@pytest.mark.parametrize(
    "stu, passes",
    [
        ('print("Hi, there!")', True),
        ('print("hi  there!")', True),
        ('print("Hello there")', False),
    ],
)
def test_test_output_contains(stu, passes):
    s = setup_state(stu, "")
    with helper.verify_sct(passes):
        s.test_output_contains(r"[H|h]i,*\s+there!")
