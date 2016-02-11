import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise
from pythonbackend import utils

class TestTestExerciseError(unittest.TestCase):

	def setUp(self):
		self.data = {
			"DC_PEC": '''
# no pec
			''',
			"DC_CODE": '''
print "yolo"
			''',
			"DC_SOLUTION": '''
x = 6
			'''
		}

	def test_standardTestPass(self):
		self.data["DC_SCT"] = '''
test_object("x")
success_msg("Well done!")
		'''
		self.exercise = Exercise(self.data)
		self.exercise.runInit()
		output = self.exercise.runSubmit(self.data)
		self.assertEqual(output[0]['type'], "error")
		self.assertEqual(output[1]['payload']['correct'], False)
		self.assertEqual(output[1]['payload']['message'], "Your code can not be excuted due to a syntax error: Missing parentheses in call to 'print' (<string>, line 2).") 
