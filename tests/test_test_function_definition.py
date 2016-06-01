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
def shout ( word, times = 3 ):
    shout_word = word + '???'
    print( shout_word )
    return word * times
      ''',
      "DC_SOLUTION": '''
def shout ( word = 'help', times = 3 ):
    shout_word = word + '!!!'
    print( shout_word )
    return word * times
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
test_function_definition('shout', arg_defaults = False, outputs = [('help')], wrong_output_msg = "WRONG")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "WRONG")

  def test_Pass2(self):
    self.data["DC_SCT"] = '''
test_function_definition('shout', arg_defaults = False, results = [('help')])
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Pass3(self):
    self.data["DC_SCT"] = '''
test_function_definition('shout', arg_defaults = False, body = lambda: test_function('print', args=[]))
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
# Define the function shout, which accepts the parameters word1 and word2
def shout (word1, word2):

    # Concatenate the string '!!!' to word1 and assign to shout1
    shout1 = word1 + '!!!'

    # Concatenate the string '!!!' to word2 and assign to shout2
    shout2 = word2 + '!!!'

    # Concatenate word2 to word1 and assign to new_shout
    new_shout = word1 + word2

    # Return new_shout
    return new_shout

# Call shout with the strings 'help' and 'fire' and assign the result to yell
yell = shout('help', 'fire')

# Print the value of yell
print(yell)
      ''',
      "DC_SOLUTION": '''
# Define the function shout, which accepts the parameters word1 and word2
def shout (word1, word2):

    # Concatenate the string '!!!' to word1 and assign to shout1
    shout1 = word1 + '!!!'

    # Concatenate the string '!!!' to word2 and assign to shout2
    shout2 = word2 + '!!!'

    # Concatenate word2 to word1 and assign to new_shout
    new_shout = word1 + word2

    print(new_shout)

    # Return new_shout
    return new_shout

# Call shout with the strings 'help' and 'fire' and assign the result to yell
yell = shout('help', 'fire')

