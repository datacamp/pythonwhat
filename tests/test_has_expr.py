import pytest
from pythonwhat.test_exercise import setup_state
from protowhat.failure import InstructorError
import tests.helper as helper


@pytest.mark.parametrize(
    "stu, passes", [("", False), ("a = 3", False), ("a = 2", True)]
)
def test_has_equal_value_basic(stu, passes):
    s = setup_state(stu, "a = 2")
    with helper.verify_sct(passes):
        s.has_equal_value(expr_code="a")


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("a = 0\nfor i in range(0): pass", False),
        ("a = 0\nfor i in range(0): a = a - 1", False),
        ("a = 0\nfor i in range(0): a = a + 1", True),
    ],
)
def test_has_equal_value_name(stu, passes):
    s = setup_state(stu, "a = 0\nfor i in range(0): a = 1")
    with helper.verify_sct(passes):
        s.check_for_loop().check_body().has_equal_value(name="a")


def test_has_equal_value_pickle():
    """limit deep copy of env when just reading value"""
    sol = """a = 1
class NoPickle(list):
    def __getstate__(self):
        raise TypeError("Can't pickle this")
b = NoPickle()
    """
    s = setup_state(sol, sol)
    with helper.verify_sct(True):
        s.check_object("a").has_equal_value()
    with helper.verify_sct(True):
        s.check_object("a").has_equal_value(name="a")
    with helper.verify_sct(True):
        s.has_equal_value(expr_code="a")
    with pytest.raises(InstructorError):
        s.has_equal_value(expr_code="a", name="a")
    with pytest.raises(InstructorError):
        s.has_equal_value(expr_code="print(a)")
    with pytest.raises(InstructorError):
        s.has_equal_value(expr_code="print(a)", name="a")
    with pytest.raises(InstructorError):
        s.has_equal_value(expr_code="print(a)")


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("a = 0\nfor i in range(0): pass", False),
        ("a = 0\nfor i in range(0): a = a - 1", False),
        ("a = 0\nfor i in range(0): a = a + 1", True),
    ],
)
def test_has_equal_value_old(stu, passes):
    out = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "a = 0\nfor i in range(0): a = a + 1",
            "DC_SCT": "test_for_loop(body = test_object_after_expression('a'))",
        }
    )
    out["correct"] == passes


@pytest.mark.parametrize(
    "stu, passes", [("", False), ('x = {"a": 2}', False), ('x = {"a": 1}', True)]
)
def test_has_equal_output_basic(stu, passes):
    s = setup_state(stu, 'x = {"a":1, "b":2, "c": 3}')
    with helper.verify_sct(passes):
        s.test_expression_output(expr_code='print(x["a"])')


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("for i in range(10):\n    print(i + 1)", False),
        ("for i in range(10):\n    print(i)", True),
    ],
)
@pytest.mark.parametrize("context_vals", [None, [1]])
def test_has_equal_output_for(stu, passes, context_vals):
    s = setup_state(stu, "for i in range(10):\n    print(i)")
    with helper.verify_sct(passes):
        s.check_for_loop().check_body().has_equal_output(context_vals=context_vals)


@pytest.mark.parametrize("copy, passes", [(False, True), (True, False)])
def test_copy_functionality(copy, passes):
    s = setup_state("a = [1]", "a = [2]")
    with helper.verify_sct(passes):
        s.has_equal_value(expr_code="a[0] = 3", name="a", copy=copy).has_equal_value(
            expr_code="a", name="a"
        )


@pytest.mark.parametrize("tol, passes", [(0.001, True), (0.0001, False)])
def test_test_custom_equality_func(tol, passes):
    s = setup_state("a = [1.011]", "a = [1.01]")
    import numpy as np

    with helper.verify_sct(passes):
        s.check_object("a").has_equal_value(
            func=lambda x, y: np.allclose(x, y, atol=tol)
        )


def test_has_expr_override_pass():
    stu = "x = [1, 2, 3]"
    sol = "x = [1, 2, 5]"
    s = setup_state(stu_code=stu, sol_code=sol)
    helper.passes(s.check_object("x").has_equal_value(expr_code="x[2]", override=3))


def test_has_expr_override_pass_2():
    stu = "x = [1, 2, 3]"
    sol = "x = [1, 2, 5]"
    s = setup_state(stu_code=stu, sol_code=sol)
    helper.passes(s.check_object("x").has_equal_value(override=[1, 2, 3]))
