import helper
import pytest


@pytest.mark.backend
def test_check_function2():
    code = "round(2.718282, 3)"
    data = {
        "DC_SOLUTION": code, "DC_CODE": code,
        "DC_SCT": 'Ex().check_function("round").multi(check_args("number").has_equal_value("number"),check_args("ndigits").has_equal_value("ndigits"))'
    }
    sct_payload = helper.run(data)
    assert sct_payload.get('correct') is True

@pytest.mark.backend
def test_syntax():
    code = "x = 4\nif x > 0: print('x is positive')"
    data = {
        "DC_SOLUTION": code, "DC_CODE": code,
        "DC_SCT": """Ex().check_if_else(0).multi(check_test().test_student_typed(r"x\s+>\s+0"), check_body().check_function('print', 0).check_args('value').has_equal_value())"""
    }
    sct_payload = helper.run(data)
    assert sct_payload.get('correct') is True

