import unittest
import helper

class TestTestExerciseError(unittest.TestCase):

	def test_normal_pass(self):
		self.data = {
			"DC_PEC": '#no pec',
			"DC_CODE": 'x = 4',
			"DC_SOLUTION": 'x = 4',
			"DC_SCT": 'test_object("x")\nsuccess_msg("nice")'
		}
		output = helper.run(self.data)
		self.assertTrue(output['correct'])
		self.assertEqual(output['message'], 'nice')

	def test_normal_fail(self):
		self.data = {
			"DC_PEC": '#no pec',
			"DC_CODE": 'x = 4',
			"DC_SOLUTION": 'x = 6',
			"DC_SCT": 'test_object("x")\nsuccess_msg("nice")'
		}
		output = helper.run(self.data)
		self.assertFalse(output['correct'])

	def test_syntax_error(self):
		self.data = {
			"DC_PEC": '# no pec',
			"DC_CODE": 'print "yolo"',
			"DC_SOLUTION": 'x = 6',
			"DC_SCT": 'test_object("x")'
		}
		output = helper.run(self.data)
		self.assertFalse(output['correct'])
		self.assertEqual(output['message'], "Your code can not be executed due to a syntax error:<br><code>Missing parentheses in call to 'print' (script.py, line 1).</code>") 

	def test_indentation_error(self):
		self.data = {
			"DC_PEC": '# no pec',
			"DC_CODE": '	print("yolo")',
			"DC_SOLUTION": 'x = 6',
			"DC_SCT": 'test_object("x")'
		}
		output = helper.run(self.data)
		self.assertFalse(output['correct'])
		self.assertEqual(output['message'], "Your code could not be parsed due to an error in the indentation:<br><code>unexpected indent (script.py, line 1).</code>")

	def test_enrichment_error(self):
		self.data = {
			"DC_PEC": '# no pec',
			"DC_CODE": '',
			"DC_SOLUTION": 'x = 6',
			"DC_SCT": 'test_object("x")'
		}
		output = helper.run(self.data)
		self.assertFalse(output['correct'])
		helper.test_absent_lines(self, output)

if __name__ == "__main__":
    unittest.main()
