import pytest
import helper
import requests


def build_data(course_id, chapter_id, ex_number, printout=False):
    url = "https://www.datacamp.com/api/courses/{course_id}/chapters/{chapter_id}/exercises.json".format(
        course_id=course_id, chapter_id=chapter_id
    )
    resp = requests.get(url)
    assert resp.status_code == 200
    ex = resp.json()[ex_number - 1]

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
    data = build_data(735, 1842, 2)
    output = helper.run(data)
    assert output["correct"]
