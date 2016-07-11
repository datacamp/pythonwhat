import unittest
import helper

class TestExercise1(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
# Define the function shout
def shout():

  # Concatenate the strings
  shout_word = 'congratulation' + '!!!'

  # Print shout_word
  print(shout_word)

# Call shout
shout()
      ''',
      "DC_SOLUTION": '''
# Define the function shout
def shout():

    # Concatenate the strings
    shout_word = 'congratulations' + '!!!'

    # Print shout_word
    print(shout_word)

# Call shout
shout()
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Test the value of shout_word
test_function_definition(
    "shout",
    arg_names = False,
    body = lambda: test_object_after_expression(
        "shout_word",
        undefined_msg = "have you defined `shout_word`?",
        incorrect_msg = "test"
    )
)
success_msg("Nice work!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], 'In your definition of <code>shout()</code>, test')

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Test the value of shout_word
test_function_definition(
    "shout",
    arg_names = False,
    body = lambda: test_object_after_expression(
        "shout_word",
        undefined_msg = "have you defined `shout_word`?"
    )
)
success_msg("Nice work!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], 'In your definition of <code>shout()</code>, are you sure you assigned the correct value to <code>shout_word</code>?')

if __name__ == "__main__":
  unittest.main()
