import pytest
import tests.helper as helper
from pythonwhat.test_exercise import setup_state


def test_disable_highlighting():
    s = setup_state(stu_code="round(1.234, 2)", sol_code="round(2.345, 2)")
    assert s._state.highlighting_disabled is None
    assert s.disable_highlighting()._state.highlighting_disabled
    assert s.disable_highlighting().check_function("round")._state.highlighting_disabled
    assert s.check_function("round").disable_highlighting()._state.highlighting_disabled


@pytest.fixture
def data():
    return {"DC_CODE": "round(1.234, 2)", "DC_SOLUTION": "round(2.345, 2)"}


def test_with_highlighting(data):
    data[
        "DC_SCT"
    ] = 'Ex().check_function("round").check_args("number").has_equal_value()'
    output = helper.run(data)
    assert not output["correct"]
    helper.with_line_info(output, 1, 1, 7, 11)


@pytest.mark.parametrize(
    "sct",
    [
        'Ex().disable_highlighting().check_function("round").check_args("number").has_equal_value()',
        'Ex().check_function("round").disable_highlighting().check_args("number").has_equal_value()',
        'Ex().check_function("round").check_args("number").disable_highlighting().has_equal_value()',
    ],
)
def test_without_highlighting(data, sct):
    data["DC_SCT"] = sct
    output = helper.run(data)
    assert not output["correct"]
    helper.no_line_info(output)


@pytest.fixture
def first_ok():
    return {"DC_SOLUTION": "round(1)\nround(2)", "DC_CODE": "round(1)\nround(3)"}


@pytest.fixture
def second_ok():
    return {"DC_SOLUTION": "round(1)\nround(2)", "DC_CODE": "round(3)\nround(2)"}


@pytest.fixture
def second_solves_first():
    return {"DC_SOLUTION": "round(1)\nround(2)", "DC_CODE": "round(3)\nround(1)"}


@pytest.fixture
def first_solves_second():
    return {"DC_SOLUTION": "round(1)\nround(2)", "DC_CODE": "round(2)\nround(3)"}


def test_check_function_twice(
    first_ok, second_ok, second_solves_first, first_solves_second
):
    patt = (
        'Ex().check_function("round", index={}).check_args("number").has_equal_value()'
    )
    sct = patt.format(0) + "\n" + patt.format(1)
    first_ok["DC_SCT"] = sct
    output = helper.run(first_ok)
    assert not output["correct"]
    helper.with_line_info(output, 2, 2, 7, 7)

    second_ok["DC_SCT"] = sct
    output = helper.run(second_ok)
    assert not output["correct"]
    helper.with_line_info(output, 1, 1, 7, 7)

    second_solves_first["DC_SCT"] = sct
    output = helper.run(second_solves_first)
    assert not output["correct"]
    helper.with_line_info(output, 1, 1, 7, 7)

    first_solves_second["DC_SCT"] = sct
    output = helper.run(first_solves_second)
    assert not output["correct"]
    helper.with_line_info(output, 1, 1, 7, 7)

    first_ok["DC_SCT"] = patt.format(1)
    output = helper.run(first_ok)
    assert not output["correct"]
    helper.with_line_info(output, 2, 2, 7, 7)  ## THIS IS INTUITIVE!
