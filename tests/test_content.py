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

if __name__ == "__main__":
    unittest.main()
