import unittest
import helper

class TestTemplate(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '''
import pandas as pd
movies = pd.read_csv("http://s3.amazonaws.com/assets.datacamp.com/course/introduction_to_r/movies.csv")
import numpy as np
            ''',
            "DC_SOLUTION": '''
_, ints = np.unique(movies.genre, return_inverse = True)
import matplotlib.pyplot as plt
plt.scatter(movies.runtime, movies.rating, c=ints)
#plt.show()
            ''',
            "DC_SCT": '''
test_function("numpy.unique")
test_object("ints")
test_import("matplotlib.pyplot", same_as = True)
test_function("matplotlib.pyplot.scatter")
# test_function("matplotlib.pyplot.show")
success_msg("Great work!")
            '''
        }

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestToolbox1(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_1342/datasets/tweets.csv'
from urllib.request import urlretrieve
urlretrieve(fn, 'tweets.csv')
            ''',
            "DC_SOLUTION": '''
import pandas as pd
df = pd.read_csv('tweets.csv')
langs_count = {}
col = df['lang']
for entry in col:
    if entry in langs_count.keys():
        langs_count[entry] += 1
    else:
        langs_count[entry] = 1
print(langs_count)
            ''',
            "DC_SCT": '''
test_import("pandas")
test_function("pandas.read_csv")
test_object("df")

test_object("col")
def test_for_iter():
    test_expression_result()

def test_for_body():
    def test_test():
        test_function("langs_count.keys")
    def test_body():
        test_student_typed("\+=\s*1")
    def test_orelse():
        test_student_typed("=\s*1")
    test_if_else(index = 1,
                 test = test_test,
                 body = test_body,
                 orelse = test_orelse)

test_for_loop(
    index=1,
    for_iter=test_for_iter,
    body=test_for_body
)

test_object("langs_count")
test_function("print")

success_msg("Great work!")
            '''
        }

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestToolbox2(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''
fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_1342/datasets/tweets.csv'
from urllib.request import urlretrieve
urlretrieve(fn, 'tweets.csv')
            ''',
            "DC_SOLUTION": '''
import pandas as pd
df = pd.read_csv('tweets.csv')
langs_count = {}
col = df['lang']
for entry in col:
    if entry in langs_count.keys():
        langs_count[entry] += 1
    else:
        langs_count[entry] = 1
print(langs_count)
            ''',
            "DC_SCT": '''
test_import("pandas")
test_function("pandas.read_csv")
test_object("df")

test_object("col")
def test_for_iter():
    test_expression_result()

def test_for_body():
    test_object_after_expression("langs_count",
                                 extra_env = {'langs_count': {"en": 1}},
                                 context_vals = ['et'])
    test_object_after_expression("langs_count",
                                 extra_env = {'langs_count': {"en": 1}},
                                 context_vals = ['en'])

test_for_loop(
    index=1,
    for_iter=test_for_iter,
    body=test_for_body
)

test_object("langs_count")
test_function("print")

success_msg("Great work!")
            '''
        }

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestToolbox3(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
def three_shouts(word1, word2, word3):
    def inner(word):
        return word + '!!!'
    return (inner(word1), inner(word2), inner(word3))
            ''',
            "DC_SCT": '''

def inner_test():
    def inner_body_test():
        test_student_typed("word\s*\+\s*['\\"]!!!['\\"]", not_typed_msg = "Have you correctly coded `inner()`?")
    test_function_definition("inner", body = inner_body_test)

test_function_definition("three_shouts",
                         body= inner_test,
                         results = [("hi", "there", "pretty")])
            '''}

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestToolbox4(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
def echo_shout(word):
    echo_word = word*2
    print(echo_word)
    def shout():
        global echo_word
        echo_word = echo_word + '!!!'
    shout()
    print(echo_word)
            ''',
            "DC_SCT": '''

def inner_test():
    test_object_after_expression("echo_word", context_vals=["hello"])
    test_function_definition("shout")
    test_function("shout")
    test_function("print", args=[], index=1)
    test_function("print", args=[], index=2)

test_function_definition("echo_shout", body=inner_test)
            '''}

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestToolbox5(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
def shout_echo(word1, echo = 1, intense = False):
    echo_word = word1 * echo
    if intense is True:
        echo_word_new = echo_word.upper() + '!!!'
    else:
        echo_word_new = echo_word + '!!!'

    return echo_word_new
            ''',
            "DC_SCT": '''


def inner_test():
    def check_inner():
        test_object_after_expression("echo_word", context_vals = ["Hey!!!", 2, True])
        test_object_after_expression("echo_word_new", context_vals = ["Hey!!!", 2, True])

    def diagnose_inner():
        def test_test():
            test_expression_result({"intense": True})
            test_expression_result({"intense": False})

        def test_body():
            test_object_after_expression("echo_word_new", extra_env = {'echo_word': 'Hey!!! Hey!!!'})

        def test_orelse():
            test_object_after_expression("echo_word_new", extra_env = {'echo_word': 'Hey!!! Hey!!!'})

        test_if_else(index = 1, test = test_test, body = test_body, orelse = test_orelse)

    # test_correct(check_inner, diagnose_inner)
    check_inner()
    diagnose_inner()

test_function_definition("shout_echo", body = inner_test)
            '''
        }

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestToolbox6(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
spells = ["protego", "accio", "expecto patronum", "legilimens"]
shout_spells = map(lambda item: item + '!!!', spells)
            ''',
            "DC_SCT": '''
test_object('shout_spells')
def diagnose():
    test_lambda_function(1, results = ["lam('hello')"])
    test_function("map", args = [1])
test_correct(lambda: test_object('shout_spells'), diagnose)
            '''
        }

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestToolbox7(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '''
fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_1342/datasets/tweets.csv'
from urllib.request import urlretrieve
urlretrieve(fn, 'tweets.csv')
import pandas as pd
tweets_df = pd.read_csv('tweets.csv')
            ''',
            "DC_SOLUTION": '''
def count_entries(df, col_name):
    langs_count = {}
    col = df[col_name]
    for entry in col:
        if entry in langs_count.keys():
            langs_count[entry] += 1
        else:
            langs_count[entry] = 1
    return langs_count

result = count_entries(tweets_df, 'lang')
print(result)
            ''',
            "DC_SCT": '''

def inner_test():
    import pandas as pd
    test_df = pd.DataFrame({'a': [0,1], 'lang':[2,2]})
    test_object_after_expression("col", context_vals = [test_df, 'lang'])
    def test_for_iter():
        test_expression_result(extra_env = {'col': pd.Series([2, 2])})

    def test_for_body():
        test_object_after_expression("langs_count",
                                     extra_env = {'langs_count': {"en": 1}},
                                     context_vals = ['et'])
        test_object_after_expression("langs_count",
                                     extra_env = {'langs_count': {"en": 1}},
                                     context_vals = ['en'])

    test_for_loop(
        index=1,
        for_iter=test_for_iter,
        body=test_for_body
    )

    test_object_after_expression("langs_count", context_vals = [test_df, 'lang'])

import pandas as pd
test_df = pd.DataFrame({'a': [0,1], 'lang':[2,2]})
test_function_definition(
    "count_entries", body = inner_test,
    results=[[test_df, 'lang']],
)
test_function("count_entries")
test_object("result")
test_function("print")

success_msg("Great work!")
            '''
        }

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestFunctionBase(unittest.TestCase):

    def test_pass(self):
        self.data = {
            "DC_PEC": '''
fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/tweets3.txt'
from urllib.request import urlretrieve
urlretrieve(fn, 'tweets.txt')
import json
tweets_data_path = 'tweets.txt'
tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    tweet = json.loads(line)
    tweet["text"] = tweet.get("text").encode('unicode_escape')
    tweets_data.append(tweet)
tweets_file.close()
            ''',
            "DC_SOLUTION": '''
import pandas as pd
df = pd.DataFrame(tweets_data, columns=['text', 'lang'])
print(df.head())
            ''',
            "DC_CODE": '''
import pandas as pd
df = pd.DataFrame(tweets_data, columns=['text', 'lang'])
print(df.head())
            ''',
            "DC_SCT": '''
test_import("pandas", same_as=True)
# set_converter(key = "pandas.core.frame.DataFrame", fundef = lambda x: x.shape)
test_function_v2("pandas.DataFrame", params = ["data"], do_eval = [False])
test_object("df", do_eval = False)
test_function("df.head")
test_function("print")
success_msg("Awesome!")
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestImporting(unittest.TestCase):
    def test_pass(self):
        self.data = {
            "DC_PEC": '''
from urllib.request import urlretrieve
fn1 = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite'
urlretrieve(fn1, 'Chinook.sqlite')
            ''',
            "DC_SOLUTION": '''
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('sqlite:///Chinook.sqlite')
df = pd.read_sql_query("SELECT * FROM Album", engine)
print(df.head())
with engine.connect() as con:
    rs = con.execute("SELECT * FROM Album")
    df1 = pd.DataFrame(rs.fetchall())
    df1.columns = rs.keys()
print(df.equals(df1))
            ''',
            "DC_SCT": '''
predef_msg = "You don't have to change any of the predefined code."
test_import(
    "sqlalchemy.create_engine",
    same_as=True,
    not_imported_msg=predef_msg,
    incorrect_as_msg=predef_msg
)

# Test: import pandas
test_import("pandas", same_as=True)

# Test: call to create_engine() and 'engine' variable
test_object("engine", do_eval=False, undefined_msg=predef_msg)
test_function("sqlalchemy.create_engine")

test_function(
    "pandas.read_sql_query", args=[1], index=1,
    do_eval=False,
    not_called_msg="Make sure you call `pd.read_sql_query()`.",
    incorrect_msg="Make sure to pass `engine` as the second argument to `pd.read_sql_query`."
)



# Test: call to pandas.read_sql_query() and 'df' variable
# test_object("df", undefined_msg="You don't have to change any of the predefined code.")

test_object("df", undefined_msg="You don't have to change any of the predefined code.")
test_function("pandas.read_sql_query", not_called_msg="You don't have to change any of the predefined code.")

# Test: Predefined code
test_function("print", index=1, incorrect_msg=predef_msg)
def test_with_body():
    predef_msg = "You don't have to change any of the predefined code."
    test_object("rs", do_eval=False, undefined_msg=predef_msg, incorrect_msg = predef_msg)
    test_object("df1", do_eval=False, undefined_msg=predef_msg, incorrect_msg = predef_msg)
    test_student_typed(
        "df1.columns",
        pattern = False,
        not_typed_msg=predef_msg
    )

test_with(1,
    context_vals=True,
    context_tests=lambda: test_function("engine.connect"),
    body=test_with_body
)

test_function("print", index=2, not_called_msg=predef_msg, incorrect_msg=predef_msg)

success_msg("Excellent!")
            '''
        }
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()
