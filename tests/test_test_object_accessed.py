import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise
from pythonbackend import utils

import helper

class TestTestObjectAccessed(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_CODE": '''
import numpy as np
arr = np.array([1, 2, 3])
x = arr.shape
      ''',
      "DC_SOLUTION": '''
import numpy as np
arr = np.array([1, 2, 3])
x = arr.shape
t = arr.dtype
      '''      
    }

  def test_standardTestPass(self):
    self.data["DC_SCT"] = 'test_object_accessed("arr")'
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

    self.data["DC_SCT"] = 'test_object_accessed("arr.shape")'
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    
    self.data["DC_SCT"] = 'test_object_accessed("arr.dtype")'
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    

if __name__ == "__main__":
    unittest.main()
