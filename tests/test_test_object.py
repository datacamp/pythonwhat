import unittest
import helper

class TestObjectStepByStep(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = 100",
            "DC_SCT": "test_object('x')"
        }

    def test_step_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you defined <code>x</code>?")

    def test_step_2(self):
        self.data["DC_CODE"] = "x = 500"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>x</code> aren't correct.")
        helper.test_lines(self, sct_payload, 1, 1, 1, 7)

    def test_pass(self):
        self.data["DC_CODE"] = "x = 100"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestObjectStepByStepCustom(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = 100",
            "DC_SCT": "test_object('x', undefined_msg = 'undefined', incorrect_msg = 'incorrect')"
        }

    def test_step_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "undefined")

    def test_step_2(self):
        self.data["DC_CODE"] = "x = 500"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "incorrect")
        helper.test_lines(self, sct_payload, 1, 1, 1, 7)

    def test_pass(self):
        self.data["DC_CODE"] = "x = 100"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestTestObjectNonDillable(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "xl = pd.ExcelFile('battledeath.xlsx')",
            "DC_SCT": "test_object('xl')"
        }

    def test_step_1(self):
        self.data["DC_CODE"] = "xl = pd.ExcelFile('battledeath.xlsx')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestTestObjectManualConverter(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "xl = pd.ExcelFile('battledeath.xlsx')",
            "DC_SCT": '''
def my_converter(x):
    return(x.sheet_names)
set_converter(key = "pandas.io.excel.ExcelFile", fundef = my_converter)
test_object('xl')
'''
        }

    def test_step_1(self):
        self.data["DC_CODE"] = "xl = pd.ExcelFile('battledeath2.xlsx')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()


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
        self.assertEqual(sct_payload['message'], "The contents of <code>a</code> aren't correct.")
        helper.test_lines(self, sct_payload, 3, 3, 5, 9)

    def test_fail_else(self):
        self.data["DC_SCT"] = 'test_object("c")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>c</code> aren't correct.")
        helper.test_lines(self, sct_payload, 8, 8, 5, 9)

    def test_fail_for(self):
        self.data["DC_SCT"] = 'test_object("d")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>d</code> aren't correct.")
        helper.test_lines(self, sct_payload, 11, 11, 5, 9)

    def test_fail_for(self):
        self.data["DC_SCT"] = 'test_object("e")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>e</code> aren't correct.")
        helper.test_lines(self, sct_payload, 15, 15, 5, 9)

    def test_fail_try(self):
        self.data["DC_SCT"] = 'test_object("f")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>f</code> aren't correct.")
        helper.test_lines(self, sct_payload, 19, 19, 5, 9)

    def test_fail_try_finally_1(self):
        self.data["DC_SCT"] = 'test_object("g")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>g</code> aren't correct.")
        helper.test_lines(self, sct_payload, 24, 24, 5, 9)

    def test_fail_try_finally_2(self):
        self.data["DC_SCT"] = 'test_object("h")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>h</code> aren't correct.")
        helper.test_lines(self, sct_payload, 28, 28, 5, 9)

    def test_fail_if2(self):
        self.data["DC_SCT"] = 'test_object("i")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>i</code> aren't correct.")
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
        self.data["DC_SCT"] = 'test_object("df")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail(self):
        self.data["DC_SCT"] = 'test_object("df2")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_absent_lines(self, sct_payload)



# This is for some day

# class TestTestObjectAttribute1(unittest.TestCase):
#     def setUp(self):
#         self.data = {
#             "DC_PEC": '',
#             "DC_CODE": '''
# import numpy as np
# arr = np.array([1, 2, 3, 4])
#             ''',
#             "DC_SOLUTION": '''
# import numpy as np
# arr = np.array([1, 2, 3])
#             '''
#             }

#     def test_fail_incorrect(self):
#         self.data["DC_SCT"] = 'test_object("arr.shape")'
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], "The contents of <code>arr.shape</code> aren't correct.")
#         helper.test_absent_lines(self, sct_payload)

#     def test_pass(self):
#         self.data["DC_SCT"] = 'test_object("np.dtype")'
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])


# class TestTestObjectAttribute2(unittest.TestCase):
#     def setUp(self):
#         self.data = {
#             "DC_PEC": '',
#             "DC_CODE": '''
# class Try():

#     def __init__(self):
#         self.savings2 = 110
#         self.savings3 = 140

# tryobj = Try()
#             ''',
#             "DC_SOLUTION": '''
# class Try():

#     def __init__(self):
#         self.savings = 100
#         self.savings2 = 110
#         self.savings3 = 140

# tryobj = Try()
#             '''
#             }

#     def test_fail_undef(self):
#         self.data["DC_SCT"] = 'test_object("tryobj.savings")'
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], "Have you defined <code>tryobj.savings</code>?")
#         helper.test_absent_lines(self, sct_payload)

#     def test_fail_incorr(self):
#         self.data["DC_SCT"] = 'test_object("tryobj.savings2")'
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], "The contents of <code>tryobj.savings2</code> aren't correct.")
#         helper.test_absent_lines(self, sct_payload)

#     def test_pass(self):
#         self.data["DC_SCT"] = 'test_object("tryobj.savings3")'
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])


if __name__ == "__main__":
    unittest.main()
