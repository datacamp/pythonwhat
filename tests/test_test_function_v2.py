import unittest
import helper
import pytest

class TestFunctionBase(unittest.TestCase):

    def test_fun_pass(self):
        self.data = {
            "DC_PEC": "def my_fun(a):\n    pass",
            "DC_SOLUTION": "my_fun(1)",
            "DC_CODE": "my_fun(1)",
            "DC_SCT": "test_function_v2('my_fun', params = ['a'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fun_fail(self):
        self.data = {
            "DC_PEC": "def my_fun(a):\n    pass",
            "DC_SOLUTION": "my_fun(2)",
            "DC_CODE": "my_fun(1)",
            "DC_SCT": "test_function_v2('my_fun', params = ['a'])"
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_builtin_pass(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "round(1)",
            "DC_CODE": "round(1)",
            "DC_SCT": "test_function_v2('round', params = ['number'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_builtin_fail(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "round(1)",
            "DC_CODE": "round(2)",
            "DC_SCT": "test_function_v2('round', params = ['number'])"
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_custom_builtin_pass(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "max([1, 2, 3, 4])",
            "DC_CODE": "max([1, 2, 3, 4])",
            "DC_SCT": '''
sig = sig_from_params(param('iterable', param.POSITIONAL_ONLY))
test_function_v2('max', params = ['iterable'], signature = sig)
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_custom_builtin_fail(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "max([1, 2, 3, 4])",
            "DC_CODE": "max([1, 2, 3, 412])",
            "DC_SCT": '''
sig = sig_from_params(param('iterable', param.POSITIONAL_ONLY))
test_function_v2('max', params = ['iterable'], signature = sig)
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_package_fun_pass(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "df = pd.DataFrame({'a': [1, 2, 3]})",
            "DC_CODE": "df = pd.DataFrame({'a': [1, 2, 3]})",
            "DC_SCT": "test_function_v2('pandas.DataFrame', params = ['data'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_package_fun_fail(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "df = pd.DataFrame({'a': [1, 2, 3]})",
            "DC_CODE": "df = pd.DataFrame({'a': [1, 2, 312]})",
            "DC_SCT": "test_function_v2('pandas.DataFrame', params = ['data'])"
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_package_builtin_pass(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "arr = np.array([1, 2, 3])",
            "DC_CODE": "arr = np.array([1, 2, 3])",
            "DC_SCT": "test_function_v2('numpy.array', params = ['object'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_package_builtin_fail(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "arr = np.array([1, 2, 3])",
            "DC_CODE": "arr = np.array([1, 2, 123])",
            "DC_SCT": "test_function_v2('numpy.array', params = ['object'])"
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_custom_package_builtin_pass(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "com = np.complex(2, 4)",
            "DC_CODE": "com = np.complex(2, 4)",
            "DC_SCT": '''
sig = sig_from_params(param('real', param.POSITIONAL_OR_KEYWORD), param('imag', param.POSITIONAL_OR_KEYWORD, default=0))
test_function_v2('numpy.complex', params = ['real', 'imag'], signature=sig)
            '''}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_custom_package_builtin_fail(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "com = np.complex(2, 4)",
            "DC_CODE": "com = np.complex(2, 5)",
            "DC_SCT": '''
sig = sig_from_params(param('real', param.POSITIONAL_OR_KEYWORD), param('imag', param.POSITIONAL_OR_KEYWORD, default=0))
test_function_v2('numpy.complex', params = ['real', 'imag'], signature=sig)
            '''}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_method_pass(self):
        self.data = {
            "DC_PEC": '''
class Test():
    def __init__(self, a):
        self.a = a

    def set_a(self, value):
        self.a = value
x = Test(123)
            ''',
            "DC_SOLUTION": "x.set_a(4)",
            "DC_CODE": "x.set_a(4)",
            "DC_SCT": "test_function_v2('x.set_a', params = ['value'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_method_fail(self):
        self.data = {
            "DC_PEC": '''
class Test():
    def __init__(self, a):
        self.a = a

    def set_a(self, value):
        self.a = value
x = Test(123)
            ''',
            "DC_SOLUTION": "x.set_a(4)",
            "DC_CODE": "x.set_a(4123)",
            "DC_SCT": "test_function_v2('x.set_a', params = ['value'])"
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_method_builtin_pass(self):
        self.data = {
            "DC_PEC": "arr = [1, 2, 3, 4]",
            "DC_SOLUTION": "arr.append(5)",
            "DC_CODE": "arr.append(5)",
            "DC_SCT": "test_function_v2('arr.append', params = ['object'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_method_builtin_fail(self):
        self.data = {
            "DC_PEC": "arr = [1, 2, 3, 4]",
            "DC_SOLUTION": "arr.append(5)",
            "DC_CODE": "arr.append(5123)",
            "DC_SCT": "test_function_v2('arr.append', params = ['object'])"
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_custom_method_builtin_pass(self):
        self.data = {
            "DC_PEC": "arr = [1, 2, 3, 4]",
            "DC_SOLUTION": "res = arr.count(2)",
            "DC_CODE": "res = arr.count(2)",
            "DC_SCT": '''
sig = sig_from_params(param('value', param.POSITIONAL_ONLY))
test_function_v2('arr.count', params = ['value'], signature=sig)
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_custom_method_builtin_fail(self):
        self.data = {
            "DC_PEC": "arr = [1, 2, 3, 4]",
            "DC_SOLUTION": "res = arr.count(2)",
            "DC_CODE": "res = arr.count(2123)",
            "DC_SCT": '''
sig = sig_from_params(param('value', param.POSITIONAL_ONLY))
test_function_v2('arr.count', params = ['value'], signature=sig)
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_chained_method_builtin_pass(self):
        self.data = {
            "DC_PEC": "x = 'test'",
            "DC_SOLUTION": "x.upper().center(8)",
            "DC_CODE": "x.upper().center(8)",
            "DC_SCT": "test_function_v2('x.upper.center', params=['width'], signature='str.center')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_chained_method_builtin_fail(self):
        self.data = {
            "DC_PEC": "x = 'test'",
            "DC_SOLUTION": "x.upper().center(8)",
            "DC_CODE": "x.upper().center(7)",
            "DC_SCT": "test_function_v2('x.upper.center', params=['width'], signature='str.center')"
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_chained_method_builtin_v2_pass(self):
        self.data = {
            "DC_PEC": '''
class Test():
    def __init__(self, a):
        self.a = a

    def set_a(self, value):
        self.a = value
        return(self)
x = Test(123)
            ''',
            "DC_SOLUTION": "x.set_a(843).set_a(102)",
            "DC_CODE": "x.set_a(843).set_a(102)",
            "DC_SCT": '''
sig = sig_from_obj('x.set_a')
test_function_v2('x.set_a.set_a', params = ['value'], signature=sig)
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_chained_method_builtin_v2_fail(self):
        self.data = {
            "DC_PEC": '''
class Test():
    def __init__(self, a):
        self.a = a

    def set_a(self, value):
        self.a = value
        return(self)
x = Test(123)
            ''',
            "DC_SOLUTION": "x.set_a(843).set_a(102)",
            "DC_CODE": "x.set_a(843).set_a(103)",
            "DC_SCT": '''
sig = sig_from_obj('x.set_a')
test_function_v2('x.set_a.set_a', params = ['value'], signature=sig)
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

class TestArgsKeywords(unittest.TestCase):

    def test_fun1(self):
        self.data = {
            "DC_SOLUTION": "round(2, 3)",
            "DC_CODE": "round(2, 3)",
            "DC_SCT": 'test_function_v2("round", params=["number", "ndigits"])'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fun2(self):
        self.data = {
            "DC_SOLUTION": "round(2, 3)",
            "DC_CODE": "round(2, ndigits=3)",
            "DC_SCT": 'test_function_v2("round", params=["number", "ndigits"])'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fun3(self):
        self.data = {
            "DC_SOLUTION": "round(2, ndigits=3)",
            "DC_CODE": "round(2, ndigits=3)",
            "DC_SCT": 'test_function_v2("round", params=["number", "ndigits"])'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fun4(self):
        self.data = {
            "DC_SOLUTION": "round(2, ndigits=3)",
            "DC_CODE": "round(2, 3)",
            "DC_SCT": 'test_function_v2("round", params=["number", "ndigits"])'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_class0(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "import pandas as pad; import numpy as nump; pad.DataFrame(nump.zeros((5,2)), columns = ['a', 'b'])",
            "DC_CODE": "import pandas as pd; import numpy as np; pd.DataFrame(np.zeros((5,2)), columns = ['a', 'b'])",
            "DC_SCT": "test_function_v2('pandas.DataFrame', params = ['data', 'columns'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_class1(self):
        self.data = {
            "DC_PEC": "import pandas as pd; import numpy as np",
            "DC_SOLUTION": "pd.DataFrame(np.zeros((5,2)), columns = ['a', 'b'])",
            "DC_CODE": "pd.DataFrame(np.zeros((5,2)), columns = ['a', 'b'])",
            "DC_SCT": "test_function_v2('pandas.DataFrame', params = ['data', 'columns'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_class2(self):
        self.data = {
            "DC_PEC": "import pandas as pd; import numpy as np",
            "DC_SOLUTION": "pd.DataFrame(data = np.zeros((5,2)), columns = ['a', 'b'])",
            "DC_CODE": "pd.DataFrame(np.zeros((5,2)), columns = ['a', 'b'])",
            "DC_SCT": "test_function_v2('pandas.DataFrame', params = ['data', 'columns'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_class3(self):
        self.data = {
            "DC_PEC": "import pandas as pd; import numpy as np",
            "DC_SOLUTION": "pd.DataFrame(columns = ['a', 'b'], data = np.zeros((5,2)))",
            "DC_CODE": "pd.DataFrame(data = np.zeros((5,2)), columns = ['a', 'b'])",
            "DC_SCT": "test_function_v2('pandas.DataFrame', params = ['data', 'columns'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_builtin1(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "round(1.123, ndigits = 2)",
            "DC_CODE": "round(1.123, ndigits = 2)",
            "DC_SCT": "test_function_v2('round', params = ['number', 'ndigits'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_builtin2(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "round(1.123, ndigits = 2)",
            "DC_CODE": "round(1.123, 2)",
            "DC_SCT": "test_function_v2('round', params = ['number', 'ndigits'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_builtin3(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "round(1.123, 2)",
            "DC_CODE": "round(1.123, ndigits = 2)",
            "DC_SCT": "test_function_v2('round', params = ['number', 'ndigits'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestStepByStep(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "df = pd.DataFrame([1, 2, 3], columns=['a'])",
            "DC_SCT": "test_function_v2('pandas.DataFrame', params=['data', 'columns'])"
        }

    def test_step1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_absent_lines(self, sct_payload)

    def test_step2(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(x=[1, 2, 3])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_step3(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_step4(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['b'])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_step5(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['a'])"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestStepByStepCustom(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "df = pd.DataFrame([1, 2, 3], columns=['a'])",
            "DC_SCT": '''
test_function_v2('pandas.DataFrame', params=['data', 'columns'],
                 not_called_msg='notcalledmsg',
                 params_not_matched_msg='paramsnotmatchedmsg',
                 params_not_specified_msg='paramsnotspecifiedmsg',
                 incorrect_msg='incorrectmsg')
            '''
        }

        self.SPEC2_SCT = """
Ex().check_function('pandas.DataFrame', 0, missing_msg = "notcalledmsg", expand_msg="", params_not_matched_msg='paramsnotmatchedmsg')\
        .multi(
            check_args('data', missing_msg='paramsnotspecifiedmsg'),
            check_args('columns', missing_msg='paramsnotspecifiedmsg'))
"""

    def test_step1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual('notcalledmsg', sct_payload['message'])
        helper.test_absent_lines(self, sct_payload)

    def test_step1_spec2(self):
        self.data["DC_SCT"] = self.SPEC2_SCT
        self.test_step1()

    def test_step2(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(x=[1, 2, 3])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual('paramsnotmatchedmsg', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 6, 30)

    def test_step2_spec2(self):
        self.data["DC_SCT"] = self.SPEC2_SCT
        self.test_step2()

    def test_step3(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('paramsnotspecifiedmsg', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 6, 33)

    def test_step3_spec2(self):
        self.data["DC_SCT"] = self.SPEC2_SCT
        self.test_step3()

    def test_step4(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['b'])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual('incorrectmsg', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 35, 47)

    def test_step5(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['a'])"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestStepByStepCustom2(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "df = pd.DataFrame([1, 2, 3], columns=['a'])",
            "DC_SCT": '''
test_function_v2('pandas.DataFrame', params=['data', 'columns'],
                 incorrect_msg=['dataincorrect', 'columnsincorrect'])
            '''
        }

    def test_step4(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3, 4], columns=['a'])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual('dataincorrect', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 19, 35)

    def test_step4b(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['b'])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual('columnsincorrect', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 35, 47)

    def test_step5(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['a'])"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestStepByStepCustom3(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "df = pd.DataFrame([1, 2, 3], columns=['a'])",
            "DC_SCT": '''
test_function_v2('pandas.DataFrame', params=['data', 'columns'],
                 params_not_specified_msg=['datanotspecified', 'columnsnotspecified'])
            '''
        }

    def test_step4(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('columnsnotspecified', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 6, 33)

    def test_step5(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['a'])"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestStepByStepPositional(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "x = 'test'",
            "DC_SOLUTION": "x.center(50, 't')",
            "DC_SCT": "test_function_v2('x.center', params=['width','fillchar'])"
        }

    def test_step1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_absent_lines(self, sct_payload)

    def test_step2(self):
        self.data["DC_CODE"] = "x.center(width = 50)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 20)

    def test_step3(self):
        self.data["DC_CODE"] = "x.center(50)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 12)

    def test_step4(self):
        self.data["DC_CODE"] = "x.center(50, 'c')"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 14, 16)

    def test_step5(self):
        self.data["DC_CODE"] = "x.center(50, 't')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestDoEval(unittest.TestCase):
    def test_do_eval_true_pass(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(2.1234, ndigits = 4)",
                     "DC_CODE": "round(2.1234, ndigits = 4)",
                     "DC_SCT": "test_function_v2('round', params=['number', 'ndigits'], do_eval = True)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_true_fail(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(2.1234, ndigits = 4)",
                     "DC_CODE": "round(2.123456, ndigits = 4)",
                     "DC_SCT": "test_function_v2('round', params=['number', 'ndigits'], do_eval = True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_do_eval_false_pass(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "x = 2.12309123; round(x, ndigits = 4)",
                     "DC_CODE": "x = 2.123450; round(x, ndigits = 4)",
                     "DC_SCT": "test_function_v2('round', params=['number', 'ndigits'], do_eval = False)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_false_fail(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "y = 2.12309123; round(y, ndigits = 4)",
                     "DC_CODE": "x = 2.123450; round(x, ndigits = 4)",
                     "DC_SCT": "test_function_v2('round', params=['number', 'ndigits'], do_eval = False)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_do_eval_none_pass(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, ndigits = 2)",
             "DC_CODE": "round(123.123, ndigits = 2)",
             "DC_SCT": "test_function_v2('round', params=['number', 'ndigits'], do_eval = None)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_none_fail1(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, ndigits = 2)",
             "DC_CODE": "round(123.123)",
             "DC_SCT": "test_function_v2('round', params=['number', 'ndigits'], do_eval = None)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_do_eval_none_fail2(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, 2)", # args = [0, 1]
             "DC_CODE": "round(123.123)", # student_args is len 1
             "DC_SCT": "test_function_v2('round', params=['number', 'ndigits'], do_eval = None)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

class TestDoEvalList(unittest.TestCase):
    def setUp(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "pow(3, 2, 4)",
                     "DC_SCT": "test_function_v2('pow', params=['x','y','z'], do_eval = [True, False, None])"}

    def test_do_eval_1(self):
        self.data["DC_CODE"] = "pow(3, 2, 4)"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_2(self):
        self.data["DC_CODE"] = "pow(4, 2, 4)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_do_eval_3(self):
        self.data["DC_CODE"] = "x = 2; pow(3, x, 4)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_do_eval_4(self):
        self.data["DC_CODE"] = "pow(3, 2, 3)"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


if __name__ == "__main__":
    unittest.main()
