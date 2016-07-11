import os
import unittest

from os.path import exists
from unittest.mock import patch

from pythonbackend.Exercise import Exercise
from pythonbackend import utils

import helper

class TestExercisesd(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
# Addition and subtraction
print(5 + 5)
print(5 - 5)

# Multiplication and division
print(3 * 5)
print(10 / 2)

# Exponentiation
print(4 ** 2)

# Modulo
print(18 % 7)

# How much is your $100 worth after 7 years?
print(100 * 1.1 ** 7)
      ''',
      "DC_SOLUTION": '''
# Addition and subtraction
print(5 + 5)
print(5 - 5)

# Multiplication and division
print(3 * 5)
print(10 / 2)

# Exponentiation
print(4 ** 2)

# Modulo
print(18 % 7)

# How much is your $100 worth after 7 years?
print(100 * 1.1 ** 7)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
msg = "You don't have to change the predefined code. Just add one line at the bottom!"
for i in range(1,7):
  test_operator(i, not_found_msg = msg, incorrect_op_msg = msg, incorrect_result_msg = msg)
for i in range(1,7):
  test_function("print", index = i, not_called_msg = msg, incorrect_msg = msg)

test_operator(7, not_found_msg = "Add an operation to calculate what's instructed.", 
  incorrect_op_msg = "You should use at least one '*' and one '**' operator to calculate what's instructed.",
  incorrect_result_msg = "You should calculate the total intrest on 100 dollar after 7 years given a 10\% rate.")
test_function("print", index = 7)

success_msg("Time for another video!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Time for another video!")


class TestExercise2(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
# Create a variable savings
savings = 100

# Print out savings
print(savings)
      ''',
      "DC_SOLUTION": '''
# Create a variable savings
savings = 100

# Print out savings
print(savings)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_object("savings")
test_function("print")
success_msg("Great! Let's try to do some calculations with this variable now!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Great! Let's try to do some calculations with this variable now!")

class TestExercise3(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
# Create a variable savings
savings = 100

# Create a variable factor
factor = 1.1

# Calculate result
result = savings * factor ** 7

# Print out result
print(result)
      ''',
      "DC_SOLUTION": '''
# Create a variable savings
savings = 100

# Create a variable factor
factor = 1.1

# Calculate result
result = savings * factor ** 7

# Print out result
print(result)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_object("savings")
test_object("factor")
test_object("result", do_eval = False)
test_operator(3, not_found_msg = "Have you used the correct calculations to calculate result?",
                 incorrect_op_msg = "Use '*' and '**' to calculate result.",
                 incorrect_result_msg = "Have you used to correct variables to calculate result?")
test_object("result", incorrect_msg = "Assign the correct value to result.")
test_function("print")
success_msg("Awesome! If you now change the value of `savings` and submit your script again, `result` will change as well.")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Awesome! If you now change the value of <code>savings</code> and submit your script again, <code>result</code> will change as well.")


class TestExercise4(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''

# Create a variable desc
desc = "compound interest"

# Create a variable profitable
profitable = True

      ''',
      "DC_SOLUTION": '''

# Create a variable desc
desc = "compound interest"

# Create a variable profitable
profitable = True
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_object("desc")
test_object("profitable")

success_msg("Nice!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Nice!")

class TestExercise5(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
# Several variables to experiment with
savings = 100
factor = 1.1
desc = "compound interest"

# Assign product of savings and factor to year1
year1 = savings * factor

# Print the type of year1
print(type(year1))

# Assign sum of desc and desc to doubledesc
doubledesc = desc + desc

# Print out doubledesc
print(doubledesc)

      ''',
      "DC_SOLUTION": '''
# Several variables to experiment with
savings = 100
factor = 1.1
desc = "compound interest"

# Assign product of savings and factor to year1
year1 = savings * factor

# Print the type of year1
print(type(year1))

# Assign sum of desc and desc to doubledesc
doubledesc = desc + desc

# Print out doubledesc
print(doubledesc)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_object("savings")
test_object("factor")
test_object("desc")

test_object("year1", do_eval = False)
test_operator(3)
test_object("year1")

test_function("type")
test_function("print")

test_object("doubledesc", do_eval = False)
test_operator(4)
test_object("doubledesc")

test_function("print", 2)
success_msg("Nice. Notice how `desc + desc` causes the strings to be pasted together.")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Nice. Notice how `desc + desc` causes the strings to be pasted together.")

class TestExercise5(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
savings = 100
result = 100 * 1.10 ** 7

# Fix the printout
print("I started with $" + str(savings) + " and now have $" + str(result) + ". Awesome!")

# Definition of pi_string
pi_string = "3.1415926"

# Convert pi_string into float: pi_float
pi_float = float(pi_string)
      ''',
      "DC_SOLUTION": '''

# Definition of savings and result
savings = 100
result = 100 * 1.10 ** 7

# Fix the printout
print("I started with $" + str(savings) + " and now have $" + str(result) + ". Awesome!")

# Definition of pi_string
pi_string = "3.1415926"

# Convert pi_string into float: pi_float
pi_float = float(pi_string)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_object("savings")
test_object("result")

test_function("print")

test_object("pi_string")
test_object("pi_float")

success_msg("Great! You have a profit of around \$95, that's pretty awesome indeed!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Great! You have a profit of around \$95, that's pretty awesome indeed!")

class TestExercise6(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''

# area variables (in square meters)
hallway = 11.25
kitchen = 18.0
living = 20.0
bedroom = 10.75
bathroom = 9.50

# Create list areas
areas = [hallway, kitchen, living, bedroom, bathroom]

# Print areas
print(areas)
      ''',
      "DC_SOLUTION": '''
# area variables (in square meters)
hallway = 11.25
kitchen = 18.0
living = 20.0
bedroom = 10.75
bathroom = 9.50

# Create list areas
areas = [hallway, kitchen, living, bedroom, bathroom]

# Print areas
print(areas)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
msg = "Don't remove or edit the predefined variables!"
test_object("hallway", undefined_msg = msg, incorrect_msg = msg)
test_object("kitchen", undefined_msg = msg, incorrect_msg = msg)
test_object("living", undefined_msg = msg, incorrect_msg = msg)
test_object("bedroom", undefined_msg = msg, incorrect_msg = msg)
test_object("bathroom", undefined_msg = msg, incorrect_msg = msg)

test_object("areas", incorrect_msg = "Define `areas` as the list containing all the area variables, in the correct order.")

test_function("print")

success_msg("Nice! A list is way better here, isn't it?")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Nice! A list is way better here, isn't it?")

class TestExercise7(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''

# Definition of radius
r = 0.43

# Import the math package
import math

# Calculate C
C = 2 * r * math.pi 

# Calculate A
A = math.pi * r ** 2

# Build printout
print("Circumference: " + str(C))
print("Area: " + str(A))
      ''',
      "DC_SOLUTION": '''

# Definition of radius
r = 0.43

# Import the math package
import math

# Calculate C
C = 2 * r * math.pi 

# Calculate A
A = math.pi * r ** 2

# Build printout
print("Circumference: " + str(C))
print("Area: " + str(A))
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_import("math")
success_msg("Nice!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Nice!")

class TestExercise8(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Use append twice to add poolhouse and garage size
areas.append(24.5)
areas.append(15.45)

# Print out areas
print(areas)

# Reverse the orders of the elements in areas
areas.reverse()

# Print out areas
print(areas)
      ''',
      "DC_SOLUTION": '''
areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Use append twice to add poolhouse and garage size
areas.append(24.5)
areas.append(15.45)

# Print out areas
print(areas)

# Reverse the orders of the elements in areas
areas.reverse()

# Print out areas
print(areas)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_function("areas.append")
success_msg("Nice!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Nice!")

class TestExercise9(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
      ''',
      "DC_CODE": '''
# Several variables to experiment with
savings = 100
factor = 1.1
desc = "compound interest"

      ''',
      "DC_SOLUTION": '''
# Several variables to experiment with
savings = 100
factor = 1.1
desc = "compound interest"

# Assign product of savings and factor to year1
year1 = savings * factor

# Print the type of year1
print(type(year1))

# Assign sum of desc and desc to doubledesc
doubledesc = desc + desc

# Print out doubledesc
print(doubledesc)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
msg = "You don't have to change or remove the predefined variables."
test_object("savings", undefined_msg = msg, incorrect_msg = msg)
test_object("factor", undefined_msg = msg, incorrect_msg = msg)
test_object("desc", undefined_msg = msg, incorrect_msg = msg)


test_operator(3, not_found_msg = "Calculate `year1` using the `*` operator.",
                 incorrect_op_msg = "To calculate `year1`, you should use `*` once.",
                 incorrect_result_msg = "You should use `savings` and `factor` to calculate `year1`. Take a look at the hint if you're stuck.")
test_object("year1", incorrect_msg = "Assign the correct value you calculated to `year1`.")

msg = "Make sure to print out the type of `year1` like this: `print(type(year1))`."
test_function("type", incorrect_msg = msg)
test_function("print", 1, incorrect_msg = msg)

msg = "You can add up a string to another string, just type `desc + desc`."
test_operator(4, not_found_msg = msg, incorrect_op_msg = msg, incorrect_result_msg = msg)
test_object("doubledesc", incorrect_msg  = "Assign the resulting string to `doubledesc`.")

test_function("print", 2, incorrect_msg = "Be sure to print out `double_desc`.")
success_msg('Nice. Notice how `desc + desc` causes `"compound interest"` and `"compound interest"` to be pasted together.')
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Calculate <code>year1</code> using the <code>*</code> operator.")

class TestExercise10(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec comes here
import pandas as pd
np_baseball = pd.read_csv("http://s3.amazonaws.com/assets.datacamp.com/course/intro_to_python/baseball.csv")[['Height', 'Weight', 'Age']].as_matrix()
import numpy as np
      ''',
      "DC_CODE": '''
# np_baseball is available

# Import numpy
import numpy as np

# Print mean height (first column)
avg = np.mean(np_baseball[:,0])
print("Average: " + str(avg))

# Print median height. Replace 'None'
med = np.median(np_baseball[:,0])
print("Median: " + str(med))

# Print out the standard deviation on height. Replace 'None'
stddev = np.std(np_baseball[:,0])
print("Standard Deviation: " + str(stddev))

# Print out correlation between first and second column. Replace 'None'
corr = np.corrcoef(np_baseball[:,0:2], rowvar = False) 
print("Correlation: " + str(corr))

year = 1
if year > 5:
  print("test")
      ''',
      "DC_SOLUTION": '''
# np_baseball is available

# Import numpy
import numpy as np

# Print mean height (first column)
avg = np.mean(np_baseball[:,0])
print("Average: " + str(avg))

# Print median height. Replace 'None'
med = np.median(np_baseball[:,0])
print("Median: " + str(med))

# Print out the standard deviation on height. Replace 'None'
stddev = np.std(np_baseball[:,0])
print("Standard Deviation: " + str(stddev))

# Print out correlation between first and second column. Replace 'None'
corr = np.corrcoef(np_baseball[:,0], np_baseball[:,1])
print("Correlation: " + str(corr))

year = 1
if year > 10:
  print("test")
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_import("numpy")

msg = "You don't have to change or remove the predefined variables."
test_object("avg", undefined_msg = msg, incorrect_msg = msg)
test_function("print", 1, not_called_msg = msg, incorrect_msg = msg)

test_function("numpy.median", 1, not_called_msg = "Don't forget to call [`np.median()`](http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.median.html).", incorrect_msg = "To assign `med`, use [`np.median()`](http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.median.html). Make sure to pass it the correct column of `np_baseball`.")
test_object("med")
test_function("print", 2, not_called_msg = msg, incorrect_msg = msg)

test_function("numpy.std", 1, not_called_msg = "Don't forget to call [`np.std()`](http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.std.html).", incorrect_msg = "To assign `stddev`, use [`np.std()`](http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.std.html). Make sure to pass it the correct column of `np_baseball`.")
test_object("stddev")
test_function("print", 3, not_called_msg = msg, incorrect_msg = msg)

test_function("numpy.corrcoef", 1, args = [], keywords = [], not_called_msg = "Don't forget to call [`np.corrcoef()`](http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.corrcoef.html).")
test_object("corr", incorrect_msg = "To assign `corr`, use [`np.corrcoef()`](http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.corrcoef.html). Make sure to pass it the correct columns of `np_baseball`. You have to pass it two columns.")
test_function("print", 4, not_called_msg = msg, incorrect_msg = msg)

test_if_else(1, lambda: test_expression_result({"year": 6}, incorrect_msg = "Test if `year > 10`"))

success_msg("Great! Time to use all of your new data science skills in the last exercise!")
    '''
    sct_payload = helper.run(self.data)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "Test if <code>year &gt; 10</code> in the condition of the <code>if</code> statement on line 24.")


if __name__ == "__main__":
    unittest.main()


