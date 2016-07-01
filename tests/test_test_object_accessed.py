import os
import unittest

from os.path import exists
from unittest.mock import patch

import helper

class TestTestObjectAccessed(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '',
      "DC_CODE": '''
import numpy as np
arr = np.array([1, 2, 3])
x = arr.shape
print(arr.data)
      ''',
      "DC_SOLUTION": '''
      # not used
      '''      
    }

  def test_objectOnly(self):
    self.data["DC_SCT"] = 'test_object_accessed("arr")'
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)

    self.data["DC_SCT"] = 'test_object_accessed("arr", times=2)'
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)

    self.data["DC_SCT"] = 'test_object_accessed("arr", times=3)'
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Have you accessed <code>arr</code> at least 3 times?")

    self.data["DC_SCT"] = 'test_object_accessed("arr", times=3, not_accessed_msg="silly")'
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "silly")


  def test_objectAndAttribute(self):

    self.data["DC_SCT"] = 'test_object_accessed("arr.shape")'
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)

    self.data["DC_SCT"] = 'test_object_accessed("arr.shape", times=2)'
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Have you accessed <code>arr.shape</code> at least twice?")

    self.data["DC_SCT"] = 'test_object_accessed("arr.shape", times=2, not_accessed_msg="silly")'
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "silly")
    
    self.data["DC_SCT"] = 'test_object_accessed("arr.dtype")'
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Have you accessed <code>arr.dtype</code>?")

    self.data["DC_SCT"] = 'test_object_accessed("arr.dtype", not_accessed_msg="silly")'
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "silly")


if __name__ == "__main__":
    unittest.main()
