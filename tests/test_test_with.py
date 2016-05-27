import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise
from pythonbackend import utils

import helper

class TestExercise1(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
# # Read & print the first 3 lines
# with open('moby_dick.txt') as file:
#     print(file.readline())
#     print(file.readline())
#     print(file.readline())

# # The rows that you wish to print
# I = [0,1,3,5,6,7,8,9]

# # Print out these rows
# with open('moby_dick.txt') as file:
#     for i, row in enumerate(file):
#         if i in I:
#             print(row)
      ''',
      "DC_SOLUTION": '''
# # Read & print the first 3 lines
# with open('moby_dick.txt') as file:
#     print(file.readline())
#     print(file.readline())
#     print(file.readline())

# # The rows that you wish to print
# I = [0,1,3,5,6,7,8,9]

# # Print out these rows
# with open('moby_dick.txt') as file:
#     for i, row in enumerate(file):
#         if i in I:
#             print(row)
'''
    }

  def test_Pass1(self):
    self.data["DC_SCT"] = '''
  #test_with(1, body = lambda: [test_function('print') for _ in range(3)])
  success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    # self.assertIn("Check the <code>with</code> statement on line 3.", sct_payload['message'])

  def test_Pass1(self):
    self.data["DC_SCT"] = '''
#test_with(1, body = lambda: [test_function('print') for _ in range(3)], expand_message = False)
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    # self.assertNotIn("Check the <code>with</code> statement on line 3.", sct_payload['message'])


if __name__ == "__main__":
  unittest.main()
