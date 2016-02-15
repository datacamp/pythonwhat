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
      "DC_PEC": '''
f = open('cars.csv', "w")
f.write(""",cars_per_cap,country,drives_right
US,809,United States,True
AUS,731,Australia,False
JAP,588,Japan,False
IN,18,India,False
RU,200,Russia,True
MOR,70,Morocco,True
EG,45,Egypt,True""")
f.close()
      ''',
      "DC_CODE": '''
# Import cars data
import pandas as pd
cars = pd.read_csv('cars.csv', index_col = 0)

# Print out observation for Japan
print(cars.loc[0])

# Print out observations for Japan and Egypt
print(cars.loc[['AUS', 'EG']])
      ''',
      "DC_SOLUTION": '''
# Import cars data
import pandas as pd
cars = pd.read_csv('cars.csv', index_col = 0)

# Print out observation for Japan
print(cars.iloc[2])

# Print out observations for Japan and Egypt
print(cars.loc[['AUS', 'EG']])
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
msg = "You don't have to change or remove the predefined `import` statement."
test_import("pandas",
  not_imported_msg = msg,
  incorrect_as_msg = msg)
  
msg = "Don't change or remove the definition for `cars`, it was coded for you."
test_object("cars", undefined_msg = msg, incorrect_msg = msg)

msg = "For the %s printout, use `cars.loc[%s]` or `cars.iloc[%s]` in order to select the correct elements."

msg1 = msg % ("first", "'JAP'", "2")
test_function("print", index = 1, not_called_msg = msg1, incorrect_msg = msg1)

msg2 = msg % ("second", "['AUS', 'EG']", "[1, 6]")
test_function("print", index = 2, not_called_msg = msg2, incorrect_msg = msg2 + " Remember in Python, the first element has index `0`.")

success_msg("You aced selecting observations from DataFrames; over to selecting both rows and columns!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)
    self.assertEqual(sct_payload['message'], "For the first printout, use <code>cars.loc['JAP']</code> or <code>cars.iloc[2]</code> in order to select the correct elements.")

class TestExercise2(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
# Define variables
room = "kit"
area = 14.0

# if statement for room
if room == "kit" :
    print("looking around in the kitchen.")

# if statement for area
if area > 15 :
    print("big place!")
      ''',
      "DC_SOLUTION": '''
# Define variables
room = "kit"
area = 14.0

# if statement for room
if room == "kit" :
    print("looking around in the kitchen.")

# if statement for area
if area > 15 :
  print("big place!")
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
def test():
  msg = "You don't have to change or remove the first `if` statement."
  test_expression_result({"room": "kit"}, incorrect_msg = msg)
  test_expression_result({"room": "not_kit"}, incorrect_msg = msg)

test_if_else(index = 1, test = test)

def test():
  msg = "The second `if` statement should succeed if `area` is greater than `15`."
  test_expression_result({"area": 14}, incorrect_msg = msg)
  test_expression_result({"area": 15}, incorrect_msg = msg)
  test_expression_result({"area": 16}, incorrect_msg = msg)

test_if_else(index = 2, test = test)


success_msg("Great! `big place!` wasn't printed, because `area > 15` is not `True`. Experiment with other values of `room` and `area` to see how the printouts change.")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

class TestExercise3(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''''',
      "DC_CODE": '''
# Define variables
room = "kit"
area = 14.0

# if-else construct for room
if room == "kit" :
    print("looking around in the kitchen.")
else :
    print("looking around elsewhere.")

# if-else construct for area :
if area > 15 :
    print("big place!")
else :
    print("pretty small.")
      ''',
      "DC_SOLUTION": '''
# Define variables
room = "kit"
area = 14.0

# if-else construct for room
if room == "kit" :
    print("looking around in the kitchen.")
else :
    print("looking around elsewhere.")

# if-else construct for area :
if area > 15 :
    print("big place!")
else :
    print("pretty small.")
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
def test_first():
  msg = "You don't have to change or remove anything" # this will automatically be completed with extra info
                                                      # about the if statement
  test_expression_result({"room": "kit"}, incorrect_msg = msg)
  test_expression_result({"room": "not_kit"}, incorrect_msg = msg)

def body_first():
  msg = "You don't have to change or remove anything"
  test_function("print", incorrect_msg = msg)

test_if_else(index = 1, test = test_first, body = body_first, orelse = body_first)

def test_second():
  msg = "The `area` should be greater than `15`" # ...
  test_expression_result({"area": 14}, incorrect_msg = msg)
  test_expression_result({"area": 15}, incorrect_msg = msg)
  test_expression_result({"area": 16}, incorrect_msg = msg)
  
def body_second():
  msg = 'Print out `\"big place!\"`'
  test_function("print", incorrect_msg = msg)

def else_second():
  msg = 'Print out `\"pretty small.\"`'
  test_function("print", incorrect_msg = msg)
  
test_if_else(index = 2, test = test_second, body = body_second, orelse = else_second)

success_msg("Nice! Again, feel free to play around with different values of `room` and `area` some more. Then, head over to the next exercise, where you'll take this customization one step further!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

class TestExercise4(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec here
      ''',
      "DC_CODE": '''
if True:
  print("test")
  print("test 2")
      ''',
      "DC_SOLUTION": '''
if True:
  print("test")
  print("test 2")
      '''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_if_else(1, body = lambda : test_expression_output())
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

