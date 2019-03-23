import pytest
import tests.helper as helper


@pytest.mark.parametrize(
    "stu_code, passes, mess",
    [
        ("selected_option = 1", False, "a"),
        ("selected_option = 2", True, "b"),
        ("selected_option = 3", False, "c"),
    ],
)
def test_has_chosen(stu_code, passes, mess):
    data = {"DC_CODE": stu_code, "DC_SCT": "test_mc(2, ['a', 'b', 'c'])"}
    res = helper.run(data)
    assert res["correct"] is passes
    assert res["message"] == mess

    data = {"DC_CODE": stu_code, "DC_SCT": "Ex().has_chosen(2, ['a', 'b', 'c'])"}
    res = helper.run(data)
    assert res["correct"] is passes
    assert res["message"] == mess
