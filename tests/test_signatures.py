from pythonwhat.test_exercise import setup_state
import pytest

# https://docs.python.org/3.x/library/functions.html
#
# Builtins that haven't been implemented/tested yet
# filter(), format(), frozenset(), iter(), map(), max(), min(),
# memoryview(), next(), property(), range(), slice(), super(), zip()


@pytest.mark.parametrize(
    "name, params, arguments",
    [
        ("abs", ["x"], "1"),
        ("all", ["iterable"], "[True, True]"),
        ("any", ["iterable"], "[True, False]"),
        ("ascii", ["obj"], "'test'"),
        ("bin", ["number"], "123456"),
        ("bool", ["x"], "1"),
        ("callable", ["obj"], "round"),
        ("chr", ["i"], "123"),
        ("classmethod", ["function"], "str"),
        ("complex", ["real", "imag"], "1,2"),
        ("dir", ["object"], "[1,2,3]"),
        ("divmod", ["x", "y"], "7,3"),
        ("enumerate", ["iterable", "start"], "[1,2,3],1"),
        ("float", ["x"], "123"),
        ("hash", ["obj"], "123"),
        ("hex", ["number"], "123"),
        ("id", ["obj"], "123"),
        ("int", ["x", "base"], "'1001',2"),
        ("isinstance", ["obj", "class_or_tuple"], "[1,2,3],list"),
        ("issubclass", ["cls", "class_or_tuple"], "list,str"),
        ("len", ["obj"], "[1,2,3]"),
        ("list", [], ""),
        ("list", ["iterable"], "[1,2,3,4]"),
        ("oct", ["number"], "12345"),
        ("ord", ["c"], "'a'"),
        ("pow", ["x", "y"], "3,3"),
        ("pow", ["x", "y", "z"], "3,3,5"),
        ("print", ["value"], "123"),
        ("repr", ["obj"], "[1,2,3]"),
        ("reversed", ["sequence"], "[1,2,3]"),
        ("round", ["number", "ndigits"], "2.123123, 2"),
        ("set", [], ""),
        ("set", ["iterable"], "[1,2,3,4]"),
        ("dir", ["object"], "[1,2,3]"),
        ("divmod", ["x", "y"], "7,3"),
        ("enumerate", ["iterable", "start"], "[1,2,3],1"),
        ("float", ["x"], "123"),
        ("sorted", ["iterable"], "[4,3,2,1]"),
        ("str", ["object"], "123"),
        ("sum", ["iterable", "start"], "[4,3,2,1],3"),
        ("tuple", [], ""),
        ("tuple", ["iterable"], "[1,2,3,4]"),
        ("type", ["object"], "[1,2,3,4]"),
    ],
)
def test_builtins(name, params, arguments):
    code = "%s(%s)" % (name, arguments)
    s = setup_state(code, code)
    fun_state = s.check_function(name)
    for param in params:
        fun_state.check_args(param).has_equal_value()


@pytest.mark.parametrize(
    "name, values, arguments",
    [
        ("delattr", "'a'", ["obj", "name"]),
        ("getattr", "'a'", ["object", "name"]),
        ("hasattr", "'a'", ["obj", "name"]),
        ("setattr", "'a', 4", ["obj", "name", "value"]),
    ],
)
def test_attrs(name, values, arguments):
    pec = """
class Test():
    def __init__(self, a):
        self.a = a
    def set_a(self, value):
        self.a = value
x = Test(123)
    """
    code = "%s(x, %s)" % (name, values)
    s = setup_state(code, code, pec=pec)
    fun_state = s.check_function(name)
    for arg in arguments:
        fun_state.check_args(arg).has_equal_ast()


@pytest.mark.parametrize(
    "name, values, arguments",
    [
        ("numpy.array", "[1, 2, 3, 4]", ["object"]),
        ("numpy.random.seed", "123", ["seed"]),
        ("numpy.random.rand", "3,3,3", ["d0", "d1", "d2"]),
        ("numpy.random.randint", "0, 5, size=(2,2)", ["low", "high", "size"]),
        (
            "numpy.random.choice",
            "a=5, size=3, replace=False, p=[0.1, 0, 0.3, 0.6, 0]",
            ["a", "size", "replace", "p"],
        ),
        ("numpy.random.poisson", "lam=(100., 500.), size=(100, 2)", ["lam", "size"]),
        (
            "numpy.random.normal",
            "loc = 0, scale=1.0, size=100",
            ["loc", "scale", "size"],
        ),
        ("numpy.random.binomial", "n=10, p=0.5, size=100", ["n", "p", "size"]),
        ("numpy.random.shuffle", "numpy.arange(10)", ["x"]),
        ("numpy.random.permutation", "numpy.arange(10)", ["x"]),
    ],
)
def test_numpy_builtins(name, values, arguments):
    code = "%s(%s)" % (name, values)
    s = setup_state(code, code, pec="import numpy")
    fun_state = s.check_function(name)
    for arg in arguments:
        fun_state.check_args(arg).has_equal_value()


def test_math_builtins():
    code = "m.radians(100)"
    s = setup_state(code, code, pec="import math as m")
    s.check_function("math.radians").check_args("x").has_equal_value()


@pytest.mark.parametrize("fun, argument", [("append", "object"), ("count", "value")])
def test_list_methods(fun, argument):
    code = "x.%s(2)" % fun
    s = setup_state(code, code, "x = [1, 2, 3]")
    s.check_function("x.%s" % fun).check_args(argument).has_equal_value()


# One-offs --------------------------------------------------------------------


def test_vars():
    pec = """
class Test():
    def __init__(self, a):
        self.a = a
    def set_a(self, value):
        self.a = value
x = Test(123)
    """
    code = "vars(x)"
    s = setup_state(code, code, pec=pec)
    s.check_function("vars").check_args("object").has_equal_ast()


def test_center():
    code = "x.center(10, 's')"
    s = setup_state(code, code, "x = 'test'")
    fun_state = s.check_function("x.center")
    fun_state.check_args("width").has_equal_value()
    fun_state.check_args("fillchar").has_equal_value()