# Print the value of yell
print(yell)
'''
    }

  def test_Pass1(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout")
success_msg("Nice work man!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Pass2(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout", results=[('help', 'fire')])
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Fail1(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout", outputs=[('help', 'fire')])
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Calling <code>shout('help', 'fire')</code> should output <code>helpfire</code>, instead got ``.")

  class TestExercise5(unittest.TestCase):

    def setUp(self):
      self.data = {
        "DC_PEC": '''''',
        "DC_CODE": '''
  # Define the function shout, which accepts the parameters word1 and word2
  def shout (word1, word2):

      # Concatenate the string '!!!' to word1 and assign to shout1
      shout1 = word1 + '!!!'

      # Concatenate the string '!!!' to word2 and assign to shout2
      shout2 = word2 + '!!!'

      # Concatenate word2 to word1 and assign to new_shout
      new_shout = word1 + word2

      # Return new_shout
      return new_shout

  # Call shout with the strings 'help' and 'fire' and assign the result to yell
  yell = shout('help', 'fire')

  # Print the value of yell
  print(yell)
        ''',
        "DC_SOLUTION": '''
  # Define the function shout, which accepts the parameters word1 and word2
  def shout (word1, word2, word3 = "nothing"):

      # Concatenate the string '!!!' to word1 and assign to shout1
      shout1 = word1 + '!!!'

      # Concatenate the string '!!!' to word2 and assign to shout2
      shout2 = word2 + '!!!'

      # Concatenate word2 to word1 and assign to new_shout
      new_shout = word1 + word2

      print(new_shout)

      # Return new_shout
      return new_shout

  # Call shout with the strings 'help' and 'fire' and assign the result to yell
  yell = shout('help', 'fire')

  # Print the value of yell
  print(yell)
  '''
      }

    def test_Fail1(self):
      self.data["DC_SCT"] = '''
  test_function_definition("pout", not_called_msg = 'bad luck!')
  success_msg("Nice work man!")
      '''
      self.exercise = Exercise(self.data)
      self.exercise.runInit()
      output = self.exercise.runSubmit(self.data)
      sct_payload = helper.get_sct_payload(output)
      self.assertEqual(sct_payload['correct'], False)
      self.assertEqual(sct_payload['message'], 'bad luck!')

    def test_Fail2(self):
      self.data["DC_SCT"] = '''
  test_function_definition("shout", arg_names_msg = "not good")
  success_msg("Nice work!")
      '''
      self.exercise = Exercise(self.data)
      self.exercise.runInit()
      output = self.exercise.runSubmit(self.data)
      sct_payload = helper.get_sct_payload(output)
      self.assertEqual(sct_payload['correct'], False)
      self.assertEqual(sct_payload['message'], 'not good')

    def test_Fail2(self):
      self.data["DC_SCT"] = '''
  test_function_definition("shout", arg_defafults = False, arg_names_msg = "not good", arg_defaults_msg = "Not good at all")
  success_msg("Nice work!")
      '''
      self.exercise = Exercise(self.data)
      self.exercise.runInit()
      output = self.exercise.runSubmit(self.data)
      sct_payload = helper.get_sct_payload(output)
      self.assertEqual(sct_payload['correct'], False)
      self.assertEqual(sct_payload['message'], 'Not good at all')


class TestExercise6(unittest.TestCase):
  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
# Define the function shout, which accepts the parameters word1 and word2
def shout (word1, word2):

    # Concatenate the string '!!!' to word1 and assign to shout1
    shout1 = word1 + '!!!'

    # Concatenate the string '!!!' to word2 and assign to shout2
    shout2 = word2 + '!!!'

    # Concatenate word2 to word1 and assign to new_shout
    new_shout = word1 + word2

    # Return new_shout
    return new_shout

# Call shout with the strings 'help' and 'fire' and assign the result to yell
yell = shout('help', 'fire')

# Print the value of yell
print(yell)
      ''',
      "DC_SOLUTION": '''
# Define the function shout, which accepts the parameters word1 and word2
def shout (word1, word2):

    # Concatenate the string '!!!' to word1 and assign to shout1
    shout1 = word1 + '!!!'

    # Concatenate the string '!!!' to word2 and assign to shout2
    shout2 = word2 + '!!!'

    # Concatenate word2 to word1 and assign to new_shout
    new_shout = word1 + word2

    print(new_shout)

    # Return new_shout
    return new_shout

# Call shout with the strings 'help' and 'fire' and assign the result to yell
yell = shout('help', 'fire')

# Print the value of yell
print(yell)
'''
    }

  def test_Pass1(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout")
success_msg("Nice work man!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Pass2(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout", results=[('help', 'fire')])
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Fail1(self):
    self.data["DC_SCT"] = '''
test_function_definition("shout", outputs=[('help', 'fire')])
success_msg("Nice work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Calling <code>shout('help', 'fire')</code> should output <code>helpfire</code>, instead got ``.")


class TestExercise7(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_SOLUTION": '''
def to_decimal(number, base = 2):
  print("Converting %d from base %s to base 10" % (number, base))
  number_str = str(number)
  number_range = range(len(number_str))
  multipliers = [base ** ((len(number_str) - 1) - i) for i in number_range]
  decimal = sum([int(number_str[i]) * multipliers[i] for i in number_range])
  return decimal
      ''',
      "DC_SCT": '''
test_function_definition("to_decimal", arg_defaults = True, arg_names = False)
test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
  results = [
      (1001101, 2),
      (1212357, 8)]
)
test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
  outputs = [
      (1234, 6),
      (8888888, 9)]
)
test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
  body = lambda: test_function("sum", args = [], incorrect_msg = "you should use the `sum()` function."))
'''
    }

  def test_Fail1(self):
    self.data["DC_CODE"] = '''
def to_decimal(number, base = 3):
  print("Converting %d from base %s to base 10" % (number, base))
  number_str = str(number)
  number_range = range(len(number_str))
  multipliers = [base ** ((len(number_str) - 1) - i) for i in number_range]
  decimal = sum([int(number_str[i]) * multipliers[i] for i in number_range])
  return decimal
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], 'In your definition of <code>to_decimal()</code>, the 2nd argument should have <code>2</code> as default, instead got <code>3</code>.')


  def test_Fail2(self):
    self.data["DC_CODE"] = '''
from numpy import sum
def to_decimal(number, base = 2):
  print("Converting %d from base %s to base 10" % (number, base))
  number_str = str(number)
  number_range = range(len(number_str))
  multipliers = [base ** ((len(number_str) - 1) - i) for i in number_range]
  decimal = sum([int(number_str[i]) * multipliers[i] for i in number_range])
  return decimal
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

class TestExercise8(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_SOLUTION": '''
# Define the function shout
def shout():

    # Concatenate the string 'congratulations' to '!!!' and assign to shout_word
    shout_word = 'congratulations' + '!!!'

    # Print the value of shout_word
    print(shout_word)

# Call the shout function
shout()
      ''',
      "DC_SCT": '''
# Test the value of shout_word
test_function_definition(
    "shout",
    arg_names = False,
    body = lambda: test_object_after_expression("shout_word"))

'''
    }

  def test_Pass(self):
    self.data["DC_CODE"] = '''
