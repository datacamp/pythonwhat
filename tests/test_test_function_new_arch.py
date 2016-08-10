import unittest
import helper

class TestStepByStep(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": "df = pd.DataFrame([1, 2, 3], columns=['a'])",
            "DC_SCT": "test_function('pandas.DataFrame')"
            #"DC_SCT": "test_function_v2('pandas.DataFrame', params=['data', 'columns'])"
        }

    def test_pass(self):
        self.data["DC_CODE"] = "df = pd.DataFrame([1, 2, 3], columns=['a'])"
        sct_payload = helper.run(self.data)
        print(sct_payload)
        self.assertTrue(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()
