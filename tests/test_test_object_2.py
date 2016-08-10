import unittest
import helper

class TestTestObjectBasic(unittest.TestCase):

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
        self.data["DC_CODE"] = "x = 50"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>x</code> aren't correct.")

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

