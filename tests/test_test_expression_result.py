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

    def test_no_copy_bad_sct_passes(self):
        self.data["DC_SOLUTION"] = "a = [2]"
        self.data["DC_CODE"] = "a = [1]"
        self.data["DC_SCT"] = "Ex().has_equal_value(expr_code = 'a[0] = 3', name = 'a', copy = False).has_equal_value(expr_code = 'a', name = 'a')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_copy_sct_fails(self):
        self.data["DC_SOLUTION"] = "a = [2]"
        self.data["DC_CODE"] = "a = [1]"
        self.data["DC_SCT"] = "Ex().has_equal_value(expr_code = 'a[0] = 3', name = 'a', copy = True).has_equal_value(name = 'a')"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()
