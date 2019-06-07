import pytest
import tests.helper as helper

from pythonwhat.test_exercise import setup_state
from pythonwhat.sct_syntax import v2_check_functions

globals().update(v2_check_functions)


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("def test(): print(3)", False),
        ("def test(y): print(y)", False),
        ("def test(x): pass", False),
        ("def test(x): print(x + 2)", False),
        ("def test(x): print(x)", True),
    ],
)
def test_check_function_def_basic(stu, passes):
    s = setup_state(stu, "def test(x): print(x)")
    with helper.verify_sct(passes):
        s.check_function_def("test").multi(
            check_args(0).has_equal_part("name", msg="wrong"),
            check_body()
            .set_context(1)
            .check_function("print")
            .check_args(0)
            .has_equal_value(),
        )


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("def shout(x): pass", False),
        ("def shout(word): print(word + '!!')", True),
        ("def shout(x): print(x + '!!')", True),
    ],
)
def test_check_function_def_no_args(stu, passes):
    s = setup_state(stu, "def shout(word): print(word + '!!')")
    with helper.verify_sct(passes):
        s.check_function_def("shout").check_body().set_context(
            "test"
        ).has_equal_output()


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("def shout(word): pass", False),
        ("def shout(word):\n  bigword = word*2", False),
        ("def shout(word):\n  bigword = word+'!!'", True),
        ("def shout(word):\n  bigword = word+'!!'\n  return bigword", True),
    ],
)
def test_check_function_def_name(stu, passes):
    s = setup_state(stu, "def shout(word):\n  bigword = word + '!!'\n  return bigword")
    with helper.verify_sct(passes):
        s.check_function_def("shout").check_body().set_context("test").has_equal_value(
            name="bigword"
        )


# Old spec still supported? -------------------------------------------------


@pytest.mark.parametrize(
    "sct",
    [
        "Ex().check_function_def('shout').check_body().set_context('test').has_equal_output()",
        "test_function_definition('shout', body = lambda: test_expression_output(context_vals = ['help']))",
        "test_function_definition('shout', body = test_expression_output(context_vals = ['help']))",
    ],
)
def test_old_ways_of_calling(sct):
    code = "def shout(word): print(word + '!!')"
    res = helper.run({"DC_CODE": code, "DC_SOLUTION": code, "DC_SCT": sct})
    assert res["correct"]


@pytest.mark.parametrize(
    "sct",
    [
        """
Ex().check_function_def('my_fun').multi(
    check_args('*args').has_equal_part('name', msg='x'),
    check_args('**kwargs').has_equal_part('name', msg='x')
)
    """,
        "Ex().test_function_definition('my_fun')",
    ],
)
def test_old_ways_of_calling_starargs(sct):
    code = "def my_fun(*x, **y): pass"
    res = helper.run({"DC_CODE": code, "DC_SOLUTION": code, "DC_SCT": sct})
    assert res["correct"]


# Arguments, lengths, defaults -----------------------------------------------


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("def f(): pass", False),
        ("def f(c, b = 3): pass", False),
        ("def f(a = 2, b = 3): pass", False),
        ("def f(a): pass", False),
        ("def f(a, c): pass", False),
        ("def f(a, b): pass", False),
        ("def f(a, b = 4): pass", False),
        ("def f(a, b = 3): pass", True),
    ],
)
def test_check_function_def_args(stu, passes):
    s = setup_state(stu, "def f(a, b = 3): pass")
    with helper.verify_sct(passes):
        s.check_function_def("f").multi(
            check_args(0)
            .has_equal_part("name", msg="wrong")
            .has_equal_part("is_default", msg="wrong"),
            check_args(1)
            .has_equal_part("name", msg="wrong")
            .has_equal_part("is_default", msg="wrong")
            .has_equal_value(),
        )


