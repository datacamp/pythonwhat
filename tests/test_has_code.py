import pytest
import tests.helper as helper
from pythonwhat.test_exercise import setup_state


@pytest.mark.parametrize("stu, passes", [("", False), ("c", False), ("a == c", True)])
def test_basic(stu, passes):
    s = setup_state(stu, "", pec="c,a=0,0")
    with helper.verify_sct(passes):
        s.has_code("a|b")


@pytest.mark.parametrize(
    "stu, passes", [("", False), ("c", False), ("a == c", False), ('"a|b"', True)]
)
def test_basic_pattern(stu, passes):
    s = setup_state(stu, "", pec="a,c=0,0")
    with helper.verify_sct(passes):
        s.has_code("a|b", pattern=False)
