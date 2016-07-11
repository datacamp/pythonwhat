import unittest
import helper

class TestStudentTypedComment(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
# Just testing division
print(5 / 8)

# Addition works too
print(7 + 10)
''',
      "DC_SOLUTION": '''
# Just testing division
print(5 / 8)

# Addition works too
print(7 + 10)
'''

    }

  def test_success(self):
    self.data["DC_SCT"] = '''
test_student_typed("# (A|a)ddition works to(o?)\sprint\(7", not_typed_msg = "Make sure to add the instructed comment before `print(7+10)`.")
success_msg("You typed the correct comment.")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "You typed the correct comment.")

class TestStudentDidntTypeComment(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
# Just testing division
print(5 / 8)


print(7 + 10)
''',
      "DC_SOLUTION": '''
# Just testing division
print(5 / 8)

# Addition works too
print(7 + 10)
'''

    }

  def test_fail(self):
    self.data["DC_SCT"] = '''
test_student_typed("# (A|a)ddition works to(o?)\sprint\(7", not_typed_msg = "Make sure to add the instructed comment before `print(7+10)`.")
success_msg("You typed the correct comment.")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Make sure to add the instructed comment before <code>print(7+10)</code>.")


