import pytest
import tests.helper as helper
from inspect import getsource
from pythonwhat.test_exercise import setup_state
from protowhat.failure import TestFail as TF, InstructorError
from pythonwhat.sct_syntax import v2_check_functions

globals().update(v2_check_functions)

# Basics ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("my_fun(2, 2)", False),
        ("my_fun(2, b=2)", False),
        ("my_fun(a=2, b=2)", False),
        ("my_fun(1, 3)", False),
        ("my_fun(1, b=3)", False),
        ("my_fun(a=1, b=3)", False),
        ("my_fun(1, 2)", True),
        ("my_fun(1, b=2)", True),
        ("my_fun(a=1, b=2)", True),
    ],
)
@pytest.mark.parametrize("a_arg", ["a", 0])
@pytest.mark.parametrize("b_arg", ["b", 1])
def test_check_function_basic(stu, passes, a_arg, b_arg):
    s = setup_state(stu, "my_fun(1, 2)", pec="def my_fun(a, b): pass")
    with helper.verify_sct(passes):
        s.check_function("my_fun").multi(
            check_args(a_arg).has_equal_value(), check_args(b_arg).has_equal_value()
        )


def test_params_not_matched():
    res = helper.run(
        {
            "DC_PEC": "def my_fun(a, b): pass",
            "DC_CODE": "my_fun(x = 2)",
            "DC_SOLUTION": "my_fun(1, 2)",
            "DC_SCT": "Ex().check_function('my_fun')",
        }
    )
    assert not res["correct"]
    assert (
        res["message"]
        == "Have you specified the arguments for <code>my_fun()</code> using the right syntax?"
    )


# Different types of functions ------------------------------------------------


@pytest.mark.parametrize(
    "fun, code, arg",
    [
        ("my_fun", "def my_fun(a): pass\nmy_fun(1)", "a"),  # self-defined
        ("round", "round(1)", "number"),  # builtin
        (
            "pandas.DataFrame",
            "import pandas as pd\npd.DataFrame({'a': [1]})",
            "data",
        ),  # package
        (
            "numpy.array",
            "import numpy as np\nnp.array([1, 2, 3])",
            "object",
        ),  # builtin from package
    ],
)
def test_diff_function_types(fun, code, arg):
    s = setup_state(code, code)
    s.check_function(fun).check_args(arg).has_equal_value()


# Argument binding ------------------------------------------------------------


def test_bind_args():
    from pythonwhat.test_exercise import setup_state
    from inspect import signature
    from pythonwhat.checks.check_function import bind_args

    def my_fun(a, b, *args, **kwargs): pass
    pec = getsource(my_fun).strip()
    s = setup_state(pec=pec, stu_code="my_fun(1, 2, 3, 4, c = 5)")
    args = s._state.ast_dispatcher.find("function_calls", s._state.student_ast)[
        "my_fun"
    ][0]["args"]
    sig = signature(my_fun)
    bound_args = bind_args(sig, args)
    assert bound_args["a"]["node"].n == 1
    assert bound_args["b"]["node"].n == 2
    assert bound_args["args"][0]["node"].n == 3
    assert bound_args["args"][1]["node"].n == 4
    assert bound_args["kwargs"]["c"]["node"].n == 5


@pytest.mark.parametrize("argspec", [["args", 0], ["args", 1], ["kwargs", "c"]])
def test_args_kwargs_check_function_passing(argspec):
    code = "my_fun(1, 2, 3, 4, c = 5)"
    s = setup_state(
        pec="def my_fun(a, b, *args, **kwargs): pass", stu_code=code, sol_code=code
    )
    x = s.check_function("my_fun")
    helper.passes(x.check_args(argspec).has_equal_value())


@pytest.mark.parametrize(
    "argspec, msg",
    [
        (
            ["args", 0],
            "Did you specify the first argument passed as a variable length argument",
        ),
        (
            ["args", 1],
            "Did you specify the second argument passed as a variable length argument",
        ),
        (["kwargs", "c"], "Did you specify the argument `c`"),
    ],
)
def test_args_kwargs_check_function_failing_not_specified(argspec, msg):
    s = setup_state(
        pec="def my_fun(a, b, *args, **kwargs): pass",
        sol_code="my_fun(1, 2, 3, 4, c = 5)",
        stu_code="my_fun(1, 2)",
    )
    x = s.check_function("my_fun")
    with pytest.raises(TF, match=msg):
        x.check_args(argspec)


