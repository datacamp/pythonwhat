import pytest
import tests.helper as helper


@pytest.mark.parametrize("stu, passes", [("c", False), ("a = 3", True)])
def test_basic(stu, passes):
    res = helper.run(
        {"DC_CODE": stu, "DC_SOLUTION": "", "DC_SCT": "Ex().has_no_error()"}
    )
    assert res["correct"] == passes
