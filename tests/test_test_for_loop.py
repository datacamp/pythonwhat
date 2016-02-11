import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise
from pythonbackend import utils

import helper

class TestForLoop(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
size = 1
for i in range(10):
  size = size + i
  print("%d:%d" % (i, size))
      ''',
      "DC_SOLUTION": '''
size = 1
for n in range(10):
  size = size + 2*n
  size = size - n
  print("%d:%d" % (n, size))
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_for_loop(1, 
              lambda: test_function("range"),
              lambda: test_object_after_expression("size", {"size": 1}, [1]))
test_for_loop(1, 
              lambda: test_function("range"),
              lambda: test_expression_output({"size": 5}, [1]))
success_msg("Great!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Great!")

class TestForLoop2(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
# areas list
areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Code the for loop
for test in enumerate(areas) :
    print("room " + str(test[0]) + ": " + str(test[1]))
      ''',
      "DC_SOLUTION": '''
# areas list
areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Code the for loop
for index, area in enumerate(areas) :
    print("room " + str(index) + ": " + str(area))
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
msg = "Make sure to loop over `index, area` in `enumerate(areas)`"
test_for_loop(1, for_iter=lambda msg=msg: test_function("enumerate", incorrect_msg = msg))

msg = "Have another look at the example. Print out the correct string by looping over `index, aread` in `enumerate(areas)`"
test_for_loop(1, body=lambda msg=msg: test_expression_output(incorrect_msg = msg, context_vals = [2, "test"]))
success_msg("Well done!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Well done!")


if __name__ == "__main__":
    unittest.main()