@pytest.mark.parametrize(
    "argspec, msg",
    [
        (
            ["args", 0],
            "Did you correctly specify the first argument passed as a variable length argument",
        ),
        (
            ["args", 1],
            "Did you correctly specify the second argument passed as a variable length argument",
        ),
        (["kwargs", "c"], "Did you correctly specify the argument `c`"),
    ],
)
def test_args_kwargs_check_function_failing_not_correct(argspec, msg):
    s = setup_state(
        pec="def my_fun(a, b, *args, **kwargs): pass",
        sol_code="my_fun(1, 2, 3, 4, c = 5)",
        stu_code="my_fun(1, 2, 4, 5, c = 6)",
    )
    x = s.check_function("my_fun")
    with pytest.raises(TF, match=msg):
        x.check_args(argspec).has_equal_value()


def test_check_function_with_has_equal_value():
    code = "import numpy as np\narr = np.array([1, 2, 3, 4, 5])\nnp.mean(arr)"
    s = setup_state(stu_code=code, sol_code=code)
    helper.passes(s.check_function("numpy.mean").has_equal_value())


def check_function_sig_false():
    code = "f(color = 'blue')"
    s = setup_state(pec="def f(*args, **kwargs): pass", sol_code=code, stu_code=code)
    helper.passes(
        s.check_function("f", 0, signature=False).check_args("color").has_equal_ast()
    )


def check_function_sig_false_override():
    s = setup_state(
        pec="def f(*args, **kwargs): pass",
        sol_code="f(color = 'blue')",
        stu_code="f(c = 'blue')",
    )
    helper.passes(
        s.override("f(c = 'blue')")
        .check_function("f", 0, signature=False)
        .check_args("c")
        .has_equal_ast()
    )


@pytest.mark.parametrize(
    "stu, passes", [("max([1, 2, 3, 4])", True), ("max([1, 2, 3, 400])", False)]
)
def test_sig_from_params(stu, passes):
    s = setup_state(stu, "max([1, 2, 3, 4])")
    with helper.verify_sct(passes):
        sig = sig_from_params(param("iterable", param.POSITIONAL_ONLY))
        s.check_function("max", signature=sig).check_args(0).has_equal_value()


# Multiple calls --------------------------------------------------------------


def check_function_multiple_times():
    from pythonwhat.local import setup_state

    s = setup_state(sol_code="print('test')", stu_code="print('test')")
    helper.passes(s.check_function("print"))
    helper.passes(s.check_function("print").check_args(0))
    helper.passes(s.check_function("print").check_args("value"))


# Methods ---------------------------------------------------------------------


# Manually create a signature for functions that need self passed
def test_method_1():
    code = "df.groupby('b').sum()"
    s = setup_state(
        sol_code=code,
        stu_code=code,
        pec="import pandas as pd; df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'x', 'y']})",
    )
    helper.passes(s.check_function("df.groupby").check_args(0).has_equal_value())
    helper.passes(s.check_function("df.groupby.sum", signature=False))

    import inspect
    from inspect import Parameter as param
    manual_sig = inspect.Signature([
        param("x", param.POSITIONAL_OR_KEYWORD, default=None),
        param("axis", param.POSITIONAL_OR_KEYWORD, default=None)
    ])
    helper.passes(
        s.check_function("df.groupby.sum", signature=manual_sig)
    )


def test_method_2():
    code = "print('a')"
    s = setup_state(
        sol_code=code,
        stu_code=code,
        pec="",
    )
    helper.passes(s.check_function("print", signature=False))

    from pythonwhat.signatures import sig_from_obj
    helper.passes(s.check_function("print", signature=sig_from_obj('print')))


from pythonwhat.signatures import sig_from_params, param

# Function parser -------------------------------------------------------------

from pythonwhat.parsing import FunctionParser
import ast


@pytest.mark.parametrize(
    "code",
    [
        "print(round(1.23))",
        "x = print(round(1.23))",
        "x = [round(1.23)]",
        'x = {"a": round(1.23)}',
        "x = 0; x += round(1.23)",
        "x = 0; x > round(1.23)",
        "not round(1.23)",
    ],
)
def test_function_parser(code):
    p = FunctionParser()
    p.visit(ast.parse(code))
    assert "round" in p.out


