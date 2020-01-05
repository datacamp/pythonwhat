import json

import pytest
import tests.helper as helper


@pytest.fixture(scope="session", autouse=True)
def log_calls():
    yield
    print("Output test data")
    with open("docs/test_data.json", "w") as write_file:
        json.dump(helper.test_data, write_file)


def test_normal_pass():
    data = {
        "DC_PEC": "#no pec",
        "DC_CODE": "x = 4",
        "DC_SOLUTION": "x = 4",
        "DC_SCT": 'test_object("x")\nsuccess_msg("nice")',
    }
    output = helper.run(data)
    assert output["correct"]
    assert output["message"] == "nice"


def test_normal_fail():
    data = {
        "DC_PEC": "#no pec",
        "DC_CODE": "x = 4",
        "DC_SOLUTION": "x = 6",
        "DC_SCT": 'test_object("x")\nsuccess_msg("nice")',
    }
    output = helper.run(data)
    assert not output["correct"]


def test_normal_error():
    data = {
        "DC_PEC": "#no pec",
        "DC_CODE": "x = y",
        "DC_SOLUTION": "x = 6",
        "DC_SCT": "# no sct",
    }
    output = helper.run(data)
    assert not output["correct"]
    assert "Your code generated an error." in output["message"]


def test_syntax_error():
    data = {
        "DC_PEC": "# no pec",
        "DC_CODE": 'print "yolo"',
        "DC_SOLUTION": "x = 6",
        "DC_SCT": 'test_object("x")',
    }
    output = helper.run(data)
    assert not output["correct"]
    assert "Your code can not be executed due to a syntax error" in output["message"]


def test_indentation_error():
    data = {
        "DC_PEC": "# no pec",
        "DC_CODE": '	print("yolo")',
        "DC_SOLUTION": "x = 6",
        "DC_SCT": 'test_object("x")',
    }
    output = helper.run(data)
    assert not output["correct"]
    assert (
        "Your code could not be parsed due to an error in the indentation"
        in output["message"]
    )


def test_enrichment_error():
    data = {
        "DC_PEC": "# no pec",
        "DC_CODE": "",
        "DC_SOLUTION": "x = 6",
        "DC_SCT": 'test_object("x")',
    }
    output = helper.run(data)
    assert not output["correct"]
    # assert not "line_start" in output
