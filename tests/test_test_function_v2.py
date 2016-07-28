import unittest
import helper

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
        self.assertIn('The argument you specified for <code>a</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 8, 8)

    def test_builtin_pass(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "print('test')",
            "DC_CODE": "print('test')",
            "DC_SCT": "test_function_v2('print', params = ['value'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_builtin_fail(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "print('test')",
            "DC_CODE": "print('testing')",
            "DC_SCT": "test_function_v2('print', params = ['value'])"
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('The argument you specified for <code>value</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 7, 15)

    def test_custom_builtin_pass(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "max([1, 2, 3, 4])",
            "DC_CODE": "max([1, 2, 3, 4])",
            "DC_SCT": '''
sig = build_sig(param('iterable', param.POSITIONAL_ONLY))
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
sig = build_sig(param('iterable', param.POSITIONAL_ONLY))
test_function_v2('max', params = ['iterable'], signature = sig)
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('The argument you specified for <code>iterable</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 5, 18)

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
        self.assertIn('The argument you specified for <code>data</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 19, 36)

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
        self.assertIn('The argument you specified for <code>object</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 16, 26)

    def test_custom_package_builtin_pass(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "com = np.complex(2, 4)",
            "DC_CODE": "com = np.complex(2, 4)",
            "DC_SCT": '''
sig = build_sig(param('real', param.POSITIONAL_OR_KEYWORD), param('imag', param.POSITIONAL_OR_KEYWORD, default=0))
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
sig = build_sig(param('real', param.POSITIONAL_OR_KEYWORD), param('imag', param.POSITIONAL_OR_KEYWORD, default=0))
test_function_v2('numpy.complex', params = ['real', 'imag'], signature=sig)
            '''}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('The argument you specified for <code>imag</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 21, 21)

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
        self.assertIn('The argument you specified for <code>value</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 9, 12)

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
        self.assertIn('The argument you specified for <code>object</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 12, 15)

    def test_custom_method_builtin_pass(self):
        self.data = {
            "DC_PEC": "arr = [1, 2, 3, 4]",
            "DC_SOLUTION": "res = arr.count(2)",
            "DC_CODE": "res = arr.count(2)",
            "DC_SCT": '''
sig = build_sig(param('value', param.POSITIONAL_ONLY))
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
sig = build_sig(param('value', param.POSITIONAL_ONLY))
test_function_v2('arr.count', params = ['value'], signature=sig)
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('The argument you specified for <code>value</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 17, 20)

class TestIrregularities(unittest.TestCase):
    def test_fun_insufficient_calls_solution(self):
        self.data = {
            "DC_PEC": "arr = [1, 2, 3, 4]",
            "DC_SOLUTION": "",
            "DC_CODE": "",
            "DC_SCT": "test_function_v2('print')"
        }
        self.assertRaises(NameError, helper.run, self.data)

    def test_fun_insufficient_calls_solution2(self):
        self.data = {
            "DC_PEC": "arr = [1, 2, 3, 4]",
            "DC_SOLUTION": "print(arr)",
            "DC_CODE": "print(arr)",
            "DC_SCT": "test_function_v2('print', index = 2)"
        }
        self.assertRaises(NameError, helper.run, self.data)

    def test_fun_wrong_call_solution(self):
        self.data = {
            "DC_PEC": "arr = [1, 2, 3, 4]",
            "DC_SOLUTION": "arr.count(2)",
            "DC_CODE": "arr.count(2)",
            "DC_SCT": "test_function_v2('arr.count', params = ['value'])"
        }
        self.assertRaises(ValueError, helper.run, self.data)

    def test_fun_wrong_call_solution2(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "x = np.complex(1)",
            "DC_CODE": "np.complex(1, 2)",
            "DC_SCT": '''
sig = build_sig(param('real', param.POSITIONAL_OR_KEYWORD), param('imag', param.POSITIONAL_OR_KEYWORD, default=0))
test_function_v2('numpy.complex', params = ['real', 'imag'], signature=sig)
            '''}
        self.assertRaises(ValueError, helper.run, self.data)

    def test_fun_wrong_call_student(self):
        self.data = {
            "DC_PEC": "def my_fun(a):\n    pass",
            "DC_SOLUTION": "my_fun(1)",
            "DC_CODE": "my_fun(b = 1)",
            "DC_SCT": "test_function_v2('my_fun', params = ['a'])"
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('Something went wrong in figuring out how', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 13)

class TestArgsKeywords(unittest.TestCase):

    def test_fun1(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": "file = open('moby_dick.txt', 'r')\nfile.close()",
            "DC_CODE": "file = open('moby_dick.txt', 'r')\nfile.close()",
            "DC_SCT": 'test_function_v2("open", params=["file", "mode"])'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fun2(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": "file = open('moby_dick.txt', 'r')\nfile.close()",
            "DC_CODE": "file = open('moby_dick.txt', mode='r')\nfile.close()",
            "DC_SCT": 'test_function_v2("open", params=["file", "mode"])'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fun3(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": "file = open('moby_dick.txt', mode='r')\nfile.close()",
            "DC_CODE": "file = open('moby_dick.txt', mode='r')\nfile.close()",
            "DC_SCT": 'test_function_v2("open", params=["file", "mode"])'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fun4(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": "file = open('moby_dick.txt', mode='r')\nfile.close()",
            "DC_CODE": "file = open('moby_dick.txt', 'r')\nfile.close()",
            "DC_SCT": 'test_function_v2("open", params=["file", "mode"])'
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

    def test_method1(self):
        self.data = {
             "DC_PEC": '''
from urllib.request import urlretrieve
from sqlalchemy import create_engine, MetaData, Table
engine = create_engine('sqlite:///census.sqlite')
metadata = MetaData()
connection = engine.connect()
from sqlalchemy import select
census = Table('census', metadata, autoload=True, autoload_with=engine)
stmt = select([census])
             ''',
            "DC_SOLUTION": '''
x = connection.execute(stmt).fetchall()
            ''',
             "DC_CODE": '''
x = connection.execute(stmt).fetchall()
            ''',
            "DC_SCT": '''
test_function_v2('connection.execute', params = ['object'], do_eval = False)
test_function_v2('connection.execute.fetchall', params = [])
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_method2(self):
        self.data = {
             "DC_PEC": '''
from urllib.request import urlretrieve
from sqlalchemy import create_engine, MetaData, Table
engine = create_engine('sqlite:///census.sqlite')
metadata = MetaData()
connection = engine.connect()
from sqlalchemy import select
census = Table('census', metadata, autoload=True, autoload_with=engine)
stmt = select([census])
             ''',
            "DC_SOLUTION": '''
x = connection.execute(stmt).fetchall()
            ''',
             "DC_CODE": '''
x = connection.execute(object = stmt).fetchall()
            ''',
            "DC_SCT": '''
test_function_v2('connection.execute', params = ['object'], do_eval = False)
test_function_v2('connection.execute.fetchall', params = [])
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestMultipleCalls(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
print("abc")
print(123)
print([1, 2, 3])
            ''',
             "DC_SCT": '''
test_function_v2("print", index = 1, params = ['value'])
test_function_v2("print", index = 2, params = ['value'])
test_function_v2("print", index = 3, params = ['value'])
            '''
        }
    def test_multiple_1(self):
        self.data["DC_CODE"] = 'print("abc")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the second call of <code>print()</code>, but hasn't found it; have another look at your code.")

    def test_multiple_2(self):
        self.data["DC_CODE"] = 'print("abc")\nprint(123)'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the third call of <code>print()</code>, but hasn't found it; have another look at your code.")

    def test_multiple_3(self):
        self.data["DC_CODE"] = 'print("abc")\nprint(123)\nprint([1, 2, 3])'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_multiple_4(self):
        self.data["DC_CODE"] = 'print("acb")\nprint(1234)\nprint([1, 2, 3])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>print()</code> with the correct arguments? The argument you specified for <code>value</code> seems to be incorrect.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 7, 11)

    def test_multiple_5(self):
        self.data["DC_CODE"] = 'print("abc")\nprint(1234)\nprint([1, 2, 3])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>print()</code> with the correct arguments? The argument you specified for <code>value</code> seems to be incorrect.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 2, 2, 7, 10)

    def test_multiple_6(self):
        self.data["DC_CODE"] = 'print("abc")\nprint(123)\nprint([1, 2, 3, 4])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>print()</code> with the correct arguments? The argument you specified for <code>value</code> seems to be incorrect.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 3, 3, 7, 18)


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
        self.assertIn('Have you called <code>pd.DataFrame()</code>?', sct_payload['message'])
        helper.test_absent_lines(self, sct_payload)

    def test_step2(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(x=[1, 2, 3])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('Something went wrong in figuring out how you specified the arguments for <code>pd.DataFrame()</code>', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 6, 30)

    def test_step3(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('Have you specified all required arguments inside <code>pd.DataFrame()</code>? You didn\'t specify <code>columns</code>.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 6, 33)

    def test_step4(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['b'])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('Did you call <code>pd.DataFrame()</code> with the correct arguments? The argument you specified for <code>columns</code> seems to be incorrect.', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 43, 47)

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

    def test_step1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual('notcalledmsg', sct_payload['message'])
        helper.test_absent_lines(self, sct_payload)

    def test_step2(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(x=[1, 2, 3])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual('paramsnotmatchedmsg', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 6, 30)

    def test_step3(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual('paramsnotspecifiedmsg', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 6, 33)

    def test_step4(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['b'])"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual('incorrectmsg', sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 43, 47)

    def test_step5(self):
        self.data["DC_CODE"] = "df = pd.DataFrame(data=[1, 2, 3], columns=['a'])"
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
        self.assertIn("Did you call <code>round()</code> with the correct arguments?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 7, 14)

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
        self.assertEqual("Did you call <code>round()</code> with the correct arguments? The argument you specified for <code>number</code> seems to be incorrect.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 21, 21)

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
        self.assertEqual("Have you specified all required arguments inside <code>round()</code>? You didn\'t specify <code>ndigits</code>.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 14)

    def test_do_eval_none_fail2(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, 2)", # args = [0, 1]
             "DC_CODE": "round(123.123)", # student_args is len 1
             "DC_SCT": "test_function_v2('round', params=['number', 'ndigits'], do_eval = None)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Have you specified all required arguments inside <code>round()</code>? You didn\'t specify <code>ndigits</code>.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 14)

if __name__ == "__main__":
    unittest.main()