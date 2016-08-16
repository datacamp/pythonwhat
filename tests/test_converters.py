import unittest
import helper

class TestBuiltInConverters(unittest.TestCase):

    def test_excel(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "xl = pd.ExcelFile('battledeath.xlsx')",
            "DC_SCT": "test_object('xl')",
            "DC_CODE": "xl = pd.ExcelFile('battledeath.xlsx')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_dict_keys(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = {'a': 1, 'b': 2}; print(x.keys())",
            "DC_CODE": "x = {'a': 1, 'b':2}; print(x.keys())",
            "DC_SCT": "test_function_v2('print', params = ['value'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])



if __name__ == "__main__":
    unittest.main()
