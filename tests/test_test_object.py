import unittest
import helper
from pythonwhat.local import setup_state
from pythonwhat.Test import TestFail as TF
import pytest

@pytest.mark.parametrize('sct', [
    "test_object('x', undefined_msg='udm', incorrect_msg='icm')",
    "Ex().check_object('x', missing_msg='udm').has_equal_value(incorrect_msg='icm')"
])
@pytest.mark.parametrize('stu_code, passes, msg', [
    ('', False, 'udm'),
    ('x = 1', False, 'icm'),
    ('x = 100', True, None)
])
def test_check_object(sct, stu_code, passes, msg):
    output = helper.run({
        'DC_SOLUTION': 'x = 100',
        'DC_CODE': stu_code,
        'DC_SCT': sct
    })
    assert output['correct'] == passes
    if msg: assert output['message'] == msg

def test_check_object_wrong_usage():
    with pytest.raises(NameError):
        helper.run({
            'DC_SCT': 'Ex().check_object("x")'
        })

@pytest.mark.parametrize('stu_code, passes', [
    ('x = filter(lambda x: x > 0, [0, 1])', False),
    ('x = filter(lambda x: x > 0, [1, 1])', True)
])
def test_check_object_exotic_compare(stu_code, passes):
    output = helper.run({
        'DC_SOLUTION': 'x = filter(lambda x: x > 0, [1, 1])',
        'DC_SCT': "Ex().check_object('x').has_equal_value()",
        'DC_CODE': stu_code
    })
    assert output['correct'] == passes

@pytest.mark.parametrize('stu_code, passes', [
    ('x = [1, 2, 3]', True),
    ('x = [1, 2, 3, 4]', False)
])
def test_check_object_custom_compare(stu_code, passes):
    output = helper.run({
        "DC_SOLUTION": 'x = [4, 5, 6]',
        'DC_CODE': stu_code,
		'DC_SCT': 'Ex().check_object("x").has_equal_value(func = lambda x,y: len(x) == len(y))'
	})
    assert output['correct'] == passes

def test_check_object_single_process():
    state2pids = setup_state('x = 3', '')
    with pytest.raises(NameError):
        state2pids.check_object('x')
    state1pid = setup_state('x = 3', '', pid = 1)
    helper.passes(state1pid.check_object('x'))

@pytest.mark.parametrize('stu_code, passes', [
    ('arr = 4', False),
    ('arr = np.array([1])', True)
])
def test_is_instance(stu_code, passes):
    output = helper.run({
        'DC_PEC': 'import numpy as np',
        'DC_SOLUTION': 'arr = np.array([1, 2, 3, 4])',
        'DC_SCT': "import numpy; Ex().check_object('arr').is_instance(numpy.ndarray)",
        'DC_CODE': stu_code
    })
    assert output['correct'] == passes

@pytest.mark.parametrize('sct', [
    "test_data_frame('df', columns=['a'], undefined_msg='udm', not_data_frame_msg='ndfm', undefined_cols_msg='ucm', incorrect_msg='icm')",
    "test_data_frame('df', columns=None, undefined_msg='udm', not_data_frame_msg='ndfm', undefined_cols_msg='ucm', incorrect_msg='icm')",
    """
import pandas as pd
Ex().check_object('df', missing_msg='udm', expand_msg='').\
     is_instance(pd.DataFrame, not_instance_msg='ndfm').\
     check_keys('a', missing_msg='ucm').has_equal_value(incorrect_msg='icm')
    """,
    """
import pandas as pd
Ex().check_df('df', missing_msg='udm', expand_msg='', not_instance_msg='ndfm').\
     check_keys('a', missing_msg='ucm').has_equal_value(incorrect_msg='icm')
    """
])
@pytest.mark.parametrize('stu_code, passes, msg', [
    ('', False, 'udm'),
    ('df = 3', False, 'ndfm'),
    ('df = pd.DataFrame({ "b": [1]})', False, 'ucm'),
    ('df = pd.DataFrame({ "a": [1]})', False, 'icm'),
    ('df = pd.DataFrame({ "a": [1, 2, 3] })', True, None),
    ('df = pd.DataFrame({ "a": [1, 2, 3], "b": [3, 4, 5] })', True, None),
])
def test_test_data_frame(sct, stu_code, passes, msg):
    output = helper.run({
        'DC_PEC': 'import pandas as pd',
        'DC_SOLUTION': 'df = pd.DataFrame({"a": [1, 2, 3]})',
        'DC_CODE': stu_code,
        'DC_SCT': sct
    })
    assert output['correct'] == passes
    if msg: assert output['message'] == msg

@pytest.mark.parametrize('stu_code, passes', [
    ('x = {}', False),
    ('x = {"b": 3}', False),
    ('x = {"a": 3}', False),
    ('x = {"a": 2}', True),
    ('x = {"a": 2, "b": 3}', True),
])
def test_check_keys(stu_code, passes):
    output = helper.run({
        'DC_SOLUTION': 'x = {"a": 2}',
        'DC_CODE': stu_code,
        'DC_SCT': 'Ex().check_object("x").check_keys("a").has_equal_value()'
    })
    assert output['correct'] == passes

