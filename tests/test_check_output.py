import unittest
import helper

class TestCheckOutput(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SCT": "Ex().check_output(r'[H|h]i,*\\s+there!')",
            "DC_SOLUTION": ''
        }

    def test_success(self):
        self.data["DC_CODE"] = 'print("Hi, there!")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_success2(self):
        self.data["DC_CODE"] = 'print("hi  there!")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail(self):
        self.data["DC_CODE"] = 'print("Hello there")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])


class TestOutputContains(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SCT": "test_output_contains(r'[H|h]i,*\\s+there!')",
            "DC_SOLUTION": ''
        }

    def test_success(self):
        self.data["DC_CODE"] = 'print("Hi, there!")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_success2(self):
        self.data["DC_CODE"] = 'print("hi  there!")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail(self):
        self.data["DC_CODE"] = 'print("Hello there")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()