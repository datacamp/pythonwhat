import unittest
import helper

class TestExpressionOutputBasic(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "a = 2",
            "DC_SCT": "test_expression_result(expr_code = 'a', error_msg = 'cough')"
        }

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'cough')

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()
