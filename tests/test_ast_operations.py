import pytest
from pythonwhat.State import Dispatcher


@pytest.mark.parametrize(
    "script",
    [
        "# encoding: target\nx=4",
        "x = 4 + 5 - 7 + 7 * (8) / 9",
        "(12, 23)",
        "(12, )",
        "[1, 2, 'test', (1, 2)]",
        "[1,\n2,\n'test'\n,(1,)]",
        "{'a': 1, 'b':2, 'c': (1, 2)}",
        "{'a':1,\n'b':2,\n'c':(1,)}",
        "round(1.213, 2)",
        "round(1.213, ndigits = 2)",
        "round(abs(1.213), ndigits = 2)",
        "round(abs((1.213)), ndigits = 2)",
        "round(abs((1.213)), ndigits = abs(2))",
        "import numpy as np; np.array([1, 2, 3])",
        "import numpy as np; np.array([1, 2, 3])",
        "print(file.read())",
        "if True:\n  print('x')\nelif False:\n  print('y')\nelse:\n  print('z')",
        "while True:\n  print(1)",
        "for i in [1, 2, 3]:\n  print(i)",
        "try:\n  x = 4\nexcept:\n  print('test')",
        "from numpy import array as arr",
        "def my_fun(a, b = 2):\n  return a + b",
        "def my_fun(a, b = 2):\n  return a + abs(b)",
        "def my_fun(a, b = 2):\n  return a + (abs(b))",
        "echo_word = lambda word, echo = 1: word * echo",
        "(lambda word, echo = 1: word * echo)('test', 3)",
    ],
)
def test_parses_without_error(script):
    Dispatcher().parse(script)