class TestExercise4(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec here
      ''',
      "DC_CODE": '''
if True:
  print("test")
  print("test 2")
      ''',
      "DC_SOLUTION": '''
if True:
  print("test")
  print("test 2")
      '''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_if_else(1, body = lambda : test_expression_output())
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)

class TestExercise5(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec here
      ''',
      "DC_CODE": '''
# Import numpy as np
import numpy as np

# Set the seed
np.random.seed(123)

# Generate and print random float
print(np.random.rand())
      ''',
      "DC_SOLUTION": '''
# Import numpy as np
import numpy as np

# Set the seed
np.random.seed(123)

# Generate and print random float
print(np.random.rand())
      '''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
msg = "Have you correctly imported `numpy` as `np`?"
test_import("numpy", not_imported_msg = msg, incorrect_as_msg = msg)

msg = "Have you correctly set the seed to 123? Use `np.random.seed(123)`."
test_function("numpy.random.seed", not_called_msg = msg, incorrect_msg = msg)

msg = "Have you correctly called the `rand()` function? Use `np.random.rand()`, without arguments."
test_function("numpy.random.rand", not_called_msg = msg, incorrect_msg = msg)


test_expression_output(pre_code="import numpy as np; np.random.seed(123)")

msg = "Don't forget to print out the random float you generated with `rand()`."
#test_function("print", args = [], not_called_msg = msg, incorrect_msg = msg)

success_msg("Great! Now let's simulate a dice.")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Great! Now let's simulate a dice.")


class TestExercise6(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec here
      ''',
      "DC_CODE": '''
# Import numpy and set seed
import numpy as np
np.random.seed(123)

# Starting step
step = 50

# Roll the dice
dice = np.random.randint(1,7)

# Finish the control construct
if dice <= 2 :
    step = step - 1
elif dice <= 5 :
    step = step + 1
else :
    step = step + np.random.randint(1,7)

# Print out dice and step
print(dice)
print(step)
      ''',
      "DC_SOLUTION": '''
# Import numpy and set seed
import numpy as np
np.random.seed(123)

# Starting step
step = 50

# Roll the dice
dice = np.random.randint(1,7)

# Finish the control construct
if dice <= 2 :
    step = step - 1
elif dice <= 5 :
    step = step + 1
else :
    step = step + np.random.randint(1,7)

# Print out dice and step
print(dice)
print(step)
      '''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
def else1() :
  def if2() :
    msg = "Have another look at your `elif` part. If the dice is smaller than or equal to 5, and bigger than 2, `step` should be increased by 1."
    test_object_after_expression("step", {"step": 1}, incorrect_msg = msg)

  def else2() :
    msg = "Have another look at your final `else` part. If the dice is 6, `step` should be increased by a random integer between 1 and 6, inclusive. Use `np.random.randint(1,7)`."
    pre = "import numpy as np; np.random.seed(123)"
    test_object_after_expression("step", {"step": 1}, pre_code = pre, incorrect_msg = msg)

  msg = "The condition of the `elif` part should be `dice <= 5`."
  for i in range(1,7):
    test_if_else(1, test = lambda i=i, msg=msg: test_expression_result({"dice": i}, incorrect_msg = msg), expand_message = False)
  test_if_else(1, body = if2, expand_message = False)
  test_if_else(1, orelse = else2, expand_message = False)

msg = "In the condition of your `if` part, make sure you use `dice <= 2`."
for i in range(1,7):
  test_if_else(1, test = lambda msg=msg, i=i: test_expression_result({"dice": i}, incorrect_msg = msg), expand_message = False)

test_if_else(1, orelse = else1, expand_message = False)

msg = "Make sure you output `dice` and `step`, in this order, with two `print()` calls."
test_expression_output(incorrect_msg = msg)

success_msg("Great!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Great!")


class TestExercise7(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec here
      ''',
      "DC_CODE": '''
# Import numpy and set seed
import numpy as np
np.random.seed(123)

# Initialize random_wolk
random_walk = [0]

# Complete the ___
for x in range(100) :
    # Set step: last element in random_walk
    step = random_walk[-1]
  
    # Roll the dice
    dice = np.random.randint(1,7)
  
    # Determine next step
    if dice <= 2:
        step = step - 1
    elif dice <= 5:
        step = step + 1
    else:
        step = step + np.random.randint(1,7)  

    # append next_step to random_walk
    random_walk.append(step)

# Print random_walk
print(random_walk)
      ''',
      "DC_SOLUTION": '''
# Import numpy and set seed
import numpy as np
np.random.seed(123)

# Initialize random_wolk
random_walk = [0]

# Complete the ___
for x in range(100) :
    # Set step: last element in random_walk
    step = random_walk[-1]
  
    # Roll the dice
    dice = np.random.randint(1,7)
  
    # Determine next step
    if dice <= 2:
        step = step - 1
    elif dice <= 5:
        step = step + 1
    else:
        step = step + np.random.randint(1,7)  

    # append next_step to random_walk
    random_walk.append(step)

# Print random_walk
print(random_walk)
      '''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
msg = "Be sure to initialize `random_walk` with: `random_walk = [0]`."
test_expression_result(expr_code = "random_walk[0]", incorrect_msg = msg)

msg = "Loop over `x` in `range(100)` to loop  100 times"
test_for_loop(1, for_iter=lambda msg=msg: test_function("range", not_called_msg = msg, incorrect_msg = msg))

# Check if the student uses the last element of random_walk
msg = "Initialize `step` using `random_walk[-1]`, the last element of `random_walk`,"
test_for_loop(1,
              body = lambda msg=msg: test_expression_result({"random_walk": [1, 2, 3, 4, 1000]}, expr_code = "step >= 900", incorrect_msg = msg))

# For the SCT's below, you can test in IPython Shell that the seeds will lead
# to a value for dice that are: 6 for seed = 1, 1 for seed = 2 and 3 for seed = 3
msg = "If `dice <= 2`, `step` should be `step - 1`"
pre = "import numpy as np; np.random.seed(2)"
test_for_loop(1,
              body = lambda msg=msg, pre=pre: test_object_after_expression("step", {"random_walk": [0]}, pre_code = pre, undefined_msg = msg, incorrect_msg = msg))
msg = "If `dice > 2` and `dice <= 5`, `step` should be `step + 1`"
pre = "import numpy as np; np.random.seed(3)"
test_for_loop(1,
              body = lambda msg=msg, pre=pre: test_object_after_expression("step", {"random_walk": [0]}, pre_code = pre, undefined_msg = msg, incorrect_msg = msg))
msg = "If `dice > 5`, `step` should be `step + np.random.randint(1,7)`"
pre = "import numpy as np; np.random.seed(1)"
test_for_loop(1,
              body = lambda msg=msg, pre=pre: test_object_after_expression("step", {"random_walk": [0]}, pre_code = pre, undefined_msg = msg, incorrect_msg = msg))

msg = "Finally, append `random_walk` with `step` using `.append(step)`"
pre = "import numpy as np; np.random.seed(123)"
test_for_loop(1,
              body = lambda msg=msg, pre=pre: test_object_after_expression("random_walk", {"random_walk": [0]}, pre_code = pre, undefined_msg = msg, incorrect_msg = msg))

success_msg("Great!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Great!")

class TestExercise6(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
# pec here
      ''',
      "DC_CODE": '''
# Initialization
import numpy as np
np.random.seed(123)

# Initialize all_walks
all_walks = []

# Simulate random walk 10 times
for i in range(10) :

    # Code from before
    random_walk = [0]
    for x in range(100) :
        step = random_walk[-1]
        dice = np.random.randint(1,7)
    
        if dice <= 2:
            step = max(0, step - 1)
        elif dice <= 5:
            step = step + 1
        else:
            step = step + np.random.randint(1,7)  
        random_walk.append(step)

    # Append random_walk to all_walks
    all_walks.append(random_walk)
  
# Print all_walks
print(all_walks)
      ''',
      "DC_SOLUTION": '''
# Initialization
import numpy as np
np.random.seed(123)

# Initialize all_walks
all_walks = []

# Simulate random walk 10 times
for i in range(10) :

    # Code from before
    random_walk = [0]
    for x in range(100) :
        step = random_walk[-1]
        dice = np.random.randint(1,7)
    
        if dice <= 2:
            step = max(0, step - 1)
        elif dice <= 5:
            step = step + 1
        else:
            step = step + np.random.randint(1,7)  
        random_walk.append(step)

    # Append random_walk to all_walks
    all_walks.append(random_walk)
  
# Print all_walks
print(all_walks)
      '''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''

msg = "Don't change the predefined code!"
pre = "import numpy as np; np.random.seed(123)"
test_for_loop(1, body = lambda msg=msg, pre=pre: test_object_after_expression("random_walk", pre_code=pre, undefined_msg=msg, incorrect_msg = msg), expand_message = False)
test_import("numpy", not_imported_msg = msg, incorrect_as_msg = msg)
test_function("numpy.random.seed", not_called_msg = msg, incorrect_msg = msg)

msg = "Loop over `i` in `range(10)` to loop 10 times"
test_for_loop(1, for_iter=lambda msg=msg: test_function("range", not_called_msg = msg, incorrect_msg = msg))

msg = "Append `all_walks` with `random_walk` using `.append()`"
pre = "import numpy as np; np.random.seed(123)"
test_for_loop(1, body = lambda msg=msg, pre=pre: test_object_after_expression("all_walks", {"all_walks": []}, pre_code=pre, undefined_msg=msg, incorrect_msg = msg))

msg = "Have you correctly initialized `all_walks` to `[]` and expanded it correctly each loop?"
test_expression_result(expr_code="len(all_walks)", incorrect_msg=msg)

msg = "Don't forget to print out `all_walks`."
test_function("print", args=[], not_called_msg=msg, incorrect_msg=msg)

success_msg("Well done!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)
    self.assertEqual(sct_payload['message'], "Well done!")

if __name__ == "__main__":
  unittest.main()

