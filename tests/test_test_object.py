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
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Well done!")  

  def test_standardTestFail(self):
    self.data["DC_SCT"] = '''
test_object("savings2")
success_msg("Well done!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Have you defined <code>savings2</code>?")  


if __name__ == "__main__":
    unittest.main()