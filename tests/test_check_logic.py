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
    "sct, passes",
    [
        ("test_or(lambda: test_student_typed('a'))", True),
        ("test_or(test_student_typed('a'))", True),
        ("Ex().test_or(has_code('a'))", True),
        ("Ex().test_or(test_student_typed('a'))", True),
        (
            "test_or(lambda: test_student_typed('a'), lambda: test_student_typed('b'))",
            True,
        ),
        ("test_or(test_student_typed('a'), test_student_typed('b'))", True),
        ("Ex().test_or(has_code('a'), has_code('b'))", True),
        ("Ex().test_or(test_student_typed('a'), test_student_typed('b'))", True),
        (
            "test_or(lambda: test_student_typed('a'), lambda: test_student_typed('b'))",
            True,
        ),
        ("test_or(test_student_typed('a'), test_student_typed('b'))", True),
        ("Ex().test_or(has_code('a'), has_code('b'))", True),
        ("Ex().test_or(test_student_typed('a'), test_student_typed('b'))", True),
        ("test_or(lambda: test_student_typed('b'))", False),
        ("test_or(test_student_typed('b'))", False),
        ("Ex().test_or(has_code('b'))", False),
        ("Ex().test_or(test_student_typed('b'))", False),
        (
            "test_or(lambda: test_student_typed('b'), lambda: test_student_typed('c'))",
            False,
        ),
        ("test_or(test_student_typed('b'), test_student_typed('c'))", False),
        ("Ex().test_or(has_code('b'), has_code('c'))", False),
        ("Ex().test_or(test_student_typed('b'), test_student_typed('c'))", False),
    ],
)
def test_test_or(sct, passes):
    data = {"DC_CODE": "'a'", "DC_SCT": sct}
    output = helper.run(data)
    assert output["correct"] == passes


@pytest.mark.parametrize(
    "sct",
    [
        "Ex().check_or(has_code('a', not_typed_msg = 'a'), check_or(has_code('b'), has_code('c')))",
        "Ex().test_or(has_code('a', not_typed_msg = 'a'), F().test_or(has_code('b'), has_code('c')))",
        "test_or(test_student_typed('a', not_typed_msg = 'a'), test_or(test_student_typed('b'), test_student_typed('c')))",
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
    "sct, passes, msg",
    [
        (
            "test_correct(lambda: test_student_typed('a'), lambda: test_student_typed('b'))",
            True,
            None,
        ),
        ("test_correct(test_student_typed('a'), test_student_typed('b'))", True, None),
        ("Ex().test_correct(has_code('a'), has_code('b'))", True, None),
        (
            "Ex().test_correct(test_student_typed('a'), test_student_typed('b'))",
            True,
            None,
        ),
        (
            "test_correct(lambda: test_student_typed('a'), lambda: test_student_typed('c'))",
            True,
            None,
        ),
        ("test_correct(test_student_typed('a'), test_student_typed('c'))", True, None),
        ("Ex().test_correct(has_code('a'), has_code('c'))", True, None),
        (
            "Ex().test_correct(test_student_typed('a'), test_student_typed('c'))",
            True,
            None,
        ),
        (
            "test_correct(lambda: test_student_typed('b'), lambda: test_student_typed('c', not_typed_msg='x'))",
            False,
            "x",
        ),
        (
            "test_correct(test_student_typed('b'), test_student_typed('c', not_typed_msg='x'))",
            False,
            "x",
        ),
        (
            "Ex().test_correct(has_code('b'), has_code('c', not_typed_msg='x'))",
            False,
            "x",
        ),
        (
            "Ex().test_correct(test_student_typed('b'), test_student_typed('c', not_typed_msg='x'))",
            False,
            "x",
        ),
        (
            "test_correct(lambda: test_student_typed('b', not_typed_msg='x'), lambda: test_student_typed('a'))",
            False,
            "x",
        ),
        (
            "test_correct(test_student_typed('b', not_typed_msg='x'), test_student_typed('a'))",
            False,
            "x",
        ),
        (
            "Ex().test_correct(has_code('b', not_typed_msg='x'), has_code('a'))",
            False,
            "x",
        ),
        (
            "Ex().test_correct(test_student_typed('b', not_typed_msg='x'), test_student_typed('a'))",
            False,
            "x",
        ),
    ],
)
def test_test_correct(sct, passes, msg):
    data = {"DC_CODE": "'a'", "DC_SCT": sct}
    output = helper.run(data)
    assert output["correct"] == passes
    if msg:
        assert output["message"] == msg


@pytest.mark.parametrize(
    "sct",
    [
        "Ex().check_correct(has_code('a'), check_correct(has_code('b'), has_code('c', not_typed_msg = 'c')))",
        "Ex().test_correct(has_code('a'), F().test_correct(has_code('b'), has_code('c', not_typed_msg = 'c')))",
        "test_correct(test_student_typed('a'), test_correct(test_student_typed('b'), test_student_typed('c', not_typed_msg = 'c')))",
    ],
)
def test_nested_correct(sct):
    data = {"DC_CODE": "'def'", "DC_SCT": sct}
    sct_payload = helper.run(data)
    assert sct_payload["message"] == "c"
    assert not sct_payload["correct"]
