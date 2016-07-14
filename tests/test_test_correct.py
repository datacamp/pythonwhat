import unittest
import helper

class TestExercise1(unittest.TestCase):
    def setUp(self):
        self.data = {
          "DC_PEC": 'import numpy as np',
          "DC_SCT": "test_correct(lambda: test_object('test'), lambda: test_function('numpy.sum'))",
          "DC_SOLUTION": ''
        }

    def test_Pass1(self):
        self.data["DC_CODE"] = 'test = np.sum([5, 2, 4, 9])'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass2(self):
        self.data["DC_CODE"] = 'test = 20'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass2(self):
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
        self.assertEqual(sct_payload['message'], 'Did you call <code>np.sum()</code> with the correct arguments? The first argument seems to be incorrect. Expected <code>[5, 2, 4, 9]</code>, but got <code>[5, 2, 3]</code>.')

    def test_Fail3(self):
        self.data["DC_SCT"] = 'test_correct(lambda: test_object('test'), lambda: test_function('numpy.sum', args=[]))'
        self.data["DC_CODE"] = 'test = np.sum([5, 2, 3])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'The contents of <code>test</code> aren\'t correct.')

if __name__ == "__main__":
    unittest.main()
