import unittest
from pythonwhat import utils_ast
import ast

def build_and_mark(s):
	res = ast.parse(s)
	utils_ast.mark_text_ranges(res, s + '\n')
	return(res)

class TestUtilsAstBinary(unittest.TestCase):

	def test_assignment(self):
		s = "x = 4 + 5 - 7 + 7 * (8) / 9"
		res = build_and_mark(s)

class TestUtilsAstList(unittest.TestCase):
	def test_tuple_1(self):
		s = "(12, 23)"
		res = build_and_mark(s)

	def test_tuple_2(self):
		s = "(12, )"
		res = build_and_mark(s)

	def test_list_1(self):
		s = "[1, 2, 'test', (1, 2)]"
		res = build_and_mark(s)

	def test_list_2(self):
		s = "[1,\n2,\n'test'\n,(1,)]"
		res = build_and_mark(s)

	def test_dict_1(self):
		s = "{'a': 1, 'b':2, 'c': (1, 2)}"
		res = build_and_mark(s)

	def test_dict_2(self):
		s = "{'a':1,\n'b':2,\n'c':(1,)}"
		res = build_and_mark(s)


class TestUtilsAstFunctionCalls(unittest.TestCase):
	def test_fun_call_1(self):
		s = "round(1.213, 2)"
		res = build_and_mark(s)

	def test_fun_call_2(self):
		s = "round(1.213, ndigits = 2)"
		res = build_and_mark(s)

	def test_fun_call_3(self):
		s = "round(abs(1.213), ndigits = 2)"
		res = build_and_mark(s)

	def test_fun_call_4(self):
		s = "round(abs((1.213)), ndigits = 2)"
		res = build_and_mark(s)

	def test_fun_call_5(self):
		s = "round(abs((1.213)), ndigits = abs(2))"
		res = build_and_mark(s)

	def test_fun_call_6(self):
		s = "import numpy as np; np.array([1, 2, 3])"
		res = build_and_mark(s)

	def test_fun_call_7(self):
		s = "import numpy as np; np.array([1, 2, 3])"
		res = build_and_mark(s)

	def test_fun_call_8(self):
		s = "print(file.read())"
		res = build_and_mark(s)

class TestUtilsAstFunctionControlFlow(unittest.TestCase):
	def test_if_else(self):
		s = "if True:\n  print('x')\nelif False:\n  print('y')\nelse:\n  print('z')"
		res = build_and_mark(s)

	def test_while(self):
		s = "while True:\n  print(1)"
		res = build_and_mark(s)

	def test_for(self):
		s = "for i in [1, 2, 3]:\n  print(i)"
		res = build_and_mark(s)

	def test_try_except(self):
		s = "try:\n  x = 4\nexcept:\n  print('test')"
		res = build_and_mark(s)

class TestUtilsAstImports(unittest.TestCase):
	def test_import(self):
		s = "from numpy import array as arr"
		res = build_and_mark(s)

class TestUtilsAstFunctionDefinition(unittest.TestCase):
	def test_fun_def_1(self):
		s = "def my_fun(a, b = 2):\n  return a + b"
		res = build_and_mark(s)

	def test_fun_def_2(self):
		s = "def my_fun(a, b = 2):\n  return a + abs(b)"
		res = build_and_mark(s)

	def test_fun_def_3(self):
		s = "def my_fun(a, b = 2):\n  return a + (abs(b))"
		res = build_and_mark(s)

class TestUtilsAstLambdas(unittest.TestCase):
	def test_lambda_1(self):
		s = "echo_word = lambda word, echo = 1: word * echo"
		res = build_and_mark(s)

	def test_lambda_2(self):
		s = "(lambda word, echo = 1: word * echo)('test', 3)"
		res = build_and_mark(s)

if __name__ == "__main__":
     unittest.main()
