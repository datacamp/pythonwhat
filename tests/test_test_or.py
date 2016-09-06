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

if __name__ == "__main__":
    unittest.main()
