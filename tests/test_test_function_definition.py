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
# Define the function shout, which accepts the parameter word
def shout ( word ):

    # Concatenate the '!!!' string to word and assign to shout_word
    shout_word = word + '!!!'

    # Print the value of shout_word
    print( shout_word )

# Call shout, with the string 'help'
shout( 'help' )
      ''',
      "DC_SOLUTION": '''
# Define the function shout, which accepts the parameter word
def shout ( word ):

    # Concatenate the '!!!' string to word and assign to shout_word
    shout_word = word + '!!!'

    # Print the value of shout_word
    print( shout_word )

# Call shout, with the string 'help'
shout( 'help' )
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout",
                         body = lambda: test_expression_output(context_vals = ['help']))
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
# Define the function shout, which accepts the parameter word
def shout ( word ):

    # Concatenate the '!!!' string to word and assign to shout_word
    shout_word = word + '!!!'

    # Print the value of shout_word
    print( shout_word )

# Call shout, with the string 'help'
shout( 'help' )
      ''',
      "DC_SOLUTION": '''
# Define the function shout, which accepts the parameter word
def shout ( word ):

    # Concatenate the '!!!' string to word and assign to shout_word
    shout_word = word + '!!'

    # Print the value of shout_word
    print( shout_word )

# Call shout, with the string 'help'
shout( 'help' )
'''
    }

  def test_Fail(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout",
                         body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'make sure to output the correct string.'))
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "In your definition of <code>shout()</code>, make sure to output the correct string.")

class TestExercise3(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
# Define the function shout, which accepts the parameter word
def shout ( word ):

    # Concatenate the '!!!' string to word and assign to shout_word
    shout_word = word + '!!!'

    # Print the value of shout_word
    print( shout_word )

# Call shout, with the string 'help'
shout( 'help' )
      ''',
      "DC_SOLUTION": '''
# Define the function shout, which accepts the parameter word
def shout ( word, times = None):

    # Concatenate the '!!!' string to word and assign to shout_word
    shout_word = word + '!!!'

    # Print the value of shout_word
    print( shout_word )

# Call shout, with the string 'help'
shout( 'help' )
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout", arg_names=False, arg_defaults=False,
                         body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'make sure to output the correct string.'))
success_msg("Nice work man!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Fail(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout",
                         body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'make sure to output the correct string.'))
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "You should define <code>shout()</code> with 2 arguments, instead got 1.")

class TestExercise4(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
def shout ( word ):
    shout_word = word + '???'
    print( shout_word )
    return word * 2
      ''',
      "DC_SOLUTION": '''
def shout ( word = 'help' ):
    shout_word = word + '!!!'
    print( shout_word )
    return word * 2
'''
    }

  def test_Fail1(self):
    self.data["DC_SCT"] = '''
test_function_definition('shout')
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)

  def test_Pass1(self):
    self.data["DC_SCT"] = '''
test_function_definition('shout', arg_defaults = False)
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Fail2(self):
    self.data["DC_SCT"] = '''
test_function_definition('shout', arg_defaults = False, outputs = [('help')])
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)

  def test_Pass2(self):
    self.data["DC_SCT"] = '''
test_function_definition('shout', arg_defaults = False, results = [('help')])
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

class TestExercise5(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
# Define the function shout, which accepts the parameter word
def shout ( word ):

    # Concatenate the '!!!' string to word and assign to shout_word
    shout_word = word + '!!!'

    # Print the value of shout_word
    print( shout_word )

# Call shout, with the string 'help'
shout( 'help' )
      ''',
      "DC_SOLUTION": '''
# Define the function shout, which accepts the parameter word
def shout ( word, times = None):

    # Concatenate the '!!!' string to word and assign to shout_word
    shout_word = word + '!!!'

    # Print the value of shout_word
    print( shout_word )

# Call shout, with the string 'help'
shout( 'help' )
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout", arg_names=False, arg_defaults=False,
                         body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'make sure to output the correct string.'))
success_msg("Nice work man!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Fail(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout",
                         body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'make sure to output the correct string.'))
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "You should define <code>shout()</code> with 2 arguments, instead got 1.")

if __name__ == "__main__":
  unittest.main()
