import unittest
import helper
import pytest

class TestFunctionBase(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
# pec comes here
            ''',
            "DC_CODE": '''
print(5 / 8)
print(7 + 10)
            ''',
            "DC_SOLUTION": '''
print(5 / 8)
print(7 + 10)
'''
        }

    def test_Pass(self):
        self.data["DC_SCT"] = '''
msg = "Don't remove the first statement. It is an example which is coded for you!"
test_function("print", 1)
test_function("print", 2)

success_msg("Great!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass_spec2(self):
        self.data['DC_SCT'] = """
Ex().check_function('print', 0).check_args(0).has_equal_ast()
"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestBlacklisting(unittest.TestCase):

    def test_bookkeeping(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
round(1.23456, ndigits = 1)
            ''',
            "DC_CODE": '''
round(1.23456, ndigits = 1)
            ''',
            "DC_SCT": '''
test_function('round', index = 1) # all in one
test_function('round', index = 1) # same call, should be fine.
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_bookkeeping2(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
round(1.23456, ndigits = 1)
round(1.65432, ndigits = 3)
            ''',
            "DC_CODE": '''
round(1.23456, ndigits = 1)
round(1.65432, ndigits = 3)
            ''',
            "DC_SCT": '''
test_function('round', index = 1) # all in one
test_function('round', args = [0], index = 2) # separate first
test_function('round', keywords = ['ndigits'], index = 2) # separate second
test_function('round', index = 2) # all-in-one
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_bookkeeping3(self):
        self.data = {
        "DC_PEC": '',
        "DC_SOLUTION": '''
round(1.23456, ndigits = 1)
round(1.65432, ndigits = 3)
        ''',
        "DC_CODE": '''
round(1.23456, ndigits = 1)
round(1.65432, ndigits = 4)
        ''',
        "DC_SCT": '''
test_function('round', index = 1) # all in one
test_function('round', args = [0], index = 2) # separate first
test_function('round', keywords = ['ndigits'], index = 2) # separate second
        '''
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])


class TestMessaging(unittest.TestCase):
    def setUp(self):
        self.data = {
             "DC_PEC": '',
             "DC_CODE": '''
import pandas as pd
x = pd.DataFrame({"a":[1, 2, 3]})
print(x)
# no data_range call
# no type(y) call
z = pd.Series([1, 2, 3])
len(z)
print(z)
            ''',
            "DC_SOLUTION": '''
import pandas as pad
x = pad.DataFrame({"a":[1, 2, 3]}) # correct
print(x) # correct
y = pad.date_range('1/1/2000', periods=8)
type(y)
z = pad.Series([1, 2, 4]) # incorrect
len(z) # incorrect
print(z) # incorrect
            '''
        }

    def test_auto(self):
        self.data["DC_SCT"] = '''
test_function("pandas.DataFrame")
test_function("print")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

        self.data["DC_SCT"] = 'test_function("pandas.date_range")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

        self.data["DC_SCT"] = 'test_function("type")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

        self.data["DC_SCT"] = 'test_function("pandas.Series")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

        self.data["DC_SCT"] = 'test_function("len")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

        self.data["DC_SCT"] = 'test_function("print", index = 1); test_function("print", index = 2)'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])


    def test_custom(self):
        self.data["DC_SCT"] = '''
test_function("pandas.DataFrame")
test_function("print")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

        self.data["DC_SCT"] = 'test_function("pandas.date_range", not_called_msg = "stupid")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "stupid")

        self.data["DC_SCT"] = 'test_function("type", not_called_msg = "stupid")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "stupid")

        self.data["DC_SCT"] = 'test_function("pandas.Series", incorrect_msg = "stupid")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("stupid", sct_payload['message'])

        self.data["DC_SCT"] = 'test_function("len", incorrect_msg = "stupid")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("stupid", sct_payload['message'])

class TestLineNumbers(unittest.TestCase):
    def test_line_numbers1(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(1.23456, ndigits = 1)",
                     "DC_CODE": "round(1.34567, ndigits = 1)",
                     "DC_SCT": "test_function('round', index = 1)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 7, 13)

    def test_line_numbers(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(1.23456, ndigits = 1)",
                     "DC_CODE": "round(1.23456, ndigits = 3)",
                     "DC_SCT": "test_function('round', index = 1)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 16, 26)


class TestFunctionNested(unittest.TestCase):
    def test_nested_arg1(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "print(type([1, 2, 3]))",
                     "DC_CODE": "print(type([1, 2, 3]))",
                     "DC_SCT": "test_function('type')"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_nested_arg2(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "print(type([1, 2, 3]))",
                     "DC_CODE": "print(type([1, 2, 4]))",
                     "DC_SCT": "test_function('type')"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 12, 20)

    def test_nested_keyw1(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(1.1234, ndigits = max([1, 2, 3]))",
                     "DC_CODE": "round(1.1234, ndigits = max([1, 2, 3]))",
                     "DC_SCT": "test_function('max')"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_nested_keyw2(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(1.1234, ndigits = max([1, 2, 3]))",
                     "DC_CODE": "round(1.1234, ndigits = max([1, 2]))",
                     "DC_SCT": "test_function('max')"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 29, 34)

class TestFunctionDoEval(unittest.TestCase):
    def test_do_eval_true_pass(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(2.1234, ndigits = 4)",
                     "DC_CODE": "round(2.1234, ndigits = 4)",
                     "DC_SCT": "test_function('round', do_eval = True)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_true_fail(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(2.1234, ndigits = 4)",
                     "DC_CODE": "round(2.123456, ndigits = 4)",
                     "DC_SCT": "test_function('round', do_eval = True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_do_eval_false_pass(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "x = 2.12309123; round(x, ndigits = 4)",
                     "DC_CODE": "x = 2.123450; round(x, ndigits = 4)",
                     "DC_SCT": "test_function('round', do_eval = False)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_false_fail(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "y = 2.12309123; round(y, ndigits = 4)",
                     "DC_CODE": "x = 2.123450; round(x, ndigits = 4)",
                     "DC_SCT": "test_function('round', do_eval = False)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_do_eval_none_pass(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, ndigits = 2)",
             "DC_CODE": "round(123.123, ndigits = 2)",
             "DC_SCT": "test_function('round', do_eval = None)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_none_fail1(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, ndigits = 2)",
             "DC_CODE": "round(123.123)",
             "DC_SCT": "test_function('round', do_eval = None)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 14)

    def test_do_eval_none_pass2(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123)", # args = [0]
             "DC_CODE": "round(number = 123.123)", # student args is len 0
             "DC_SCT": "test_function('round', do_eval = None)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_none_fail3(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, 2)", # args = [0, 1]
             "DC_CODE": "round(123.123)", # student_args is len 1
             "DC_SCT": "test_function('round', do_eval = None)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 14)

class TestCheckFunction(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_CODE": "np.array([1,2,3])",
            "DC_SOLUTION": "np.array([1,2,3])",
            "DC_SCT": "Ex().check_function('numpy.array', 0)"
            }

    def run_append(self, sct):
        self.data["DC_SCT"] += sct
        return helper.run(self.data)

    def run_pass(self, sct):
        sct_payload = self.run_append(sct)
        self.assertTrue(sct_payload['correct'])
        return sct_payload

    def run_fail(self, sct):
        self.assertFalse(self.run_append(sct)['correct'])

    def test_pass_np_call_exists(self):
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_test_student_typed(self):
        self.run_pass(".test_student_typed(r'np\.array\(\[1,2,3\]\)')")

    def test_fail_test_student_typed(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".test_student_typed(r'np\.array\(\[1,2,3\]\)')")

    def test_pass_func_has_equal_ast(self):
        self.run_pass(".has_equal_ast()")

    def test_fail_func_has_equal_ast(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".has_equal_ast()")

    def test_pass_check_args_pos_0(self):
        self.run_pass(".check_args(0)")

    def test_fail_check_args_pos_0(self):
        self.data["DC_CODE"] = "np.array()"
        self.run_fail(".check_args(0)")

    def test_pass_pos_0_test_student_typed(self):
        self.run_pass(".check_args(0).test_student_typed(r'\[1,2,3\]')")

    def test_fail_pos_0_test_student_typed(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".check_args(0).test_student_typed(r'\[1,2,3\]')")

    def test_pass_pos_0_has_equal_ast(self):
        self.run_pass(".check_args(0).has_equal_ast()")

    def test_fail_pos_0_has_equal_ast(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".check_args(0).has_equal_ast()")

    def test_pass_pos_0_has_equal_value(self):
        self.run_pass(".check_args(0).has_equal_value()")

    def test_fail_pos_0_has_equal_value(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".check_args(0).has_equal_value()")

    def test_pass_pos_0_inline_if_body(self):
        self.data["DC_CODE"] = "np.array([1,2,3] if True else [1])"
        self.data["DC_SOLUTION"] = "np.array([1,2,3] if False else [1])"
        self.run_pass(".check_args(0).check_if_exp(0).check_body().has_equal_ast()")

    def test_fail_pos_0_inline_if_body(self):
        self.data["DC_CODE"] = "np.array([1,2,3] if True else [1])"
        self.data["DC_SOLUTION"] = "np.array([1,2] if False else [1])"
        self.run_fail(".check_args(0).check_if_exp(0).check_body().has_equal_ast()")

    def test_test_function_kwargs(self):
        self.data["DC_SCT"] = "test_function('np.array', copy = False)"

    def test_test_function2_kwargs(self):
        self.data["DC_SCT"] = "test_function2('np.array', params = ['object'], copy = False)"


class TestFunctionComplexArgs(unittest.TestCase):
    def setUp(self):
        self.data = {
                "DC_SOLUTION": """
def sum2(arr): return sum(arr)

def apply(f, arr): return f(arr)

apply(sum2, [1,2,3])
""",
                "DC_SCT": """
test_function('apply')
"""
                }
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]

    def test_function_with_funcarg_fails(self):
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_pass_with_no_eval(self):
        self.data["DC_SCT"] = """test_function_v2('apply', params=['f', 'arr'], do_eval=[False, True])"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail_undillable_args(self):
        self.data = {
                "DC_PEC": """
import pickle; from io import BytesIO

file = BytesIO(pickle.dumps('abc'))
        """,
                "DC_SOLUTION": "d = pickle.load(file); print(d)",
                "DC_CODE": "print(file)",
                "DC_SCT": """test_function("print", index=1)"""
                }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

@pytest.mark.parametrize('stu, correct', [
    ('round(1)', False),
    ('round(1)\nround(2)', False),
    ('round(1)\nround(2)\nround(3)', True),
    ('round(3)\nround(2)\nround(3)', False),
    ('round(1)\round(1234)\nround(3)', False),
    ('round(1)\nround(2)\nround(4)', False)
])
def test_multiple_calls(stu, correct):
    data = {
        'DC_SOLUTION': 'round(1)\nround(2)\nround(3)',
        'DC_CODE': stu,
    }
    data['DC_SCT'] = """
test_function("round", index = 1)
test_function("round", index = 2)
test_function("round", index = 3)
"""
    payload = helper.run(data)
    assert payload['correct'] == correct
    data['DC_SCT'] = """
test_function_v2("round", index = 1)
test_function_v2("round", index = 2)
test_function_v2("round", index = 3)
"""
    payload = helper.run(data)

def test_has_output_fallback():
    code = "a = 3\nprint(a)\na = 4"
    data = { "DC_CODE": code, "DC_SOLUTION": code, "DC_SCT": "test_function('print')" }
    payload = helper.run(data)
    assert payload['correct']

if __name__ == "__main__":
    unittest.main()
