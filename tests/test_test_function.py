import unittest
import helper

class TestFunctionBase(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
# pec comes here
            ''',
            "DC_CODE": '''
print(5 / 8)
print(7 + 10)
            ''',
            "DC_SOLUTION": '''
print(5 / 8)
print(7 + 10)
'''
        }

    def test_Pass(self):
        self.data["DC_SCT"] = '''
msg = "Don't remove the first statement. It is an example which is coded for you!"
test_operator(1, incorrect_op_msg = msg, incorrect_result_msg = msg, not_found_msg = msg)
test_operator(2, not_found_msg = "You should add a second operation, as instructed.",
    incorrect_op_msg = "Your second operation is wrong, be sure to add `7` to `10`.",
    incorrect_result_msg = "The operation you added should add up to `17`.")
test_function("print", 1)
test_function("print", 2)

success_msg("Great!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Great!")

    def test_Pass_spec2(self):
        self.data['DC_SCT'] = """
Ex().check_function('print', 0).check_args(0).has_equal_ast()
"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestFunctionExerciseNumpy(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
# pec comes here
            ''',
            "DC_CODE": '''
# Create baseball, a list of lists
baseball = [[180, 78.4],
                        [215, 102.7],
                        [210, 98.5],
                        [188, 75.2]]

# Import numpy
import numpy as np

# Create a 2D Numpy array from baseball: np_baseball
np_baseball = np.array(baseball)

# Print out the type of np_baseball
print(type(np_baseball))

# Print out the shape of np_baseball
print(np_baseball.shape)
            ''',
            "DC_SOLUTION": '''
# Create baseball, a list of lists
baseball = [[180, 78.4],
                        [215, 102.7],
                        [210, 98.5],
                        [188, 75.2]]

# Import numpy
import numpy as np

# Create a 2D Numpy array from baseball: np_baseball
np_baseball = np.array(baseball)

# Print out the type of np_baseball
print(type(np_baseball))

# Print out the shape of np_baseball
print(np_baseball.shape)
'''
        }

    def test_Pass(self):
        self.data["DC_SCT"] = '''
msg = "You don't have to change or remove the predefined variables."
test_object("baseball", undefined_msg = msg, incorrect_msg = msg)

test_import("numpy", same_as = False)

test_object("np_baseball", do_eval = False)
test_function("numpy.array", not_called_msg = "Be sure to call [`np.array()`](http://docs.scipy.org/doc/numpy-1.10.0/glossary.html#term-array).",
                                                         incorrect_msg = "You should call `np.array(baseball)` to make a 2D numpy array out of `baseball`.")
test_object("np_baseball", incorrect_msg = "Assign the correct value to `np_baseball`.")

msg = "Make sure to print out the type of `np_baseball` like this: `print(type(np_baseball))`."
test_function("type", 1, incorrect_msg = msg)
test_function("print", 1, incorrect_msg = msg)

test_function("print", 2, incorrect_msg = "You can print the shape of `np_baseball` like this: `np_baseball.shape`.")

success_msg("Great! You're ready to convert the actual MLB data to a 2D Numpy array now!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Great! You're ready to convert the actual MLB data to a 2D Numpy array now!")

class TestFunctionImporting(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "from urllib.request import urlretrieve; urlretrieve('http://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/moby_opens.txt', 'moby_dick.txt')",
            "DC_CODE": '''
file = open('moby_dick.txt' , 'r') # 'r' is to read only.
print(file.read())
print(file.close)
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

    def test_Fail(self):
        self.data["DC_SCT"] = '''
#test_function("open", incorrect_msg = "Pass the correct arguments to `open()`" )
#file_read_msg = "Make sure to print out the contents of the file like this: `print(file.read())`."
#test_function("file.read", incorrect_msg = file_read_msg)
#test_function("print", 1, args = [], incorrect_msg = file_read_msg)
file_closed_msg = "Make sure to call `print()` the attribute `file.closed` twice, once before you closed the `file` and once after."
#test_function("print", 2, incorrect_msg = file_closed_msg)
#test_function("print", 3, incorrect_msg = file_closed_msg)
test_expression_output(incorrect_msg = file_closed_msg)
#test_function("file.close", not_called_msg = "Make sure to close the file, man!")
success_msg("Good job!")
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Make sure to call <code>print()</code> the attribute <code>file.closed</code> twice, once before you closed the <code>file</code> and once after.", sct_payload['message'])


class TestTestFunctionInWith(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/data.p', 'data.p')
            ''',
            "DC_CODE": '''
import pickle
with open('data.p','rb') as file:
        d = pickle.load(file)
print(d)
print(type(d))
            ''',
            "DC_SOLUTION": '''
import pickle
with open('data.p','rb') as file:
        d = pickle.load(file)
print(d)
print(type(d))
'''
        }
        self.CODE_FAIL = '''
import pickle
with open('data.p','rb') as file:
        d = pickle.load('something_else')
print(d)
print(type(d))
            '''

    def test_Pass(self):
        self.data["DC_SCT"] = '''
import_msg = "Did you import `pickle` correctly?"
test_import("pickle", same_as = True, not_imported_msg = import_msg, incorrect_as_msg = import_msg)
def test_with_body():
        test_object("d")
        test_function("pickle.load", do_eval = False)
test_with(
        1,
        context_vals = True,
        context_tests = lambda: test_function("open"),
        body = test_with_body
)
test_function("print", index = 1)
type_msg = "Print out the type of `d` as follows: `print(type(d))`."
test_function("type", index = 1, incorrect_msg = type_msg)
test_function("print", index = 1, incorrect_msg = type_msg)
success_msg("Awesome!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail(self):
        self.data["DC_CODE"] = self.CODE_FAIL
        self.data["DC_SCT"] = '''
import_msg = "Did you import `pickle` correctly?"
test_import("pickle", same_as = True, not_imported_msg = import_msg, incorrect_as_msg = import_msg)
def test_with_body():
        test_function("pickle.load", do_eval = False)
        test_object("d")
test_with(
        1,
        context_vals = True,
        context_tests = lambda: test_function("open"),
        body = test_with_body
)
test_function("print", index = 1)
type_msg = "Print out the type of `d` as follows: `print(type(d))`."
test_function("type", index = 1, incorrect_msg = type_msg)
test_function("print", index = 1, incorrect_msg = type_msg)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Check the body of the first <code>with</code> statement. Did you call <code>pickle.load()</code> with the correct arguments? The first argument seems to be incorrect.')

    def  test_Fail_no_lam(self):
        self.data["DC_CODE"] = self.CODE_FAIL
        self.data["DC_SCT"] = '''
import_msg = "Did you import `pickle` correctly?"
test_import("pickle", same_as = True, not_imported_msg = import_msg, incorrect_as_msg = import_msg)
test_with(
        1,
        context_vals = True,
        context_tests = test_function("open"),
        ### NOTE the functions are in the list w/o lambdas below
        body = [test_function("pickle.load", do_eval = False), test_object("d")]
)
test_function("print", index = 1)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Check the body of the first <code>with</code> statement. Did you call <code>pickle.load()</code> with the correct arguments? The first argument seems to be incorrect.')

    def  test_Fail_exchain(self):
        self.data["DC_CODE"] = self.CODE_FAIL
        self.data["DC_SCT"] = '''
import_msg = "Did you import `pickle` correctly?"
Ex().test_import("pickle", same_as = True, not_imported_msg = import_msg, incorrect_as_msg = import_msg)
Ex().test_with(
        1,
        context_vals = True,
        context_tests = test_function("open"),
        ### NOTE the functions are in the list w/o lambdas below
        body = [test_function("pickle.load", do_eval = False), test_object("d")]
)
Ex().test_function("print", index = 1)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Check the body of the first <code>with</code> statement. Did you call <code>pickle.load()</code> with the correct arguments? The first argument seems to be incorrect.')

class TestTestFunctionAndTestCorrectWithoutWith(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_CODE": '''
import tweepy
access_token = "1092294848-aHN7DcRP9B4VMTQIhwqOYiB14YkW92fFO8k8EPy"
access_token_secret = "X4dHmhPfaksHcQ7SCbmZa2oYBBVSD2g8uIHXsp5CTaksx"
consumer_key = "nZ6EA0FxZ293SxGNg8g8aP0HM"
consumer_secret = "fJGEodwe3KiKUnsYJC3VRndj7jevVvXbK2D5EiJ2nehafRgA6i"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
            ''',
            "DC_SOLUTION": '''
import tweepy
access_token = "1092294848-aHN7DcRP9B4VMTQIhwqOYiB14YkW92fFO8k8EPy"
access_token_secret = "X4dHmhPfaksHcQ7SCbmZa2oYBBVSD2g8uIHXsp5CTaksx"
consumer_key = "nZ6EA0FxZ293SxGNg8g8aP0HM"
consumer_secret = "fJGEodwe3KiKUnsYJC3VRndj7jevVvXbK2D5EiJ2nehafRgA6i"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
'''
        }

    def test_Pass(self):
        self.data["DC_SCT"] = '''
# Test: import tweepy
import_msg = "Did you correctly import the required package?"
test_import("tweepy", same_as = True, not_imported_msg = import_msg, incorrect_as_msg = import_msg)

# Test: Predefined code
predef_msg = "You don't have to change any of the predefined code."
test_object("access_token", undefined_msg = predef_msg, incorrect_msg = predef_msg)
test_object("access_token_secret", undefined_msg = predef_msg, incorrect_msg = predef_msg)
test_object("consumer_key", undefined_msg = predef_msg, incorrect_msg = predef_msg)
test_object("consumer_secret", undefined_msg = predef_msg, incorrect_msg = predef_msg)

# Test: call to tweepy.OAuthHandler() and 'auth' variable
test_object("auth", do_eval = False)
test_function("tweepy.OAuthHandler")

# Test: call to auth.set_access_token()
test_function("auth.set_access_token")

success_msg("Awesome!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestBlacklisting(unittest.TestCase):

    def test_bookkeeping(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
round(1.23456, ndigits = 1)
            ''',
            "DC_CODE": '''
round(1.23456, ndigits = 1)
            ''',
            "DC_SCT": '''
test_function('round', index = 1) # all in one
test_function('round', index = 1) # same call, should be fine.
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_bookkeeping2(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
round(1.23456, ndigits = 1)
round(1.65432, ndigits = 3)
            ''',
            "DC_CODE": '''
round(1.23456, ndigits = 1)
round(1.65432, ndigits = 3)
            ''',
            "DC_SCT": '''
test_function('round', index = 1) # all in one
test_function('round', args = [0], index = 2) # separate first
test_function('round', keywords = ['ndigits'], index = 2) # separate second
test_function('round', index = 2) # all-in-one
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_bookkeeping3(self):
        self.data = {
        "DC_PEC": '',
        "DC_SOLUTION": '''
round(1.23456, ndigits = 1)
round(1.65432, ndigits = 3)
        ''',
        "DC_CODE": '''
round(1.23456, ndigits = 1)
round(1.65432, ndigits = 4)
        ''',
        "DC_SCT": '''
test_function('round', index = 1) # all in one
test_function('round', args = [0], index = 2) # separate first
test_function('round', keywords = ['ndigits'], index = 2) # separate second
        '''
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])


class TestMessaging(unittest.TestCase):
    def setUp(self):
        self.data = {
             "DC_PEC": '',
             "DC_CODE": '''
import pandas as pd
x = pd.DataFrame({"a":[1, 2, 3]})
print(x)
# no data_range call
# no type(y) call
z = pd.Series([1, 2, 3])
len(z)
print(z)
            ''',
            "DC_SOLUTION": '''
import pandas as pad
x = pad.DataFrame({"a":[1, 2, 3]}) # correct
print(x) # correct
y = pad.date_range('1/1/2000', periods=8)
type(y)
z = pad.Series([1, 2, 4]) # incorrect
len(z) # incorrect
print(z) # incorrect
            '''
        }

    def test_auto(self):
        self.data["DC_SCT"] = '''
test_function("pandas.DataFrame")
test_function("print")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

        self.data["DC_SCT"] = 'test_function("pandas.date_range")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you called <code>pd.date_range()</code>?")

        self.data["DC_SCT"] = 'test_function("type")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn(sct_payload['message'], "Have you called <code>type()</code>?")

        self.data["DC_SCT"] = 'test_function("pandas.Series")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>pd.Series()</code> with the correct arguments?", sct_payload['message'])

        self.data["DC_SCT"] = 'test_function("len")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>len()</code> with the correct arguments?", sct_payload['message'])

        self.data["DC_SCT"] = 'test_function("print", index = 1); test_function("print", index = 2)'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>print()</code> with the correct arguments?", sct_payload['message'])


    def test_custom(self):
        self.data["DC_SCT"] = '''
test_function("pandas.DataFrame")
test_function("print")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

        self.data["DC_SCT"] = 'test_function("pandas.date_range", not_called_msg = "stupid")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "stupid")

        self.data["DC_SCT"] = 'test_function("type", not_called_msg = "stupid")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "stupid")

        self.data["DC_SCT"] = 'test_function("pandas.Series", incorrect_msg = "stupid")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("stupid", sct_payload['message'])

        self.data["DC_SCT"] = 'test_function("len", incorrect_msg = "stupid")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("stupid", sct_payload['message'])

class TestLineNumbers(unittest.TestCase):
    def test_line_numbers1(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(1.23456, ndigits = 1)",
                     "DC_CODE": "round(1.34567, ndigits = 1)",
                     "DC_SCT": "test_function('round', index = 1, highlight=True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>round()</code> with the correct arguments? The first argument seems to be incorrect.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 7, 13)

    def test_line_numbers(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(1.23456, ndigits = 1)",
                     "DC_CODE": "round(1.23456, ndigits = 3)",
                     "DC_SCT": "test_function('round', index = 1, highlight=True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>round()</code> with the correct arguments? Keyword <code>ndigits</code> seems to be incorrect.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 26, 26)


class TestFunctionNested(unittest.TestCase):
    def test_nested_arg1(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "print(type([1, 2, 3]))",
                     "DC_CODE": "print(type([1, 2, 3]))",
                     "DC_SCT": "test_function('type')"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_nested_arg2(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "print(type([1, 2, 3]))",
                     "DC_CODE": "print(type([1, 2, 4]))",
                     "DC_SCT": "test_function('type', highlight=True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 12, 20)

    def test_nested_keyw1(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(1.1234, ndigits = max([1, 2, 3]))",
                     "DC_CODE": "round(1.1234, ndigits = max([1, 2, 3]))",
                     "DC_SCT": "test_function('max', highlight=True)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_nested_keyw2(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(1.1234, ndigits = max([1, 2, 3]))",
                     "DC_CODE": "round(1.1234, ndigits = max([1, 2]))",
                     "DC_SCT": "test_function('max', highlight=True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 1, 1, 29, 34)

class TestFunctionDoEval(unittest.TestCase):
    def test_do_eval_true_pass(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(2.1234, ndigits = 4)",
                     "DC_CODE": "round(2.1234, ndigits = 4)",
                     "DC_SCT": "test_function('round', do_eval = True)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        #self.assertIn()

    def test_do_eval_true_fail(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "round(2.1234, ndigits = 4)",
                     "DC_CODE": "round(2.123456, ndigits = 4)",
                     "DC_SCT": "test_function('round', do_eval = True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>round()</code> with the correct arguments?", sct_payload['message'])

    def test_do_eval_false_pass(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "x = 2.12309123; round(x, ndigits = 4)",
                     "DC_CODE": "x = 2.123450; round(x, ndigits = 4)",
                     "DC_SCT": "test_function('round', do_eval = False)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_false_fail(self):
        self.data = {"DC_PEC": '',
                     "DC_SOLUTION": "y = 2.12309123; round(y, ndigits = 4)",
                     "DC_CODE": "x = 2.123450; round(x, ndigits = 4)",
                     "DC_SCT": "test_function('round', do_eval = False)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Did you call <code>round()</code> with the correct arguments? The first argument seems to be incorrect.", sct_payload['message'])

    def test_do_eval_none_pass(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, ndigits = 2)",
             "DC_CODE": "round(123.123, ndigits = 2)",
             "DC_SCT": "test_function('round', do_eval = None)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_do_eval_none_fail1(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, ndigits = 2)",
             "DC_CODE": "round(123.123)",
             "DC_SCT": "test_function('round', do_eval = None, highlight=True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Have you specified all required arguments inside <code>round()</code>?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 14)

    def test_do_eval_none_fail2(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123)", # args = [0]
             "DC_CODE": "round(number = 123.123)", # student args is len 0
             "DC_SCT": "test_function('round', do_eval = None, highlight=True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Have you specified all required arguments inside <code>round()</code>?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 23)

    def test_do_eval_none_fail3(self):
        self.data = {"DC_PEC": '',
             "DC_SOLUTION": "round(123.123, 2)", # args = [0, 1]
             "DC_CODE": "round(123.123)", # student_args is len 1
             "DC_SCT": "test_function('round', do_eval = None, highlight=True)"}
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Have you specified all required arguments inside <code>round()</code>?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 1, 14)

class Test_MultipleCalls(unittest.TestCase):
    def setUp(self):
        self.data = {
             "DC_PEC": '',
            "DC_SOLUTION": '''
print("abc")
print(123)
print([1, 2, 3])
            ''',
             "DC_SCT": '''
test_function("print", index = 1, highlight=True)
test_function("print", index = 2, highlight=True)
test_function("print", index = 3, highlight=True)
            '''
        }

    def test_multiple_1(self):
        self.data["DC_CODE"] = 'print("abc")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the second call of <code>print()</code>, but hasn't found it; have another look at your code.")

    def test_multiple_2(self):
        self.data["DC_CODE"] = 'print("abc")\nprint(123)'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the third call of <code>print()</code>, but hasn't found it; have another look at your code.")

    def test_multiple_3(self):
        self.data["DC_CODE"] = 'print("abc")\nprint(123)\nprint([1, 2, 3])'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_multiple_4(self):
        self.data["DC_CODE"] = 'print("acb")\nprint(1234)\nprint([1, 2, 3])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>print()</code> with the correct arguments? The first argument seems to be incorrect.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 7, 11)

    def test_multiple_4_no_highlight(self):
        self.data["DC_CODE"] = 'print("acb")\nprint(1234)\nprint([1, 2, 3])'
        self.data["DC_SCT"] = """
test_function("print", index = 1, highlight = False)
test_function("print", index = 2)
test_function("print", index = 3)
        """
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>print()</code> with the correct arguments? The first argument seems to be incorrect.", sct_payload['message'])
        self.assertEqual(sct_payload.get('line_start'), None)

    def test_multiple_5(self):
        self.data["DC_CODE"] = 'print("abc")\nprint(1234)\nprint([1, 2, 3])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>print()</code> with the correct arguments? The first argument seems to be incorrect.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 2, 2, 7, 10)

    def test_multiple_6(self):
        self.data["DC_CODE"] = 'print("abc")\nprint(123)\nprint([1, 2, 3, 4])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>print()</code> with the correct arguments? The first argument seems to be incorrect.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 3, 3, 7, 18)

    def test_nohighlight_too_few_calls(self):
        self.data["DC_SCT"] = 'test_function("print", index = 3, args = [], keywords = [])\n' + self.data["DC_SCT"]
        self.data["DC_CODE"] = 'print("abc")\nprint(1234)'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload.get('line_start'), None)

class TestCheckFunction(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_CODE": "np.array([1,2,3])",
            "DC_SOLUTION": "np.array([1,2,3])",
            "DC_SCT": "Ex().check_function('numpy.array', 0)"
            }

    def run_append(self, sct):
        self.data["DC_SCT"] += sct
        return helper.run(self.data)

    def run_pass(self, sct):
        sct_payload = self.run_append(sct)
        print(sct_payload)
        self.assertTrue(sct_payload['correct'])
        return sct_payload

    def run_fail(self, sct):
        self.assertFalse(self.run_append(sct)['correct'])

    def test_pass_np_call_exists(self):
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_test_student_typed(self):
        self.run_pass(".test_student_typed(r'np\.array\(\[1,2,3\]\)')")

    def test_fail_test_student_typed(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".test_student_typed(r'np\.array\(\[1,2,3\]\)')")

    def test_pass_func_has_equal_ast(self):
        self.run_pass(".has_equal_ast()")

    def test_fail_func_has_equal_ast(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".has_equal_ast()")

    def test_pass_check_args_pos_0(self):
        self.run_pass(".check_args(0)")

    def test_fail_check_args_pos_0(self):
        self.data["DC_CODE"] = "np.array()"
        self.run_fail(".check_args(0)")

    def test_pass_pos_0_test_student_typed(self):
        self.run_pass(".check_args(0).test_student_typed(r'\[1,2,3\]')")

    def test_fail_pos_0_test_student_typed(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".check_args(0).test_student_typed(r'\[1,2,3\]')")

    def test_pass_pos_0_has_equal_ast(self):
        self.run_pass(".check_args(0).has_equal_ast()")

    def test_fail_pos_0_has_equal_ast(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".check_args(0).has_equal_ast()")

    def test_pass_pos_0_has_equal_value(self):
        self.run_pass(".check_args(0).has_equal_value()")

    def test_fail_pos_0_has_equal_value(self):
        self.data["DC_CODE"] = "np.array([1,2])"
        self.run_fail(".check_args(0).has_equal_value()")

    def test_pass_pos_0_inline_if_body(self):
        self.data["DC_CODE"] = "np.array([1,2,3] if True else [1])"
        self.data["DC_SOLUTION"] = "np.array([1,2,3] if False else [1])"
        self.run_pass(".check_args(0).check_if_exp(0).check_body().has_equal_ast()")

    def test_fail_pos_0_inline_if_body(self):
        self.data["DC_CODE"] = "np.array([1,2,3] if True else [1])"
        self.data["DC_SOLUTION"] = "np.array([1,2] if False else [1])"
        self.run_fail(".check_args(0).check_if_exp(0).check_body().has_equal_ast()")

class TestCheckFunctionCases(unittest.TestCase):
    def setup_color(self):
        self.data = {
                'DC_PEC': "def f(*args, **kwargs): pass",
                'DC_CODE': "f(color = 'blue')"
                }
        self.data["DC_SOLUTION"] = self.data["DC_CODE"]

    def test_pass_sig_false(self):
        self.setup_color()
        self.data['DC_SCT'] =  "Ex().check_function('f', 0, signature=False).check_args('color').has_equal_ast()"

        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_sig_false_override(self):
        self.setup_color()
        self.data["DC_CODE"] = self.data["DC_CODE"].replace('color', 'c')
        self.data['DC_SCT'] =  """
Ex().override("f(c = 'blue')").check_function('f', 0, signature=False).check_args('c').has_equal_ast()
"""

        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    @unittest.skip("TODO: override code isn't parsed, so can't get args part")
    def test_pass_sig_false_override_after_check(self):
        self.setup_color()
        self.data["DC_CODE"] = self.data["DC_CODE"].replace('color', 'c')
        self.data['DC_SCT'] =  """
Ex().check_function('f', 0, signature=False).override("f(c = 'blue')").check_args('c').has_equal_ast()
"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestFunctionComplexArgs(unittest.TestCase):
    def setUp(self):
        self.data = {
                "DC_SOLUTION": """
def sum2(arr): return sum(arr)

def apply(f, arr): return f(arr)

apply(sum2, [1,2,3])
""",
                "DC_SCT": """
test_function('apply')
"""
                }
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]

    def test_function_with_funcarg_fails(self):
        # because functions are shipped across student and submission processes
        # they are always "unequal".
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_pass_with_no_eval(self):
        self.data["DC_SCT"] = """test_function_v2('apply', params=['f', 'arr'], do_eval=[False, True])"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail_undillable_args(self):
        self.data = {
                "DC_PEC": """
import pickle; from io import BytesIO

file = BytesIO(pickle.dumps('abc'))
        """,
                "DC_SOLUTION": "d = pickle.load(file); print(d)",
                "DC_CODE": "print(file)",
                "DC_SCT": """test_function("print", index=1)"""
                }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])


if __name__ == "__main__":
    unittest.main()
