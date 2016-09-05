import unittest
import helper

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

if __name__ == "__main__":
    unittest.main()
