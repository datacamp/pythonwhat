import unittest
import helper

class TestTestObjectAccessed(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '''
import numpy as np
import math as m
arr = np.array([1, 2, 3])
x = arr.shape
print(arr.data)
print(m.e)
            ''',
            "DC_SOLUTION": '# not used'      
        }

    def test_objectArr(self):
        self.data["DC_SCT"] = 'test_object_accessed("arr")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_objectAr(self):
        self.data["DC_SCT"] = 'test_object_accessed("ar")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_objectArrTwice(self):
        self.data["DC_SCT"] = 'test_object_accessed("arr", times=2)'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_objectArrThrice(self):
        self.data["DC_SCT"] = 'test_object_accessed("arr", times=3)'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you accessed <code>arr</code> at least 3 times?")

    def test_objectArrThriceCustom(self):
        self.data["DC_SCT"] = 'test_object_accessed("arr", times=3, not_accessed_msg="silly")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "silly")

    def test_objectAndAttribute(self):
        self.data["DC_SCT"] = 'test_object_accessed("arr.shape")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_objectAndAttributeTwice(self):
        self.data["DC_SCT"] = 'test_object_accessed("arr.shape", times=2)'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you accessed <code>arr.shape</code> at least twice?")

    def test_objectAndAttributeTwiceCustom(self):
        self.data["DC_SCT"] = 'test_object_accessed("arr.shape", times=2, not_accessed_msg="silly")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "silly")
        
    def test_objectAndAttributeOnce(self):
        self.data["DC_SCT"] = 'test_object_accessed("arr.dtype")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you accessed <code>arr.dtype</code>?")

    def test_objectAndAttributeOnceCustom(self):
        self.data["DC_SCT"] = 'test_object_accessed("arr.dtype", not_accessed_msg="silly")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "silly")

    def test_objectInPackageOK(self):
        self.data["DC_SCT"] = 'test_object_accessed("math.e")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_objectInPackageNOK(self):
        self.data["DC_SCT"] = 'test_object_accessed("math.pi")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you accessed <code>m.pi</code>?")

    def test_objectInPackageNOKCustom(self):
        self.data["DC_SCT"] = 'test_object_accessed("math.pi", not_accessed_msg="silly")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "silly")

if __name__ == "__main__":
    unittest.main()
