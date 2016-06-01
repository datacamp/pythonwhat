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
with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readline())
    print('test')

# # The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# # Print out these rows
with open('moby_dick.txt') as file:
    for i, row in enumerate(file):
        if i in I:
            print(row)
      ''',
      "DC_SOLUTION": '''
# # Read & print the first 3 lines
with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readline())
    print(file.readline())

# # The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# # Print out these rows
with open('moby_dick.txt') as file:
    for i, row in enumerate(file):
        if i in I:
            print(row)
'''
    }

  def test_Fail1(self):
    self.data["DC_SCT"] = '''
test_with(1, body = lambda: [test_function('print') for _ in range(3)])
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertIn("Check the body of the <code>with</code> statement on line 3.", sct_payload['message'])

  def test_Fail2(self):
    self.data["DC_SCT"] = '''
test_with(1, body = lambda: [test_function('print') for _ in range(3)], expand_message = False)
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertNotIn("Check the body of the <code>with</code> statement on line 3.", sct_payload['message'])

  def test_Pass1(self):
    self.data["DC_SCT"] = '''
test_with(2, body = lambda: test_for_loop(1, body = lambda: test_if_else(1, body = lambda: test_function('print'))))
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

class TestExercise2(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
# # Read & print the first 3 lines
with open('moby_dick.txt') as file, open('moby_dick.txt'):
    print(file.readline())
    print(file.readline())
    print('test')

# # The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# # Print out these rows
with open('moby_dick.txt') as not_file:
    for i, row in enumerate(not_file):
        if i in I:
            print(row)
      ''',
      "DC_SOLUTION": '''
# # Read & print the first 3 lines
with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readline())
    print(file.readline())

# # The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# # Print out these rows
with open('moby_dick.txt') as file:
    for i, row in enumerate(file):
        if i in I:
            print(row)
'''
    }

  def test_Fail1(self):
    self.data["DC_SCT"] = '''
test_with(1, context_vals=True)
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "In your <code>with</code> statement on line 3, make sure to use the correct number of context variables. It seems you defined too many.")

  def test_Fail2(self):
    self.data["DC_SCT"] = '''
test_with(2, context_vals=True)
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "In your <code>with</code> statement on line 12, make sure to use the correct context variable names. Was expecting <code>file</code> but got <code>not_file</code>.")

class TestExercise3(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
# # Read & print the first 3 lines
with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readline())
    print('test')

# # The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# # Print out these rows
with open('moby_dick.txt') as not_file, open('moby_dick.txt') as file:
    for i, row in enumerate(not_file):
        if i in I:
            print(row)
      ''',
      "DC_SOLUTION": '''
# # Read & print the first 3 lines
with open('moby_dick.txt') as file,  open('moby_dick.txt'):
    print(file.readline())
    print(file.readline())
    print(file.readline())

# # The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# # Print out these rows
with open('moby_dick.txt') as file, open('not_moby_dick.txt') as not_file:
    for i, row in enumerate(file):
        if i in I:
            print(row)
'''
    }

  def test_Fail1(self):
    self.data["DC_SCT"] = '''
test_with(1, context_tests=lambda: test_function('open'))
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Fail2(self):
    self.data["DC_SCT"] = '''
test_with(1, context_tests=[
  lambda: test_function('open'),
  lambda: test_function('open')])
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "In your <code>with</code> statement on line 3, make sure to use the correct number of context variables. It seems you defined too little.")

  def test_Fail3(self):
    self.data["DC_SCT"] = '''
test_with(2, context_tests=[
  lambda: test_function('open'),
  lambda: test_function('open')])
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Check the 2nd context in the <code>with</code> statement on line 12. Did you call <code>open()</code> with the correct arguments? Call on line 12 has wrong arguments. The 1st argument seems to be incorrect. Expected <code>'not_moby_dick.txt'</code>, but got <code>'moby_dick.txt'</code>.")


if __name__ == "__main__":
  unittest.main()