# Define the function shout
def shout():

    # Concatenate the string 'congratulations' to '!!!' and assign to shout_word
    shout_word = 'congratulations' + '!!!'

    # Print the value of shout_word
    print(shout_word)

# Call the shout function
shout()
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

  def test_Fail1(self):
    self.data["DC_CODE"] = '''
# Define the function shout
def shout():

    # Concatenate the string 'congratulations' to '!!!' and assign to shout_word
    shout_word = 'congratulations' + '!!'

    # Print the value of shout_word
    print(shout_word)

# Call the shout function
shout()
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], 'In your definition of <code>shout()</code>, are you sure you assigned the correct value to <code>shout_word</code>?')


class TestExercise9(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_SOLUTION": '''
# Define the function shout, which accepts the parameter word
def shout(word):

    # Concatenate the string in word with '!!!' and assign to shout_word
    shout_word = word + '!!!'

    # Print the value of shout_word
    print(shout_word)

# Call the shout function, with the string 'congratulations'
shout('congratulations')
      ''',
      "DC_SCT": '''
# The sct section defines the Submission Correctness Tests (SCTs) used to
# evaluate the student's response. All functions used here are defined in the
# pythonwhat Python package. Documentation can also be found at github.com/datacamp/pythonwhat/wiki

# Note [FRANCIS]: Tests appear code-level, that is, as they appear top-down in the code.

# Test definition of shout()
test_function_definition("shout", arg_names = True)

# Test the value of word
test_function_definition(
    "shout",
    arg_names = False,
    body = lambda: test_object_after_expression("word", context_vals = ["congratulations"])
)

# Test the value of shout_word
test_function_definition(
    "shout",
    arg_names = False,
    body = lambda: test_object_after_expression("shout_word", context_vals = ["congratulations!!!"])
)

# Test the print() call
test_function_definition("shout", arg_names = False, arg_defaults = False, # Already tested this
    body = lambda: [
      set_extra_env(extra_env={'shout_word': "congratulations"}),
      test_function("print", incorrect_msg = "you should use the `print()` function with the correct argument.")])


test_function_definition("shout", arg_names = False, arg_defaults = False,
  outputs = [('congratulations!!!')])

# Test if shout() is called
test_function("shout")

# Test the output
test_output_contains("congratulations!!!", pattern = False)

success_msg("Great work!")
'''
    }

  def test_Fail1(self):
    self.data["DC_CODE"] = '''
# Define the function shout, which accepts the parameter word
def shout(word):

    # Concatenate the string in word with '!!!' and assign to shout_word
    shout_word = word + '!!!'

    # Print the value of shout_word
    print(shout_word + '!')

# Call the shout function, with the string 'congratulations'
shout('congratulations')
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], 'In your definition of <code>shout()</code>, you should use the <code>print()</code> function with the correct argument.')

class TestExercise9(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_SOLUTION": '''
# Define the function shout
def shout():

    # Concatenate the strings
    shout_word = 'congratulations' + '!!!'

    # Print shout_word
    print(shout_word)

# Call shout
shout()
      ''',
      "DC_SCT": '''
# The sct section defines the Submission Correctness Tests (SCTs) used to
# evaluate the student's response. All functions used here are defined in the
# pythonwhat Python package. Documentation can also be found at github.com/datacamp/pythonwhat/wiki

# Note [FRANCIS]: Tests appear code-level, that is, as they appear top-down in the code.

# Test definition of shout()
test_function_definition("shout", arg_names = True)

# Test the value of shout_word
test_function_definition(
    "shout",
    arg_names = False,
    body = lambda: test_object_after_expression("shout_word"))

# Test the print() call
test_function_definition(
    "shout",
    arg_names = False,
    arg_defaults = False, # Already tested this
    # args argument of test_function doesn't work yet within test_function_definition
    body = lambda: test_function("print", args = [], incorrect_msg = "you should use the `print()` function."))

# Test the output of shout_word
test_function_definition(
    "shout",
    arg_names = False,
    arg_defaults = False,
    outputs = [()],
    wrong_output_msg = "be sure to print out `shout_word`.")

# Test if shout() is called
test_function("shout")

# Test the output
test_output_contains("congratulations!!!", pattern = False)

success_msg("Great work!")
      '''
    }

  def test_Fail1(self):
    self.data["DC_CODE"] = '''
    # Define the function shout
def shout():

    # Concatenate the strings
    shout_word = 'congratulations' + '!!'

    # Print shout_word
    print(shout_word)

# Call shout
shout()
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], 'In your definition of <code>shout()</code>, are you sure you assigned the correct value to <code>shout_word</code>?')



if __name__ == "__main__":
  unittest.main()
