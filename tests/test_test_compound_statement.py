import pytest
import tests.helper as helper
from pythonwhat.test_exercise import setup_state
from pythonwhat.sct_syntax import v2_check_functions

globals().update(v2_check_functions)

# Check for loop --------------------------------------------------------------


@pytest.mark.parametrize(
    "sct",
    [
        "test_for_loop(for_iter=lambda: test_expression_result(), body=lambda: test_expression_output())",
        "Ex().test_for_loop(for_iter=lambda: test_expression_result(), body=lambda: test_expression_output())",
        "Ex().check_for_loop().multi(check_iter().has_equal_value(), check_body().has_equal_output())",
    ],
)
@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("for i in range(4): pass", False),
        ("for i in range(3): pass", False),
        ("for i in range(3): print(i)", True),
        ("for j in range(3): print(j)", True),
    ],
)
def test_for_loop(sct, stu, passes):
    res = helper.run(
        {"DC_CODE": stu, "DC_SOLUTION": "for i in range(3): print(i)", "DC_SCT": sct}
    )
    assert res["correct"] == passes


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("for i in range(3):\n  pass", False),
        ("for i in range(3):\n  for j in range(3):\n    pass", False),
        ("for i in range(3):\n  for j in range(4):\n    pass", False),
        ("for i in range(3):\n  for j in range(4):\n    print(i + j)", True),
        ("for j in range(3):\n  for i in range(4):\n    print(i + j)", True),
    ],
)
def test_for_loop_nested(stu, passes):
    s = setup_state(stu, "for i in range(3):\n  for j in range(4):\n    print(i + j)")
    with helper.verify_sct(passes):
        s.check_for_loop().multi(
            check_iter().has_equal_value(),
            check_body()
            .set_context(2)
            .check_for_loop()
            .multi(check_iter(), check_body().set_context(3).has_equal_output()),
        )


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("for i in range(1):\n  pass", False),
        ("for i in range(1):\n  pass\nfor j in range(2): pass", False),
        ("for i in range(3):\n  pass\nfor j in range(4): pass", False),
        ("for i in range(3):\n  pass\nfor j in range(4): print(j)", True),
        ("for i in range(3):\n  pass\nfor i in range(4): print(i)", True),
    ],
)
def test_two_for_loops(stu, passes):
    s = setup_state(stu, "for i in range(1):\n  pass\nfor j in range(4): print(j)")
    with helper.verify_sct(passes):
        s.check_for_loop(index=1).multi(
            check_iter().has_equal_value(),
            check_body().set_context(2).has_equal_output(),
        )


@pytest.mark.parametrize(
    "stu, exact, passes",
    [
        ("for i in range(2): pass", False, True),
        ("for j in range(2): pass", False, True),
        ("for i in range(2): pass", True, True),
        ("for j in range(2): pass", True, False),
    ],
)
def test_has_context(stu, exact, passes):
    s = setup_state(stu, "for i in range(2): pass")
    with helper.verify_sct(passes):
        s.check_for_loop().check_body().has_context(exact_names=exact)


# Check while loop ------------------------------------------------------------


@pytest.mark.parametrize(
    "sct",
    [
        "test_while_loop(test = lambda: test_student_typed('3'), body = lambda: test_student_typed('print'))",
        "Ex().test_while_loop(test = test_student_typed('3'), body = test_student_typed('print'))",
        "Ex().check_while().multi(check_test().has_code('3'), check_body().has_code('print'))",
    ],
)
@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("while False: pass", False),
        ("while 3 > 4: pass", False),
        ("while 3 > 4: print(2)", True),
    ],
)
def test_while_loop(sct, stu, passes):
    res = helper.run(
        {"DC_CODE": stu, "DC_SOLUTION": "while 3 > 4: print(2)", "DC_SCT": sct}
    )
    assert res["correct"] == passes
