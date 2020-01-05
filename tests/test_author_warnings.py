import pytest
import ast
import tests.helper as helper

from pythonwhat.test_exercise import setup_state
from protowhat.failure import InstructorError
from inspect import signature, Signature, Parameter
from pythonwhat.checks.check_funcs import assert_ast

# Actually wrong usage that breaks --------------------------------------------


@pytest.mark.compiled
def test_converter_err():
    code = "import numpy as np; x = np.array([1, 2, 3])"
    data = {
        "DC_CODE": code,
        "DC_SOLUTION": code,
        "DC_SCT": """def convert(): return abc\nset_converter('numpy.ndarray', convert); test_object('x') """,
    }
    with pytest.raises(InstructorError):
        helper.run(data)


def test_check_syntax_double_getattr():
    s = setup_state()
    with pytest.raises(AttributeError, match=r"Expected a call of"):
        s.check_list_comp.check_body()


def test_context_vals_wrong_place_in_chain():
    code = "[(i,j) for i,j in enumerate(range(10))]"
    state = setup_state(code, code)
    with pytest.raises(
        InstructorError,
        match=r"`set_context\(\)` failed: context val names are missing, but you tried to set \['i', 'j'\]\.",
    ):
        state.check_list_comp(0).set_context(i=1, j=2).check_iter()


@pytest.fixture
def state():
    return setup_state("round(1)", "round(1)")


def test_check_function(state):
    with pytest.raises(
        InstructorError,
        match=r"`check_function\(\)` couldn't find a call of `roundddd\(\)` in the solution code. Make sure you get the mapping right!",
    ):
        state.check_function("roundddd")


def test_check_function_2(state):
    with pytest.raises(
        InstructorError,
        match=r"`check_function\(\)` couldn't find 2 calls of `round\(\)` in your solution code\.",
    ):
        state.check_function("round", 1)


def test_check_function_3(state):
    with pytest.raises(
        InstructorError,
        match=r"`check_function\(\)` couldn't match the first call of `round` to its signature:",
    ):
        sig = Signature([Parameter("wrong", Parameter.KEYWORD_ONLY)])
        state.check_function("round", 0, signature=sig)


def test_check_function_4(state):
    with pytest.raises(
        InstructorError,
        match=r"Check your call of `round\(\)`\. SCT fails on solution: Did you specify the second argument\?",
    ):
        state.check_function("round").check_args(1)


def test_check_function_5(state):
    with pytest.raises(
        InstructorError,
        match=r"Check your call of `round\(\)`. SCT fails on solution: You are zooming in on the first argument, but it is not an AST, so it can't be re-run\.",
    ):

        def round(*nums):
            pass

        state.check_function("round", 0, signature=signature(round)).check_args(
            0
        ).has_equal_value()


def test_check_object():
    s = setup_state()
    with pytest.raises(
        InstructorError,
        match=r"`check_object\(\)` couldn't find object `x` in the solution process\.",
    ):
        s.check_object("x")


def test_check_object_is_instance():
    s = setup_state("x = 1", "x = 1")
    with pytest.raises(
        InstructorError,
        match=r"`is_instance\(\)` noticed that `x` is not a `str` in the solution process\.",
    ):
        s.check_object("x").is_instance(str)


def test_check_object_keys():
    s = setup_state('x = {"a": 2}', 'x = {"a": 2}')
    with pytest.raises(
        InstructorError,
        match=r"`check_keys\(\)` couldn't find key `b` in object `x` in the solution process\.",
    ):
        s.check_object("x").check_keys("b")


def test_set_context():
    code = "x = { m:len(m) for m in ['a', 'b', 'c'] }"
    s = setup_state(code, code)
    with pytest.raises(
        InstructorError,
        match=r"In `set_context\(\)`, specify arguments either by position, either by name\.",
    ):
        s.check_dict_comp().check_key().set_context("a", m="a").has_equal_value()


def test_has_printout():
    s = setup_state()
    with pytest.raises(
        InstructorError,
        match=r"`has_printout\(1\)` couldn't find the second print call in your solution\.",
    ):
        s.has_printout(1)


def test_has_import():
    s = setup_state()
    with pytest.raises(
        InstructorError,
        match=r"`has_import\(\)` couldn't find an import of the package numpy in your solution code\.",
    ):
        s.has_import("numpy")


# Incorrect usage that wouldn't throw exceptions ------------------------------

from pythonwhat.sct_syntax import v2_check_functions


