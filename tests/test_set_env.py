import unittest
import helper

class TestSetEnv(unittest.TestCase):

    def test_Pass1(self):
        sct_payload = helper.run({ "DC_SCT": "Ex().set_env(x=4).has_equal_value(name='x')"})
        self.assertTrue(sct_payload['correct'])

    def test_Pass2(self):
        sct_payload = helper.run({ "DC_SCT": "Ex().set_env(x=4).set_env(y = 5).has_equal_value(name='x').has_equal_value(name='y')"})
        self.assertTrue(sct_payload['correct'])

    def test_Pass3(self):
        sct_payload = helper.run({ "DC_SCT": "Ex().set_env(x=4, y = 5).has_equal_value(name='x').has_equal_value(name='y')"})
        self.assertTrue(sct_payload['correct'])

    def test_Fail(self):
        # envs are not preserved in other branches of State
        sct_payload = helper.run({ "DC_SCT": "Ex().multi(set_env(x=4), set_env(y = 5).has_equal_value(name='x'))"})
        self.assertFalse(sct_payload['correct'])

    def testExample(self):
        data = {
            "DC_PEC": "a_list = list(range(100))",
            "DC_SOLUTION": "print(a_list[1])",
            "DC_SCT": "Ex().set_env(a_list = list(range(10))).has_equal_output()"
        }
        data["DC_CODE"] = "print(a_list[1])"
        sct_payload = helper.run(data)
        self.assertTrue(sct_payload['correct'])
        data["DC_CODE"] = "print(a_list[2])"
        sct_payload = helper.run(data)
        self.assertFalse(sct_payload['correct'])
   