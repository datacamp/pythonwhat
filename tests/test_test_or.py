import unittest
import helper

class TestExercise1(unittest.TestCase):
    def setUp(self):
        self.data = {
          "DC_PEC": '',
          "DC_SCT": "test_or(lambda: test_function('print'), lambda: test_object('test'))",
          "DC_SOLUTION": "print('test')\ntest = 3"
        }

    def test_Pass1(self):
        self.data["DC_CODE"] = 'test = 3'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass2(self):
        self.data["DC_CODE"] = "print('test')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass3(self):
        self.data["DC_CODE"] = "test = 3\nprint('test')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass4(self):
        self.data["DC_CODE"] = "test = 4\nprint('test')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass4(self):
        self.data["DC_CODE"] = "test = 3\nprint('not test')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail1(self):
        self.data["DC_CODE"] = "test = 4\nprint('not test')"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Did you call <code>print()</code> with the correct arguments? The first argument seems to be incorrect.")

    def test_Pass4_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Pass4()

    def test_Pass4_spec2(self):
        self.data["DC_SCT"] = "Ex().test_or(test_function('print'), check_object('test'))"
        self.test_Pass4()

    def test_Fail1_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Fail1()

class TestNestedOr(unittest.TestCase):
    def setUp(self):
        self.data = {
                "DC_SOLUTION": """for ii in range(10): print('yes') if ii < 2 else print('no')""",
                "DC_SCT": """test_for_loop(1, body=test_if_exp(body=test_or(test_student_typed('print'))))"""
                }

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()
