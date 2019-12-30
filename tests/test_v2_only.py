import pytest
import tests.helper as helper
import importlib


def relooooad():
    import pythonwhat.sct_syntax
    importlib.reload(pythonwhat.sct_syntax)


@pytest.fixture
def data():
    return {"DC_CODE": "x = round(4)", "DC_SOLUTION": "x = round(5)"}


@pytest.mark.parametrize(
    "sct",
    [
        "test_object('x')",
        "Ex().test_object('x')",
        "test_function('round')",
        "Ex().check_object('x').has_equal_value()",
        "Ex() >> check_object('x').has_equal_value()",
        "x = check_object('x').has_equal_value(); Ex() >> x",
    ],
)
def test_without_env_all_works(data, sct):
    data["DC_SCT"] = sct
    with helper.set_v2_only_env(""):
        relooooad()
        sct_payload = helper.run(data)
        assert not sct_payload["correct"]


@pytest.mark.parametrize(
    "sct, should_err",
    [
        ("test_object('x')", True),
        ("test_function('round')", True),
        ("Ex().test_object('x')", True),
        ("Ex().test_or(check_object('x').has_equal_value())", True),
        ("Ex().check_or(test_object('x'))", True),
        ("Ex().check_object('x').has_equal_value()", False),
        ("Ex() >> check_object('x').has_equal_value()", False),
        (
            "Ex().check_or(check_object('x').has_equal_value(), check_object('x').has_equal_value())",
            False,
        ),
        ("x = check_object('x').has_equal_value(); Ex() >> x", False),
    ],
)
def test_with_env_old_fail(data, sct, should_err):
    data["DC_SCT"] = sct
    with helper.set_v2_only_env("1"):
        relooooad()
        if should_err:
            with pytest.raises((NameError, AttributeError)):
                sct_payload = helper.run(data)
        else:
            sct_payload = helper.run(data)
            assert not sct_payload["correct"]
