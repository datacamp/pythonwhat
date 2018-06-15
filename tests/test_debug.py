import pytest
import helper

def test_normal_pass():
    code = "x = 123"
    data = {
		"DC_PEC": "",
		"DC_CODE": code,
        "DC_SOLUTION": code,
		"DC_SCT": "success_msg('great')"
	}
    output = helper.run(data)
    assert output['correct']