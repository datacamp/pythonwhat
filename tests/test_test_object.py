import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise
from pythonbackend import utils

import helper

class TestTestObjectScenarioOne(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# no pec
      ''',
      "DC_CODE": '''
# Create a variable savings
savings = 100

# Print out savings
print(savings)
      ''',
      "DC_SOLUTION": '''
# Create a variable savings
savings = 100
savings2 = 120

# Print out savings
print(savings)
      '''
    }

  def test_standardTestPass(self):
    self.data["DC_SCT"] = '''
test_object("savings")
test_function("print")
success_msg("Well done!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Well done!")

  def test_standardTestFail(self):
    self.data["DC_SCT"] = '''
test_object("savings2")
success_msg("Well done!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Have you defined <code>savings2</code>?")

class TestTestObjectWithNumpyArray(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
import numpy as np
      ''',
      "DC_CODE": '''
a = np.array([1,2,3])
b = np.array([1,2,np.nan])
c = np.array([4,5,np.nan])
      ''',
      "DC_SOLUTION": '''
a = np.array([1,2,3])
b = np.array([1,2,np.nan])
c = np.array([np.nan,4,5])
      '''
    }

  def test_arraysEqualWithoutNaN(self):
    self.data["DC_SCT"] = '''
test_object('a')
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_arraysEqualWithNaN(self):
    self.data["DC_SCT"] = '''
test_object('b')
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_arraysNotEqualWithNaN(self):
    self.data["DC_SCT"] = '''
test_object('c')
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)

if __name__ == "__main__":
    unittest.main()
