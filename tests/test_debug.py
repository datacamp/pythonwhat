import tests.helper as helper
import json

from protowhat.failure import InstructorError


def test_debug_on_error():
    data = {
        "DC_PEC": "",
        "DC_CODE": "x = 123",
        "DC_SOLUTION": "x = 122",
        "DC_SCT": "Ex()._debug(on_error=True).check_object('x').has_equal_value()",
    }
    try:
        output = helper.run(data)
    except InstructorError as e:
        assert "SCT" in str(e)

    # if InstructorError doesn't raise:
    # assert not output["correct"]
    # assert "SCT" in output["message"]


def build_data(ex_number, printout=False):
    # "https://www.datacamp.com/api/courses/735/chapters/1842/exercises.json"
    with open('tests/test_debug_exercises.json') as exercises_json:
        ex = json.load(exercises_json)[ex_number - 1]

    pec = ex.get("pre_exercise_code", "")
    sol = ex.get("solution", "")
    sct = ex.get("sct", "")

    if printout:
        print("\n\n\n\n")
        print("## PEC ######################\n")
        print(pec)
        print("## SOL ######################\n")
        print(sol)
        print("## SCT ######################\n")
        print(sct)
        print("#############################\n")
        print("\n\n\n\n")

    return {"DC_PEC": pec, "DC_CODE": sol, "DC_SOLUTION": sol, "DC_SCT": sct}


def test_normal_pass():
    code = "x = 123"
    data = {
        "DC_PEC": "",
        "DC_CODE": code,
        "DC_SOLUTION": code,
        "DC_SCT": "success_msg('great')",
    }
    output = helper.run(data)
    assert output["correct"]


def test_dc_exercise():
    data = build_data(2)
    output = helper.run(data)
    assert output["correct"]
