import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise

import helper

class TestExercise1(unittest.TestCase):
    def setUp(self):
        self.data = {
          "DC_PEC": '''''',
          "DC_SCT": '''
test_or(lambda: test_function('print'), lambda: test_object('test'))
          ''',
          "DC_SOLUTION": '''
print('test')
test = 3
    '''
        }

    def test_Pass1(self):
        self.data["DC_CODE"] = '''
test = 3
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], True)

    def test_Pass2(self):
        self.data["DC_CODE"] = '''
print('test')
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], True)

    def test_Pass3(self):
        self.data["DC_CODE"] = '''
test = 3
print('test')
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], True)

    def test_Pass4(self):
        self.data["DC_CODE"] = '''
test = 4
print('test')
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], True)

    def test_Pass4(self):
        self.data["DC_CODE"] = '''
test = 3
print('not test')
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], True)

    def test_Fail1(self):
        self.data["DC_CODE"] = '''
test = 4
print('not test')
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Did you call <code>print()</code> with the correct arguments? Call on line 3 has wrong arguments. The first argument seems to be incorrect. Expected <code>'test'</code>, but got <code>'not test'</code>.")

if __name__ == "__main__":
    unittest.main()
