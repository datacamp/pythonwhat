import pytest
from pythonwhat.State import State

def parsesWithoutError(s):
    try:
        State.parse_internal(s)
    except:
        pytest.fail("Parsing failed")

def test_encoding():
    parsesWithoutError("# encoding: target\nx=4")

def test_assignment():
    s = "x = 4 + 5 - 7 + 7 * (8) / 9"
    parsesWithoutError(s)

def test_tuple_1():
    s = "(12, 23)"
    parsesWithoutError(s)

def test_tuple_2():
    s = "(12, )"
    parsesWithoutError(s)

def test_list_1():
    s = "[1, 2, 'test', (1, 2)]"
    parsesWithoutError(s)

def test_list_2():
    s = "[1,\n2,\n'test'\n,(1,)]"
    parsesWithoutError(s)

def test_dict_1():
    s = "{'a': 1, 'b':2, 'c': (1, 2)}"
    parsesWithoutError(s)

def test_dict_2():
    s = "{'a':1,\n'b':2,\n'c':(1,)}"
    parsesWithoutError(s)

def test_fun_call_1():
    s = "round(1.213, 2)"
    parsesWithoutError(s)

def test_fun_call_2():
    s = "round(1.213, ndigits = 2)"
    parsesWithoutError(s)

def test_fun_call_3():
    s = "round(abs(1.213), ndigits = 2)"
    parsesWithoutError(s)

def test_fun_call_4():
    s = "round(abs((1.213)), ndigits = 2)"
    parsesWithoutError(s)

def test_fun_call_5():
    s = "round(abs((1.213)), ndigits = abs(2))"
    parsesWithoutError(s)

def test_fun_call_6():
    s = "import numpy as np; np.array([1, 2, 3])"
    parsesWithoutError(s)

def test_fun_call_7():
    s = "import numpy as np; np.array([1, 2, 3])"
    parsesWithoutError(s)

def test_fun_call_8():
    s = "print(file.read())"
    parsesWithoutError(s)
def test_if_else():
    s = "if True:\n  print('x')\nelif False:\n  print('y')\nelse:\n  print('z')"
    parsesWithoutError(s)

def test_while():
    s = "while True:\n  print(1)"
    parsesWithoutError(s)

def test_for():
    s = "for i in [1, 2, 3]:\n  print(i)"
    parsesWithoutError(s)

def test_try_except():
    s = "try:\n  x = 4\nexcept:\n  print('test')"
    parsesWithoutError(s)

def test_import():
    s = "from numpy import array as arr"
    parsesWithoutError(s)

def test_fun_def_1():
    s = "def my_fun(a, b = 2):\n  return a + b"
    parsesWithoutError(s)

def test_fun_def_2():
    s = "def my_fun(a, b = 2):\n  return a + abs(b)"
    parsesWithoutError(s)

def test_fun_def_3():
    s = "def my_fun(a, b = 2):\n  return a + (abs(b))"
    parsesWithoutError(s)
def test_lambda_1():
    s = "echo_word = lambda word, echo = 1: word * echo"
    parsesWithoutError(s)

def test_lambda_2():
    s = "(lambda word, echo = 1: word * echo)('test', 3)"
    parsesWithoutError(s)