def test_has_printout_on_root():
    code = "print(1)"
    s = setup_state(code, code)
    has_printout = v2_check_functions["has_printout"]
    s.check_or(has_printout(0), has_printout(0))


def test_has_printout_not_on_root():
    code = "for i in range(3): print(i)"
    s = setup_state(code, code)
    with pytest.raises(
        InstructorError,
        match=r"`has_printout\(\)` should only be called focusing on a full script, following `Ex\(\)` or `run\(\)`\. If you want to check printouts done in e.g. a for loop, you have to use a `check_function\('print'\)` chain instead.",
    ):
        s.check_for_loop().check_body().has_printout(0)


def test_has_no_error_not_on_root():
    code = "for i in range(3): pass"
    s = setup_state(code, code)
    with pytest.raises(
        InstructorError,
        match=r"`has_no_error\(\)` should only be called focusing on a full script, following `Ex\(\)` or `run\(\)`\.",
    ):
        s.check_for_loop().check_body().has_no_error()


def test_check_object_on_root():
    code = "x = 1"
    check_object = v2_check_functions["check_object"]
    s = setup_state(code, code)
    s.check_or(check_object("x"), check_object("x"))


def test_check_object_not_on_root():
    code = "for i in range(3): x = 1"
    s = setup_state(code, code)
    with helper.set_v2_only_env(""):
        s.check_for_loop().check_body().check_object("x")


def test_check_object_not_on_root_v2():
    code = "for i in range(3): x = 1"
    s = setup_state(code, code)
    with helper.set_v2_only_env("1"):
        with pytest.raises(
            InstructorError,
            match=r"`check_object\(\)` should only be called focusing on a full script, following `Ex\(\)` or `run\(\)`\. If you want to check the value of an object in e.g. a for loop, use `has_equal_value\(name = 'my_obj'\)` instead.",
        ):
            s.check_for_loop().check_body().check_object("x")


def test_is_instance_not_on_check_object():
    code = "round(3)"
    s = setup_state(code, code)
    with pytest.raises(
        InstructorError,
        match=r"`is_instance\(\)` can only be called on `check_object\(\)`\.",
    ):
        s.check_function("round").check_args(0).is_instance(int)


def test_check_keys_not_on_check_object():
    code = "round(3)"
    s = setup_state(code, code)
    with pytest.raises(
        InstructorError,
        match=r"`is_instance\(\)` can only be called on `check_object\(\)` or `check_df\(\)`\.",
    ):
        s.check_function("round").check_args(0).check_keys("a")


def test_has_equal_ast_on_check_object():
    code = "x = 1"
    s = setup_state(code, code)
    s.check_object("x").has_equal_ast()


def test_has_equal_ast_on_check_object_v2():
    code = "x = 1"
    s = setup_state(code, code)
    with helper.set_v2_only_env("1"):
        with pytest.raises(
            InstructorError,
            match=r"`has_equal_ast\(\)` should not be called on `check_object\(\)`\.",
        ):
            s.check_object("x").has_equal_ast()


def test_has_equal_ast_on_check_function():
    code = "round(1)"
    s = setup_state(code, code)
    s.check_function("round").has_equal_ast()


def test_has_equal_ast_on_check_function_v2():
    code = "round(1)"
    s = setup_state(code, code)
    with helper.set_v2_only_env("1"):
        with pytest.raises(
            InstructorError,
            match=r"`has_equal_ast\(\)` should not be called on `check_function\(\)`\.",
        ):
            s.check_function("round").has_equal_ast()


def test_check_call_not_on_check_function_def():
    code = "def x(a): pass"
    s = setup_state(code, code)
    with pytest.raises(
        InstructorError,
        match=r"`check_call\(\)` can only be called on `check_function_def\(\)` or `check_lambda_function\(\)`\.",
    ):
        s.check_object("x").check_call("f(1)")


# Utility functions to make the above work ------------------------------------


@pytest.mark.parametrize(
    "element, no_error",
    [
        (ast.AST(), True),
        ([ast.AST()], True),
        ({"node": ast.AST()}, True),
        ({"node": [ast.AST()]}, True),
        (1, False),
        ([1, 2], False),
        ({"node": 1}, False),
        ({"node": [1, 2]}, False),
    ],
)
def test_assert_ast(element, no_error):
    s = setup_state()._state
    if no_error:
        assert_ast(s, element, {})
    else:
        with pytest.raises(InstructorError):
            assert_ast(s, element, {})
