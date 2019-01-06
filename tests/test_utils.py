import pytest
from pythonwhat import utils


@pytest.mark.parametrize(
    "input, output", [(1, "first"), (2, "second"), (3, "third"), (11, "11th")]
)
def test_get_ord(input, output):
    assert utils.get_ord(input) == output


@pytest.mark.parametrize(
    "input, output", [(1, "one"), (2, "two"), (3, "three"), (11, "11")]
)
def test_get_num(input, output):
    assert utils.get_num(input) == output


@pytest.mark.parametrize(
    "input, output", [(1, "once"), (2, "twice"), (3, "three times"), (11, "11 times")]
)
def test_get_times(input, output):
    assert utils.get_times(input) == output
