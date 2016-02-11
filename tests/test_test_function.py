import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise
from pythonbackend import utils

import helper

class TestFunctionBase(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
print(5 / 8)
print(7 + 10)
      ''',
      "DC_SOLUTION": '''
print(5 / 8)
print(7 + 10)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
msg = "Don't remove the first statement. It is an example which is coded for you!"
test_operator(1, incorrect_op_msg = msg, incorrect_result_msg = msg, not_found_msg = msg)
test_operator(2, not_found_msg = "You should add a second operation, as instructed.", 
  incorrect_op_msg = "Your second operation is wrong, be sure to add `7` to `10`.",
  incorrect_result_msg = "The operation you added should add up to `17`.")
test_function("print", 1)
test_function("print", 2)

success_msg("Great!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Great!")


if __name__ == "__main__":
    unittest.main()
