import pytest
import tests.helper as helper
from pythonwhat.test_exercise import setup_state
from pythonwhat.sct_syntax import v2_check_functions

set_env = v2_check_functions["set_env"]


@pytest.fixture
def state():
    return setup_state()


def test_set_env_basic(state):
    state.set_env(x=4).has_equal_value(name="x")


def test_set_env_once(state):
    state.set_env(x=4, y=5).has_equal_value(name="x").has_equal_value(name="y")


def test_set_env_twice(state):
    state.set_env(x=4).set_env(y=5).has_equal_value(name="x").has_equal_value(name="y")


def test_set_env_fail(state):
    with helper.verify_sct(False):
        state.multi(set_env(x=4), set_env(y=5).has_equal_value(name="x"))


@pytest.mark.parametrize(
    "stu, passes", [("print(a_list[1])", True), ("print(a_list[2])", False)]
)
def test_set_env_full_example(stu, passes):
    s = setup_state(stu, "print(a_list[1])", pec="a_list = [0, 1, 2]")
    with helper.verify_sct(passes):
        s.set_env(a_list=list(range(10))).has_equal_output()
