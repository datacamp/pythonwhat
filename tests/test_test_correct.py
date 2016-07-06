import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise

import helper

class TestExercise1(unittest.TestCase):
    def setUp(self):
        self.data = {
          "DC_PEC": '''
import numpy as np
          ''',
          "DC_SCT": '''
test_correct(lambda: test_object('test'), lambda: test_function('numpy.sum'))
          ''',
          "DC_SOLUTION": '''
test = np.sum([5, 2, 4, 9])
    '''
        }

    def test_Pass1(self):
        self.data["DC_CODE"] = '''
test = np.sum([5, 2, 4, 9])
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], True)

    def test_Pass2(self):
        self.data["DC_CODE"] = '''
test = 20
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], True)

    def test_Pass2(self):
        self.data["DC_CODE"] = '''
test = np.sum([5, 2, 4, 4, 5])
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], True)

    def test_Fail1(self):
        self.data["DC_CODE"] = '''
test = 19
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], 'Make sure you call <code>np.sum()</code>.')


    def test_Fail2(self):
        self.data["DC_CODE"] = '''
test = np.sum([5, 2, 3])
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], 'Did you call <code>np.sum()</code> with the correct arguments? Call on line 2 has wrong arguments. The 1st argument seems to be incorrect. Expected <code>[5, 2, 4, 9]</code>, but got <code>[5, 2, 3]</code>.')

    def test_Fail3(self):
        self.data["DC_SCT"] = '''
test_correct(lambda: test_object('test'), lambda: test_function('numpy.sum', args=[]))
        '''
        self.data["DC_CODE"] = '''
test = np.sum([5, 2, 3])
        '''
        self.exercise = Exercise(self.data)
        self.exercise.runInit()
        output = self.exercise.runSubmit(self.data)
        sct_payload = helper.get_sct_payload(output)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], 'Are you sure you assigned the correct value to <code>test</code>?')

if __name__ == "__main__":
    unittest.main()
