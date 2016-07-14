import unittest
import helper

class TestTestObjectBasic(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": 'savings2 = 110\nsavings2b = 110\nsavings2b=110\nsavings3 = 140',
            "DC_SOLUTION": 'savings = 100\nsavings2 = 120\nsavings2b = 120\nsavings3 = 140'
            }

    def test_fail_undef(self):
        self.data["DC_SCT"] = 'test_object("savings")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you defined <code>savings</code>?")
        self.assertFalse('line_start' in sct_payload)
        self.assertFalse('line_end' in sct_payload)
        self.assertFalse('column_start' in sct_payload)
        self.assertFalse('column_end' in sct_payload)

    def test_fail_incorr(self):
        self.data["DC_SCT"] = 'test_object("savings2")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>savings2</code> aren't correct.")
        self.assertEqual(sct_payload['line_start'], 1)
        self.assertEqual(sct_payload['line_end'], 1)
        self.assertEqual(sct_payload['column_start'], 1)
        self.assertEqual(sct_payload['column_end'], 14)

    def test_fail_incorr(self):
        self.data["DC_SCT"] = 'test_object("savings2b")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>savings2</code> aren't correct.")
        self.assertFalse('line_start' in sct_payload)
        self.assertFalse('line_end' in sct_payload)
        self.assertFalse('column_start' in sct_payload)
        self.assertFalse('column_end' in sct_payload)

    def test_pass(self):
        self.data["DC_SCT"] = 'test_object("savings3")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestTestObjectAttribute1(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '''
import numpy as np
arr = np.array([1, 2, 3, 4])
            ''',
            "DC_SOLUTION": '''
import numpy as np
arr = np.array([1, 2, 3])
            '''
            }

    def test_fail_incorrect(self):
        self.data["DC_SCT"] = 'test_object("arr.shape")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>arr.shape</code> aren't correct.")
        self.assertFalse('line_start' in sct_payload)
        self.assertFalse('line_end' in sct_payload)
        self.assertFalse('column_start' in sct_payload)
        self.assertFalse('column_end' in sct_payload)

    def test_pass(self):
        self.data["DC_SCT"] = 'test_object("np.dtype")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestTestObjectAttribute2(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '''
class Try():

    def __init__(self):
        self.savings2 = 110
        self.savings3 = 140

tryobj = Try()
            ''',
            "DC_SOLUTION": '''
class Try():

    def __init__(self):
        self.savings = 100
        self.savings2 = 110
        self.savings3 = 140

tryobj = Try()
            '''
            }

    def test_fail_undef(self):
        self.data["DC_SCT"] = 'test_object("tryobj.savings")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you defined <code>tryobj.savings</code>?")
        self.assertFalse('line_start' in sct_payload)
        self.assertFalse('line_end' in sct_payload)
        self.assertFalse('column_start' in sct_payload)
        self.assertFalse('column_end' in sct_payload)

    def test_fail_incorr(self):
        self.data["DC_SCT"] = 'test_object("tryobj.savings2")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The contents of <code>tryobj.savings2</code> aren't correct.")
        self.assertFalse('line_start' in sct_payload)
        self.assertFalse('line_end' in sct_payload)
        self.assertFalse('column_start' in sct_payload)
        self.assertFalse('column_end' in sct_payload)

    def test_pass(self):
        self.data["DC_SCT"] = 'test_object("tryobj.savings3")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


if __name__ == "__main__":
    unittest.main()