def test_check_function_parser_mappings_1():
    code = "import numpy as np\nnp.random.randint(1, 7)"
    s = setup_state(code, code)
    s.check_function("numpy.random.randint")


# Because the mappings are only found for the substate that is zoomed in on,
# The `import numpy as np` part is not found, because it's outside of the for loop.
# This should be fixed!!!
@pytest.mark.xfail
def test_check_function_parser_mappings_2():
    code = "import numpy as np\nfor x in range(0): np.random.randint(1, 7)"
    s = setup_state(code, code)
    s.check_for_loop().check_body().check_function("numpy.random.randint")


# Incorrect usage -------------------------------------------------------------


@pytest.mark.parametrize(
    "sct",
    [
        "Ex().check_function('round').check_args('ndigits').has_equal_value()",
        "Ex().check_correct(check_object('x').has_equal_value(), check_function('round').check_args('ndigits').has_equal_value())",
        "Ex().check_function('round', signature = False).check_args('ndigits').has_equal_value()",
        "Ex().check_correct(check_object('x').has_equal_value(), check_function('round', signature = False).check_args('ndigits').has_equal_value())",
        "Ex().check_correct(check_object('x').has_equal_value(), check_function('round', signature = sig_from_params()))",
    ],
)
@pytest.mark.parametrize("sol", ["x = 5", "x = round(5.23)"])
def test_check_function_weirdness(sct, sol):
    data = {"DC_CODE": "round(1.23, ndigits = 1)", "DC_SOLUTION": sol, "DC_SCT": sct}
    with pytest.raises(InstructorError):
        helper.run(data)


# Old implementation: test_function -------------------------------------------
# NOTE: These tests shows how it _currently_ works,
# but test_function can be improved!


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("my_fun(2, 2)", False),
        ("my_fun(2, b=2)", False),
        ("my_fun(a=2, b=2)", False),
        ("my_fun(1, 3)", False),
        ("my_fun(1, b=3)", False),
        ("my_fun(a=1, b=3)", False),
        ("my_fun(1, 2)", False),  # this failure is THE limitation of test_function!
        ("my_fun(1, b=2)", False),  # this failure is THE limitation of test_function!
        ("my_fun(a=1, b=2)", True),
    ],
)
def test_test_function_basic(stu, passes):
    s = setup_state(stu, "my_fun(a = 1, b = 2)", pec="def my_fun(a, b): pass")
    with helper.verify_sct(passes):
        s.test_function("my_fun")


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("my_fun(2, 2)", False),
        ("my_fun(2, b=2)", False),
        ("my_fun(a=2, b=2)", False),
        ("my_fun(1, 3)", True),
        ("my_fun(1, b=3)", True),
        ("my_fun(a=1, b=3)", True),
        ("my_fun(1, 2)", True),
        ("my_fun(1, b=2)", True),
        ("my_fun(a=1, b=2)", True),
    ],
)
def test_test_function_args(stu, passes):
    s = setup_state(stu, "my_fun(1, b = 2)", pec="def my_fun(a, b): pass")
    with helper.verify_sct(passes):
        s.test_function("my_fun", args=[0], keywords=[])


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("my_fun(2, 2)", False),
        ("my_fun(2, b=2)", True),
        ("my_fun(a=2, b=2)", True),
        ("my_fun(1, 3)", False),
        ("my_fun(1, b=3)", False),
        ("my_fun(a=1, b=3)", False),
        ("my_fun(1, 2)", False),
        ("my_fun(1, b=2)", True),
        ("my_fun(a=1, b=2)", True),
    ],
)
def test_test_function_keywords(stu, passes):
    s = setup_state(stu, "my_fun(1, b = 2)", pec="def my_fun(a, b): pass")
    with helper.verify_sct(passes):
        s.test_function("my_fun", args=[], keywords=["b"])


@pytest.mark.parametrize(
    "stu, do_eval, passes",
    [
        ("round(1)", True, True),
        ("round(a)", True, True),
        ("round(b)", True, False),
        ("round(b - 1)", True, True),
        ("round(1)", False, False),
        ("round(a)", False, True),
        ("round(b)", False, False),
        ("round(b - 1)", False, False),
        ("a=123; round(a)", False, True),
    ],
)
def test_test_function_do_eval(stu, do_eval, passes):
    s = setup_state(stu, "round(a)", pec="a,b = 1,2")
    with helper.verify_sct(passes):
        s.test_function("round", do_eval=do_eval)


