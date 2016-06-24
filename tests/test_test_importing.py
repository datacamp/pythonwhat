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
      ''',
      "DC_CODE": '''
# Open a file
file = open('moby_dick.txt' , 'r') # 'r' is to read only.

# Print it
print(file.read())

# Check whether file is closed
print(file.closed)

# Close file
file.close()

# Check whether file is closed
print(file.closed)
      ''',
      "DC_SOLUTION": '''
# Open a file
file = open('moby_dick.txt' , 'r') # 'r' is to read only.

# Print it
print(file.read())

# Check whether file is closed
print(file.closed)

# Close file
file.close()

# Check whether file is closed
print(file.closed)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
test_function("open", incorrect_msg = "Pass the correct arguments to `open()`" )

msg = "Make sure to print out the contents of the file like this: `print(file.read())`."
test_function("file.read", incorrect_msg = msg)
test_function("print", 1, args=[], incorrect_msg = msg)
test_function("file.close", not_called_msg = "Make sure to close the file, man!")
success_msg("You aced selecting observations from DataFrames; over to selecting both rows and columns!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)


class TestExercise2(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
      ''',
      "DC_CODE": '''
# Import necessary module
from sqlalchemy import create_engine

# Create engine: engine
engine = create_engine('sqlite:///Chinook.sqlite')
      ''',
      "DC_SOLUTION": '''
# Import necessary module
from sqlalchemy import create_engine

# Create engine: engine
engine = create_engine('sqlite:///Chinook.sqlite')
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Test: import sqlalchemy
import_msg = "Did you correctly import the required package?"
test_import("sqlalchemy.create_engine", not_imported_msg = import_msg, incorrect_as_msg = import_msg)

# Test: call to create_engine() and 'engine' variable
test_object("engine", do_eval = False)
test_function("create_engine")

success_msg("Awesome!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)


class TestExercise3(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
      ''',
      "DC_CODE": '''
# Import pandas
import pandas as pd

file = 'cars.csv'

# Read the file into a dataframe: data
data = pd.read_csv(file)

# View the head of the dataframe
print(data.head())
      ''',
      "DC_SOLUTION": '''
# Import pandas
import pandas as pd

file = 'cars.csv'

# Read the file into a dataframe: data
data = pd.read_csv(file)

# View the head of the dataframe
print(data.head())
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Test: import pandas as pd
import_msg = "Did you import `pandas` correctly?"
test_import("pandas", same_as = True, not_imported_msg = import_msg, incorrect_as_msg = import_msg)

# Test: Predefined code
predef_msg = "You don't have to change any of the predefined code."
test_object("file", undefined_msg = predef_msg, incorrect_msg = predef_msg)

# [6-13-2016: UPDATE WHEN PYTHONWHAT HAS BEEN FIXED]
# Test: call to pd.read_csv() and 'data' variable
test_correct(
    lambda: test_object("data"),
    lambda: test_function("pandas.read_csv")
)

# Test: print() statement and call to head()
type_msg = "Print out the head of the dataframe as follows: `print(data.head())`."
test_function("data.head", incorrect_msg = type_msg)
test_function("print", incorrect_msg = type_msg)

success_msg("Good job!")
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
      ''',
      "DC_CODE": '''
# Import pandas
import pandas as pd

# Assign spreadsheet filename: file
file = 'battledeath.xlsx'

# Load spreadsheet: xl
xl = pd.ExcelFile(file)

# Print sheet names
print(xl.sheet_names)
      ''',
      "DC_SOLUTION": '''
# Import pandas
import pandas as pd

# Assign spreadsheet filename: file
file = 'battledeath.xlsx'

# Load spreadsheet: xl
xl = pd.ExcelFile(file)

# Print sheet names
print(xl.sheet_names)
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Test: Predefined code
predef_msg = "You don't have to change any of the predefined code."
test_import("pandas", same_as = True, not_imported_msg = predef_msg, incorrect_as_msg = predef_msg)

# Test: assign filename to 'file' variable
test_object("file")

# Test: call to pd.ExcelFile() and 'xl' variable
test_correct(
    lambda: test_object("xl"),
    lambda: test_function("pandas.ExcelFile", index = 1)
)

# Test: print() statement
test_function("print", incorrect_msg = "Did you correctly pass `xl.sheet_names` to `print()`?")

success_msg("Great job!")
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
      ''',
      "DC_CODE": '''
# Import packages
from sqlalchemy import create_engine
import pandas as pd

# Create engine: engine
engine = create_engine('sqlite:///Chinook.sqlite')

# Open engine connection
con = engine.connect()

# Perform query: rs
rs = con.execute("SELECT * FROM Album")

# Save results of the query to dataframe: df
df = pd.DataFrame(rs.fetchall())

# Close connection
con.close()

# Print head of dataframe df
print(df.head())
      ''',
      "DC_SOLUTION": '''
# Import packages
from sqlalchemy import create_engine
import pandas as pd

# Create engine: engine
engine = create_engine('sqlite:///Chinook.sqlite')

# Open engine connection
con = engine.connect()

# Perform query: rs
rs = con.execute("SELECT * FROM Album")

# Save results of the query to dataframe: df
df = pd.DataFrame(rs.fetchall())

# Close connection
con.close()

# Print head of dataframe df
print(df.head())
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Test: Predefined code
predef_msg = "You don't have to change any of the predefined code."
test_import("sqlalchemy.create_engine", same_as = True, not_imported_msg = predef_msg, incorrect_as_msg = predef_msg)
test_import("pandas", same_as = True, not_imported_msg = predef_msg, incorrect_as_msg = predef_msg)

# [6-13-2016: UPDATE WHEN PYTHONWHAT HAS BEEN FIXED]
# test_object("engine", undefined_msg = predef_msg, incorrect_msg = predef_msg)

# Test: call to engine.connect() and 'con' variable
test_object("con", do_eval = False)
test_function("engine.connect")

test_object("rs", do_eval = False)
test_function("con.execute")

# Test: call to pd.DataFrame() and 'df' variable
test_correct(
    lambda: test_object("df"),
    lambda: test_function("pandas.DataFrame")
)

# Test: call to con.close()
test_function("con.close")

success_msg("Good job!")
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
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///Chinook.sqlite')
      ''',
      "DC_CODE": '''
# Execute query and store records in dataframe: df
df = pd.read_sql_query("ELECT * FROM PlaylistTrack INNER JOIN Track on PlaylistTrack.TrackId = Track.TrackId WHERE Milliseconds < 250000", engine)

# Print head of dataframe
print(df.head())
      ''',
      "DC_SOLUTION": '''
# Execute query and store records in dataframe: df
df = pd.read_sql_query("SELECT * FROM PlaylistTrack INNER JOIN Track on PlaylistTrack.TrackId = Track.TrackId WHERE Milliseconds < 250000", engine)

# Print head of dataframe
print(df.head())
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Test: call to read_sql_query() and 'df' variable

test_correct(
    lambda: test_object("df"),
    lambda: test_function("pandas.read_sql_query", do_eval = False)
)

# Test: Predefined code
predef_msg = "You don't have to change any of the predefined code."
test_function("print", incorrect_msg = predef_msg)

success_msg("Great work!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], False)

class TestExercise6(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
from sqlalchemy import create_engine
import pandas as pd
#
engine = create_engine('sqlite:///Chinook.sqlite')
      ''',
      "DC_CODE": '''
# Open engine in context manager
# Perform query and save results to dataframe: df
with engine.connect() as con:
    rs = con.execute("SELECT LastName, Title FROM Employee")
    df = pd.DataFrame(rs.fetchmany(size=3))
    df.columns = rs.keys()

# Print the length of the dataframe df
print(len(df))

#Print the head of the dataframe df
print(df.head())
      ''',
      "DC_SOLUTION": '''
# Open engine in context manager
# Perform query and save results to dataframe: df
with engine.connect() as con:
    rs = con.execute("SELECT LastName, Title FROM Employee")
    df = pd.DataFrame(rs.fetchmany(size=3))
    df.columns = rs.keys()

# Print the length of the dataframe df
print(len(df))

#Print the head of the dataframe df
print(df.head())
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Tests for the context manager body
def test_with_body():

    # Test: call to con.execute() and 'rs' variable
    test_object("rs", do_eval = False)
    test_function("con.execute")

    # Test: call to pd.DataFrame() and 'df' variable
    test_correct(
        lambda: test_object_after_expression("df"),
        lambda: test_function("pandas.DataFrame", do_eval = False)
    )

     # Test: call to rs.keys() and df.columns
    test_correct(
        lambda: test_expression_result(expr_code = "df.columns"),
        lambda: test_function("rs.keys")
    )

# Test: Context manager
test_with(
    1,
    context_vals = True,
    context_tests = lambda: test_function("engine.connect"),
    body = test_with_body
)

# Test: Predefined code
predef_msg = "You don't have to change any of the predefined code."
test_function("print", index = 1, incorrect_msg = predef_msg)
test_function("print", index = 2, incorrect_msg = predef_msg)

success_msg("Awesome!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)


class TestExercise7(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
import numpy as np
      ''',
      "DC_CODE": '''
file = 'titanic.csv'

# Import file using np.genfromtxt: data
data = np.genfromtxt(file , delimiter = ",", names = True , dtype = None)

# Print out datatype of data
print(type(data))

# Import file using np.recfromcsv: d
d = np.recfromcsv(file)

# Print out first three entries of d
print(d[:3])
      ''',
      "DC_SOLUTION": '''
file = 'titanic.csv'

# Import file using np.genfromtxt: data
data = np.genfromtxt(file , delimiter = ",", names = True , dtype = None)

# Print out datatype of data
print(type(data))

# Import file using np.recfromcsv: d
d = np.recfromcsv(file)

# Print out first three entries of d
print(d[:3])
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Test: Predefined code
predef_msg = "You don't have to change any of the predefined code."
test_object("file", undefined_msg = predef_msg, incorrect_msg = predef_msg)

# [6-21-2016: UPDATED WITH FIX]
# Test: call to np.genfromtxt() and 'data' variable
test_object("data", do_eval = False)
test_function(
    "numpy.genfromtxt",
    not_called_msg = "Make sure you call `np.genfromtxt()`.",
    incorrect_msg = "Did you pass the correct arguments to `np.genfromtxt()`?")

# [6-21-2016: NEEDS FIX]
# Test: Predefined code
test_function("type", do_eval = False, not_called_msg = "error in type", incorrect_msg = "error in type")
test_function("print", not_called_msg = predef_msg, incorrect_msg = predef_msg)

# [6-21-2016: UPDATED WITH FIX]
# Test: call to np.recfromcsv() and 'd' variable
test_object("d", do_eval = False)
test_function(
    "numpy.recfromcsv",
    not_called_msg = "Make sure you call `np.recfromcsv()`.",
    incorrect_msg = "Did you pass the correct arguments to `np.recfromcsv()`?")

# Test: Predefined code
test_function("print", index = 2, incorrect_msg = "error is in print2")

success_msg("Good job!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)


class TestExercise8(unittest.TestCase):

  def setUp(self):
    self.data = {
      "DC_PEC": '''
import re
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

# Import package
import json

# String of path to file
tweets_data_path = 'tweets.txt'

# Initialize empty list to store tweets
tweets_data = []

# Open connection to file
tweets_file = open(tweets_data_path, "r")

# Read in tweets and store in list 'tweets_data'
for line in tweets_file:
    tweet = json.loads(line)
    tweets_data.append(tweet)

# Close connection to file
tweets_file.close()

# Import package
import pandas as pd

# Build dataframe of tweet texts and languages
df = pd.DataFrame(tweets_data, columns = ['text','lang'])
      ''',
      "DC_CODE": '''
# Initialize list to store tweet counts
[clinton, trump, sanders, cruz] = [0,0,0,0]

# Interate through df, counting the number of tweets in which
# each candidate is mentioned
for index, row in df.iterrows():
    clinton += word_in_text('clinton', row['text'])
    trump += word_in_text('trump', row['text'])
    sanders += word_in_text('sanders', row['text'])
    cruz += word_in_text('cruz', row['text'])
      ''',
      "DC_SOLUTION": '''
# Initialize list to store tweet counts
[clinton, trump, sanders, cruz] = [0,0,0,0]

# Interate through df, counting the number of tweets in which
# each candidate is mentioned
for index, row in df.iterrows():
    clinton += word_in_text('clinton', row['text'])
    trump += word_in_text('trump', row['text'])
    sanders += word_in_text('sanders', row['text'])
    cruz += word_in_text('cruz', row['text'])
'''
    }

  def test_Pass(self):
    self.data["DC_SCT"] = '''
# Test: Predefined code
predef_msg = "You don't have to change any of the predefined code."

# Test: [clinton, trump, sanders, cruz] objects
test_student_typed("[clinton, trump, sanders, cruz]", pattern = False, not_typed_msg = predef_msg)

def test_for_body():
    # Test: call to word_in_text() and 'clinton' variable
    test_correct(
        lambda: test_object("clinton"),
        lambda: test_function("word_in_text")
    )

    # Test: call to word_in_text() and 'trump' variable
    test_correct(
        lambda: test_object("trump"),
        lambda: test_function("word_in_text")
    )

    # Test: call to word_in_text() and 'sanders' variable
    test_correct(
        lambda: test_object("sanders"),
        lambda: test_function("word_in_text")
    )

    # Test: call to word_in_text() and 'cruz' variable
    test_correct(
        lambda: test_object("cruz"),
        lambda: test_function("word_in_text")
    )

msg = "You have to iterate over `df.iterrows()`"
test_for_loop(
    index = 1,
    for_iter = lambda msg = msg: test_function("df.iterrows",
                                            not_called_msg = msg,
                                            incorrect_msg = msg),
    body = test_for_body
)

success_msg("Awesome!")
    '''
    self.exercise = Exercise(self.data)
    self.exercise.runInit()
    output = self.exercise.runSubmit(self.data)
    sct_payload = helper.get_sct_payload(output)
    self.assertEqual(sct_payload['correct'], True)


if __name__ == "__main__":
  unittest.main()
