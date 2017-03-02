import unittest
import helper
import pytest

class TestExercise1(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
from urllib.request import urlretrieve; urlretrieve('http://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/moby_opens.txt', 'moby_dick.txt')
            ''',
            "DC_CODE": '''
file = open('moby_dick.txt' , 'r') # 'r' is to read only.
print(file.read())
print(file.closed)
file.close()
print(file.closed)
            ''',
            "DC_SOLUTION": '''
file = open('moby_dick.txt' , 'r') # 'r' is to read only.
print(file.read())
print(file.closed)
file.close()
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
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestExercise2(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite', 'Chinook.sqlite')
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
test_function("sqlalchemy.create_engine")

success_msg("Awesome!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestExercise3(unittest.TestCase):

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
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestExercise4(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite', 'Chinook.sqlite')
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
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestExercise5(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
import pandas as pd
from sqlalchemy import create_engine
from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite', 'Chinook.sqlite')
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
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

class TestExercise6(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
from sqlalchemy import create_engine
import pandas as pd
from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite', 'Chinook.sqlite')
engine = create_engine('sqlite:///Chinook.sqlite')
            ''',
            "DC_CODE": '''
with engine.connect() as con:
        rs = con.execute("SELECT LastName, Title FROM Employee")
        df = pd.DataFrame(rs.fetchmany(size=3))
        df.columns = rs.keys()
print(len(df))
print(df.head())
            ''',
            "DC_SOLUTION": '''
# Open engine in context manager
# Perform query and save results to dataframe: df
with engine.connect() as con:
        rs = con.execute("SELECT LastName, Title FROM Employee")
        df = pd.DataFrame(rs.fetchmany(size=3))
        df.columns = rs.keys()
print(len(df))
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
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestExercise7(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
import numpy as np
from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/titanic_sub.csv', 'titanic.csv')
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
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


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
from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/tweets3.txt', 'tweets.txt')
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
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


@pytest.mark.dep_matplotlib
class TestImportWhenTestFunction(unittest.TestCase):

    def test_pass(self):
                self.data = {
                "DC_PEC": '''
import matplotlib.pyplot as plt; import importlib; importlib.reload(plt)
plt.clf()
year = list(range(1950, 2101))
pop = [2.53,2.57,2.62,2.67,2.71,2.76,2.81,2.86,2.92,2.97,3.03,3.08,3.14,3.2,3.26,3.33,3.4,3.47,3.54,3.62,3.69,3.77,3.84,3.92,4.,4.07,4.15,4.22,4.3,4.37,4.45,4.53,4.61,4.69,4.78,4.86,4.95,5.05,5.14,5.23,5.32,5.41,5.49,5.58,5.66,5.74,5.82,5.9,5.98,6.05,6.13,6.2,6.28,6.36,6.44,6.51,6.59,6.67,6.75,6.83,6.92,7.,7.08,7.16,7.24,7.32,7.4,7.48,7.56,7.64,7.72,7.79,7.87,7.94,8.01,8.08,8.15,8.22,8.29,8.36,8.42,8.49,8.56,8.62,8.68,8.74,8.8,8.86,8.92,8.98,9.04,9.09,9.15,9.2,9.26,9.31,9.36,9.41,9.46,9.5,9.55,9.6,9.64,9.68,9.73,9.77,9.81,9.85,9.88,9.92,9.96,9.99,10.03,10.06,10.09,10.13,10.16,10.19,10.22,10.25,10.28,10.31,10.33,10.36,10.38,10.41,10.43,10.46,10.48,10.5,10.52,10.55,10.57,10.59,10.61,10.63,10.65,10.66,10.68,10.7,10.72,10.73,10.75,10.77,10.78,10.79,10.81,10.82,10.83,10.84,10.85]
                ''',
                "DC_SOLUTION": '''
# Print the last item from years and populations
print(year[-1])
print(pop[-1])

# Import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

                ''',
                "DC_CODE": '''
# Print the last item from years and populations
print(year[-1])
print(pop[-1])

# Import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
                ''',
                "DC_SCT": '''
test_function("print", 1)
test_function("print", 2)
test_import("matplotlib.pyplot")
                '''
                }
                sct_payload = helper.run(self.data)
                self.assertTrue(sct_payload['correct'])


if __name__ == "__main__":
    unittest.main()