@pytest.mark.parametrize(
    "stu, passes", [("print(1)", True), ("print('1')", True), ("print(5)", False)]
)
def test_test_function_print(stu, passes):
    s = setup_state(stu, "print(1)")
    with helper.verify_sct(passes):
        s.test_function("print")


# Old implementation: test_function_v2 ----------------------------------------


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("my_fun(2, 2)", False),
        ("my_fun(2, b=2)", False),
        ("my_fun(a=2, b=2)", False),
        ("my_fun(1, 3)", False),
        ("my_fun(1, b=3)", False),
        ("my_fun(a=1, b=3)", False),
        ("my_fun(1, 2)", True),  # test_function_v2 is better
        ("my_fun(1, b=2)", True),  # test_function_v2 is better
        ("my_fun(a=1, b=2)", True),
    ],
)
def test_test_function_v2_basic(stu, passes):
    s = setup_state(stu, "my_fun(a = 1, b = 2)", pec="def my_fun(a, b): pass")
    with helper.verify_sct(passes):
        s.test_function_v2("my_fun", params=["a", "b"])


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("my_fun(2, 2)", False),
        ("my_fun(2, b=2)", False),
        ("my_fun(a=2, b=2)", False),
        ("my_fun(1, 3)", True),
        ("my_fun(1, b=3)", True),
        ("my_fun(a=1, b=3)", True),
        ("my_fun(1, 2)", True),
        ("my_fun(1, b=2)", True),
        ("my_fun(a=1, b=2)", True),
    ],
)
def test_test_function_v2_params(stu, passes):
    s = setup_state(stu, "my_fun(1, b = 2)", pec="def my_fun(a, b): pass")
    with helper.verify_sct(passes):
        s.test_function_v2("my_fun", params=["a"])


@pytest.mark.parametrize(
    "stu, do_eval, passes",
    [
        ("round(1)", True, True),
        ("round(a)", True, True),
        ("round(b)", True, False),
        ("round(b - 1)", True, True),
        ("round(1)", False, False),
        ("round(a)", False, True),
        ("round(b)", False, False),
        ("round(b - 1)", False, False),
        ("a=123; round(a)", False, True),
    ],
)
def test_test_function_v2_do_eval(stu, do_eval, passes):
    s = setup_state(stu, "round(a)", pec="a,b = 1,2")
    with helper.verify_sct(passes):
        s.test_function_v2("round", params=["number"], do_eval=[do_eval])


@pytest.mark.parametrize(
    "stu, passes", [("print(1)", True), ("print('1')", True), ("print(5)", False)]
)
def test_test_function_v2_print(stu, passes):
    s = setup_state(stu, "print(1)")
    with helper.verify_sct(passes):
        s.test_function_v2("print", params=["value"])


@pytest.mark.parametrize(
    "sct",
    [
        "s.test_function_v2('round', params='number')",
        "s.test_function_v2('round', params=[], do_eval=[True])",
        "s.test_function_v2('round', params=[], params_not_specified_msg=['test'])",
        "s.test_function_v2('round', params=[], incorrect_msg=['test'])",
    ],
)
def test_test_function_v2_incorrect_usage(sct):
    s = setup_state("", "")
    with pytest.raises(InstructorError):
        eval(sct)


def test_test_function_v2_no_sig():
    s = setup_state("np.arange(10)", "np.arange(10)", pec="import numpy as np")
    # test_function_v2 sets signature=False if no params
    s.test_function_v2("numpy.arange")
    # check_function fails unless explicity setting signature=Fa
    s.check_function("numpy.arange", signature=False)
    with pytest.raises(InstructorError):
        s.check_function("numpy.arange")


def test_function_call_in_return():
    code = "def my_func(a): return my_func_in_return(b)"
    sct = "Ex().check_function_def('my_func').check_body().check_function('my_func_in_return', signature=False)"
    res = helper.run({"DC_CODE": code, "DC_SOLUTION": code, "DC_SCT": sct})
    assert res["correct"]


@pytest.mark.parametrize(
    "code",
    [
        "0 < len([])",
        "len([]) < 3",
        "0 < len([]) < 3",
    ],
)
def test_function_call_in_comparison(code):
    sct = "Ex().check_function('len')"
    res = helper.run({"DC_CODE": code, "DC_SOLUTION": code, "DC_SCT": sct})
    assert res["correct"]
