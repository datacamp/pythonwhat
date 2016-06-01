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
      "DC_PEC": '''
      ''',
      "DC_CODE": '''
# Open a file
file = open('moby_dick.txt' , 'r') # 'r' is to read only.

# Print it
print(file.read())

# Check whether file is closed
print(file.closed)

# Close file
file.close()

# Check whether file is closed
print(file.closed)
      ''',
      "DC_SOLUTION": '''
# Open a file
file = open('moby_dick.txt' , 'r') # 'r' is to read only.

# Print it
print(file.read())

# Check whether file is closed
print(file.closed)

# Close file
file.close()

# Check whether file is closed
print(file.closed)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_function("open", incorrect_msg = "Pass the correct arguments to `open()`" )

msg = "Make sure to print out the contents of the file like this: `print(file.read())`."
test_function("file.read", incorrect_msg = msg)
test_function("print", 1, args=[], incorrect_msg = msg)
test_function("file.close", not_called_msg = "Make sure to close the file, man!")
success_msg("You aced selecting observations from DataFrames; over to selecting both rows and columns!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)


if __name__ == "__main__":
  unittest.main()
