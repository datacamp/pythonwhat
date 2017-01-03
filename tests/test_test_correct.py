import unittest
import helper

class TestExercise1(unittest.TestCase):
    def setUp(self):
        self.data = {
          "DC_PEC": 'import numpy as np',
          "DC_SCT": "test_correct(lambda: test_object('test'), lambda: test_function('numpy.sum'))",
          "DC_SOLUTION": 'test = np.sum([5, 2, 4, 9])'
        }

    def test_Pass1(self):
        self.data["DC_CODE"] = 'test = np.sum([5, 2, 4, 9])'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass2(self):
        self.data["DC_CODE"] = 'test = np.sum([5, 3, 3, 9])'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass3(self):
        self.data["DC_CODE"] = 'test = np.sum([5, 2, 4, 4, 5])'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail1(self):
        self.data["DC_CODE"] = 'test = 19'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you called <code>np.sum()</code>?")

    def test_Fail2(self):
        self.data["DC_CODE"] = 'test = np.sum([5, 2, 3])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Did you call <code>np.sum()</code> with the correct arguments? The first argument seems to be incorrect.')

    def test_Fail3(self):
        self.data["DC_SCT"] = "test_correct(lambda: test_object('test'), lambda: test_function('numpy.sum', args=[]))"
        self.data["DC_CODE"] = 'test = np.sum([5, 2, 3])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'The contents of <code>test</code> aren\'t correct.')

    def test_Fail2_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Fail2()

    def test_Pass2_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Pass2()

    def test_Pass2_spec2(self):
        self.data["DC_SCT"] = "Ex().test_correct(check_object('test').has_equal_value(), test_function('numpy.sum'))"
        self.test_Pass2()

    def test_Pass2_spec2_F(self):
        self.data["DC_SCT"] = """
test = F().test_correct(check_object('test').has_equal_value(), test_function('numpy.sum'))
Ex().multi(test)
"""
        self.test_Pass2()

    def test_Fail2_mix_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"], count=1)
        self.test_Fail2()
        
    def test_Pass2_mix_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"], count=1)
        self.test_Pass2()


if __name__ == "__main__":
    unittest.main()