@pytest.mark.parametrize('sct', [
    "Ex().test_data_frame('pivot')",
    "Ex().check_df('pivot').check_keys(('visitors', 'Austin')).has_equal_value()"
])
def test_check_keys_exotic(sct):
    code = "pivot = users.pivot(index='weekday', columns='city')"
    output = helper.run({
        'DC_PEC': '''
import pandas as pd
users = pd.read_csv('https://s3.amazonaws.com/assets.datacamp.com/production/course_1650/datasets/users.csv')
''',
        'DC_SOLUTION': code,
        'DC_CODE': code,
        'DC_SCT': sct
    })
    assert output['correct']

def test_check_keys_wrong_usage():
    with pytest.raises(NameError):
        helper.run({
            'DC_SOLUTION': 'x = {"a": 2}',
            'DC_CODE': 'x = {"a": 2}',
            'DC_SCT': 'Ex().check_object("x").check_keys("b")'
        })

@pytest.mark.need_internet
class TestTestObjectNonDillable(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import pandas as pd; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/battledeath.xlsx', 'battledeath.xlsx')",
            "DC_SOLUTION": "xl = pd.ExcelFile('battledeath.xlsx')",
            "DC_SCT": "test_object('xl')"
        }

    def test_step_1(self):
        self.data["DC_CODE"] = "xl = pd.ExcelFile('battledeath.xlsx')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestTestObjectManualConverter(unittest.TestCase):

    @pytest.mark.need_internet
    @pytest.mark.compiled
    def test_pass_1(self):
        self.data = {
            "DC_PEC": "import pandas as pd; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/battledeath.xlsx', 'battledeath.xlsx'); from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/battledeath.xlsx', 'battledeath2.xlsx')",
            "DC_SOLUTION": "xl = pd.ExcelFile('battledeath.xlsx')",
            "DC_CODE": "xl = pd.ExcelFile('battledeath2.xlsx')",
            "DC_SCT": '''
def my_converter(x):
    return(x.sheet_names)
set_converter(key = "pandas.io.excel.ExcelFile", fundef = my_converter)
test_object('xl')
'''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestTestObjectManualConverter2(unittest.TestCase):

    @pytest.mark.compiled
    def test_pass_1(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "my_array = np.array([[1,2], [3,4], [5,6]])",
            "DC_CODE": "my_array = np.array([[0,0], [0,0], [0,0]])",
            "DC_SCT": "set_converter(key = 'numpy.ndarray', fundef = lambda x: x.shape); test_object('my_array')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestTestObjectEqualityChallenges(unittest.TestCase):
    def test_pass1(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "x = np.mean([1, 2, 3])",
            "DC_CODE": "x = 2",
            "DC_SCT": "test_object('x')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass2(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "x = 2.0",
            "DC_CODE": "x = 2",
            "DC_SCT": "test_object('x')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass3(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = None",
            "DC_CODE": "x = None",
            "DC_SCT": "test_object('x')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    @pytest.mark.need_internet
    def test_pass4(self):
        self.data = {
            "DC_PEC": "import scipy.io; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/ja_data2.mat', 'albeck_gene_expression.mat')",
            "DC_SOLUTION": "mat = scipy.io.loadmat('albeck_gene_expression.mat')\nprint(type(mat))",
            "DC_CODE": "mat = scipy.io.loadmat('albeck_gene_expression.mat')\nprint(type(mat))",
            "DC_SCT": "test_object('mat')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestTestObjectDeep(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '''
if True:
    a = 1

if False:
    b = 2
else:
    c = 3

for i in range(2):
    d = 4

x = 2
while x > 0:
    e = 5
    x -= 1

try:
    f = 6
except:
    pass

try:
    g = 7
except:
    pass
finally:
    h = 8

# 2 assignments
i = 9
if True:
    i = 9
            ''',
            "DC_SOLUTION": '''
if True:
    a = 10

if False:
    b = 20
else:
    c = 30

for i in range(2):
    d = 40

x = 2
while x > 0:
    e = 50
    x -= 1

try:
    f = 60
except:
    pass

try:
    g = 70
except:
    pass
finally:
    h = 80

# 2 assignments
i = 90
if True:
    i = 90
            '''
            }

    def test_fail_if(self):
        self.data["DC_SCT"] = 'test_object("a")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 3, 3, 5, 9)

    def test_fail_else(self):
        self.data["DC_SCT"] = 'test_object("c")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 8, 8, 5, 9)

    def test_fail_for(self):
        self.data["DC_SCT"] = 'test_object("d")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 11, 11, 5, 9)

    def test_fail_for_2(self):
        self.data["DC_SCT"] = 'test_object("e")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 15, 15, 5, 9)

    def test_fail_try(self):
        self.data["DC_SCT"] = 'test_object("f")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 19, 19, 5, 9)

    def test_fail_try_finally_1(self):
        self.data["DC_SCT"] = 'test_object("g")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 24, 24, 5, 9)

    def test_fail_try_finally_2(self):
        self.data["DC_SCT"] = 'test_object("h")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 28, 28, 5, 9)

    def test_fail_if2(self):
        self.data["DC_SCT"] = 'test_object("i")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_absent_lines(self, sct_payload)


class TestTestObjectDifferentAssignments(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '''
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df.columns = ["c", "d"]

df2 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df2.columns = ["e", "f"]
            ''',
            "DC_SOLUTION": '''
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df.columns = ["c", "d"]

df2 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df2.columns = ["c", "d"]
            '''
            }

    def test_pass(self):
        self.data["DC_SCT"] = 'Ex().check_object("df").has_equal_value()'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail(self):
        self.data["DC_SCT"] = 'Ex().check_object("df2").has_equal_value()'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_absent_lines(self, sct_payload)




if __name__ == "__main__":
    unittest.main()
