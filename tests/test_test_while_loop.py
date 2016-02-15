import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise
from pythonbackend import utils

import helper

class TestWhileLoop(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
# Initialize offset
offset = 8

# Code the while loop
while offset != 0 :
    print("correcting...")
    offset = offset - 1
    print(offset)
      ''',
      "DC_SOLUTION": '''
# Initialize offset
offset = 8

# Code the while loop
while offset != 0 :
    print("correcting...")
    offset = offset - 1
    print(offset)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_object("offset")

for i in range(-1,2):
  test_while_loop(1, test=lambda i=i: test_expression_result({"offset": i}))

for i in range(3,4):
  test_while_loop(1, body=lambda i=i: test_object_after_expression("offset", {"offset": i}))
  test_while_loop(1, body=lambda i=i: test_expression_output({"offset": i}))

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
