import pytest
import tests.helper as helper


# TODO: extend tests
@pytest.mark.parametrize(
    "sct, passes",
    [
        ("Ex().check_not(has_code('a'), msg = 'x')", False),
        ("Ex().check_not(has_code('a'), has_code('b'), msg = 'x')", False),
        ("Ex().check_not(has_code('b'), msg = 'x')", True),
        ("Ex().check_not(has_code('b'), has_code('c'), msg = 'x')", True),
        (
            "Ex().check_not(check_object('a').has_equal_value(override=1), msg = 'x')",
            False,
        ),
        (
            "Ex().check_not(check_object('a').has_equal_value(override=2), msg = 'x')",
            True,
        ),
    ],
)
def test_check_not(sct, passes):
    data = {"DC_SOLUTION": "a = 1", "DC_CODE": "a = 1", "DC_SCT": sct}
    output = helper.run(data)
    assert output["correct"] == passes
    if not passes:
        assert output["message"] == "x"


@pytest.mark.parametrize(
    "sct, passes",
    [
        ("Ex().check_or(has_code('a'))", True),
        ("Ex().check_or(has_code('a'), has_code('b'))", True),
        ("Ex().check_or(has_code('b'))", False),
        ("Ex().check_or(has_code('b'), has_code('c'))", False),
    ],
)
def test_check_or(sct, passes):
    data = {"DC_CODE": "'a'", "DC_SCT": sct}
    output = helper.run(data)
    assert output["correct"] == passes


@pytest.mark.parametrize(
    "sct",
    [
        "Ex().check_or(has_code('a', not_typed_msg = 'a'), check_or(has_code('b'), has_code('c')))",
    ],
)
def test_nested_or(sct):
    data = {"DC_CODE": "'def'", "DC_SCT": sct}
    sct_payload = helper.run(data)
    assert sct_payload["message"] == "a"
    assert not sct_payload["correct"]


@pytest.mark.parametrize(
    "sct, passes, msg",
    [
        ("Ex().check_correct(has_code('a'), has_code('b'))", True, None),
        ("Ex().check_correct(has_code('a'), has_code('c'))", True, None),
        (
            "Ex().check_correct(has_code('b'), has_code('c', not_typed_msg='x'))",
            False,
            "x",
        ),
        (
            "Ex().check_correct(has_code('b', not_typed_msg='x'), has_code('a'))",
            False,
            "x",
        ),
    ],
)
def test_check_correct(sct, passes, msg):
    data = {"DC_CODE": "'a'", "DC_SCT": sct}
    output = helper.run(data)
    assert output["correct"] == passes
    if msg:
        assert output["message"] == msg


@pytest.mark.parametrize(
    "sct, passes, msg",
    [
        ("Ex().check_correct(has_code('a'), has_code('b'))", False, None),
        ("Ex().check_correct(has_code('a'), has_code('c'))", False, None),
        (
            "Ex().check_correct(has_code('b'), has_code('c', not_typed_msg='x'))",
            False,
            "x",
        ),
        (
            "Ex().check_correct(has_code('b', not_typed_msg='x'), has_code('a'))",
            False,
            "x",
        ),
    ],
)
def test_check_correct_force_diagnose(sct, passes, msg):
    data = {"DC_CODE": "'a'", "DC_SCT": sct, "DC_FORCE_DIAGNOSE": True}
    output = helper.run(data)
    assert output["correct"] == passes
    if msg:
        assert output["message"] == msg


@pytest.mark.parametrize(
    "sct",
    [
        "Ex().check_correct(has_code('a'), check_correct(has_code('b'), has_code('c', not_typed_msg = 'c')))",
    ],
)
def test_nested_correct(sct):
    data = {"DC_CODE": "'def'", "DC_SCT": sct}
    sct_payload = helper.run(data)
    assert sct_payload["message"] == "c"
    assert not sct_payload["correct"]
