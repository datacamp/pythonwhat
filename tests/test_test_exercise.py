import unittest
from pythonbackend.Exercise import Exercise

class TestTestExerciseError(unittest.TestCase):

	def test_normal_pass(self):
		self.data = {
			"DC_PEC": '#no pec',
			"DC_CODE": 'x = 4',
			"DC_SOLUTION": 'x = 4',
			"DC_SCT": 'test_object("x")\nsuccess_msg("nice")'
		}
		self.exercise = Exercise(self.data)
		self.exercise.runInit()
		output = self.exercise.runSubmit(self.data)
		self.assertEqual(output[0]['type'], 'sct')
		self.assertTrue(output[0]['payload']['correct'])
		self.assertEqual(output[0]['payload']['message'], 'nice')

	def test_normal_fail(self):
		self.data = {
			"DC_PEC": '#no pec',
			"DC_CODE": 'x = 4',
			"DC_SOLUTION": 'x = 6',
			"DC_SCT": 'test_object("x")\nsuccess_msg("nice")'
		}
		self.exercise = Exercise(self.data)
		self.exercise.runInit()
		output = self.exercise.runSubmit(self.data)
		self.assertEqual(output[0]['type'], 'sct')
		self.assertFalse(output[0]['payload']['correct'])

	def test_syntax_error(self):
		self.data = {
			"DC_PEC": '# no pec',
			"DC_CODE": 'print "yolo"',
			"DC_SOLUTION": 'x = 6',
			"DC_SCT": 'test_object("x")'
		}
		self.exercise = Exercise(self.data)
		self.exercise.runInit()
		output = self.exercise.runSubmit(self.data)
		self.assertEqual(output[0]['type'], "error")
		self.assertFalse(output[1]['payload']['correct'])
		self.assertEqual(output[1]['payload']['message'], "Your code can not be executed due to a syntax error:<br><code>Missing parentheses in call to 'print' (script.py, line 1).</code>") 
		self.assertEqual(output[1]['payload']['tags']['fun'], "syntax_error")

	def test_indentation_error(self):
		self.data = {
			"DC_PEC": '# no pec',
			"DC_CODE": '	print("yolo")',
			"DC_SOLUTION": 'x = 6',
			"DC_SCT": 'test_object("x")'
		}
		self.exercise = Exercise(self.data)
		self.exercise.runInit()
		output = self.exercise.runSubmit(self.data)
		self.assertEqual(output[0]['type'], "script-output")
		self.assertFalse(output[1]['payload']['correct'])
		self.assertEqual(output[1]['payload']['message'], "Your code could not be parsed due to an error in the indentation:<br><code>unexpected indent (script.py, line 1).</code>")
		self.assertEqual(output[1]['payload']['tags']['fun'], "indentation_error")

	def test_enrichment_error(self):
		self.data = {
			"DC_PEC": '# no pec',
			"DC_CODE": '',
			"DC_SOLUTION": 'x = 6',
			"DC_SCT": 'test_object("x")'
		}
		self.exercise = Exercise(self.data)
		self.exercise.runInit()
		output = self.exercise.runSubmit(self.data)
		self.assertEqual(output[0]['type'], 'sct')
		self.assertFalse(output[0]['payload']['correct'])
		self.assertFalse('line_start' in output[0]['payload'])
		self.assertFalse('line_end' in output[0]['payload'])
		self.assertFalse('column_start' in output[0]['payload'])
		self.assertFalse('column_end' in output[0]['payload'])

if __name__ == "__main__":
    unittest.main()