@pytest.mark.parametrize(
    "sct",
    [
        "Ex().check_function_def('f').has_equal_part_len('args', unequal_msg='wrong')",
        "Ex().test_function_definition('f')",  # does arg len checking internally
    ],
)
@pytest.mark.parametrize(
    "stu, passes",
    [("def f(): pass", False), ("def f(a): pass", False), ("def f(a, b): pass", True)],
)
def test_check_function_equal_part_len(sct, stu, passes):
    res = helper.run(
        {"DC_CODE": stu, "DC_SOLUTION": "def f(a, b): pass", "DC_SCT": sct}
    )
    assert res["correct"] == passes


# Check call ------------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("def test(a, b): return 1", False),
        ("def test(a, b): return a + b", False),
        (
            """
def test(a, b):
    if a == 3:
        raise ValueError('wrong')
    print(a + b)
    return a + b
""",
            False,
        ),
        ("def test(a, b): print(int(a) + int(b)); return int(a) + int(b)", False),
        ("def test(a, b): print(a + b); return a + b", True),
    ],
)
def test_check_call(stu, passes):
    s = setup_state(stu, "def test(a, b): print(a + b); return a + b")
    with helper.verify_sct(passes):
        s.check_function_def("test").multi(
            check_call("f(1,2)").has_equal_value(),
            check_call("f(1,2)").has_equal_output(),
            check_call("f(3,1)").has_equal_value(),
            check_call("f(1, '2')").has_equal_error(),
        )


@pytest.mark.parametrize(
    "stu, passes", [("lambda a,b: 1", False), ("lambda a,b: a + b", True)]
)
def test_check_call_lambda(stu, passes):
    s = setup_state(stu, "lambda a, b: a + b")
    with helper.verify_sct(passes):
        s.check_lambda_function().multi(
            check_call("f(1,2)").has_equal_value(),
            check_call("f(1,2)").has_equal_output(),
        )


def test_check_call_error_types():
    s = setup_state(
        'def test(): raise NameError("boooo")', 'def test(): raise ValueError("boooo")'
    )
    s.check_function_def("test").check_call("f()").has_equal_error()


@pytest.mark.parametrize(
    "sct",
    [
        "Ex().test_function_definition('my_fun', results=[[1]])",
        "Ex().test_function_definition('my_fun', results=[(1,)])",
        "Ex().test_function_definition('my_fun', outputs=[[1]])",
        "Ex().test_function_definition('my_fun', outputs=[(1,)])",
        "Ex().test_function_definition('my_fun', errors=[['1']])",
        "Ex().test_function_definition('my_fun', errors=[('1',)])",
        "Ex().test_function_definition('my_fun', errors=['1'])",
    ],
)
def test_check_call_old_way_of_calling(sct):
    code = "def my_fun(a):\n  print(a + 2)\n  return a + 2"
    res = helper.run({"DC_CODE": code, "DC_SOLUTION": code, "DC_SCT": sct})
    assert res["correct"]


# Lambdas ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("lambda x: x", False),
        ("lambda a, b: a", False),
        ("lambda x = 1, b = 2: x", False),
        ("lambda x, b: x", False),
        ("lambda x, y = 1: x", False),
        ("lambda x, y = 2: x", False),
        ("lambda x, y = 2: print(x + y + 3)", False),
        ("lambda x, y = 2: print(x + y)", True),
        ("lambda x, y = 2: print(y + x)", True),
        ("lambda x, y = 2: print(3)", True),  # because set_context(1,2)
    ],
)
def test_check_lambda_full_ast_based(stu, passes):
    s = setup_state(stu, "lambda x, y=2: print(x + y)")
    with helper.verify_sct(passes):
        s.check_lambda_function(0).multi(
            has_equal_part_len("args", unequal_msg="wrong"),
            check_args(0)
            .has_equal_part("name", msg="wrong")
            .has_equal_part("is_default", msg="wrong"),
            check_args(1)
            .has_equal_part("name", msg="wrong")
            .has_equal_part("is_default", msg="wrong")
            .has_equal_value(),
            check_body().set_context(1, 2).has_equal_output(),
        )
