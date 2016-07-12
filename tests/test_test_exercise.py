import unittest
from pythonbackend.Exercise import Exercise

class TestTestExerciseError(unittest.TestCase):

	def setUp(self):
		self.data = {
			"DC_PEC": '# no pec',
			"DC_CODE": 'print "yolo"',
			"DC_SOLUTION": 'x = 6'
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
		self.assertEqual(output[1]['payload']['message'], "Your code can not be executed due to a syntax error: Missing parentheses in call to 'print' (<string>, line 1).") 

if __name__ == "__main__":
    unittest.main()
