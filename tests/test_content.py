import unittest
import helper

# class TestFunctionBase(unittest.TestCase):

#     def test_fun_pass(self):
#         self.data = {
#             "DC_PEC": '''
# fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/tweets3.txt'
# from urllib.request import urlretrieve
# urlretrieve(fn, 'tweets.txt')
# import json
# tweets_data_path = 'tweets.txt'
# tweets_data = []
# tweets_file = open(tweets_data_path, "r")
# for line in tweets_file:
#     tweet = json.loads(line)
#     tweet["text"] = tweet.get("text").encode('unicode_escape')
#     tweets_data.append(tweet)
# tweets_file.close()
#             ''',
#             "DC_SOLUTION": '''
# import pandas as pd
# df = pd.DataFrame(tweets_data, columns=['text', 'lang'])
# print(df.head())
#             ''',
#             "DC_CODE": '''
# import pandas as pd
# df = pd.DataFrame(tweets_data, columns=['text', 'lang'])
# print(df.head())
#             ''',
#             "DC_SCT": '''
# test_import("pandas", same_as=True)
# # set_converter(key = "pandas.core.frame.DataFrame", fundef = lambda x: x.shape)
# test_function_v2("pandas.DataFrame", params = ["data"], do_eval = [False])
# test_object("df", do_eval = False)
# test_function("df.head")
# test_function("print")
# success_msg("Awesome!")
#             '''
#         }
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

class TestImporting(unittest.TestCase):
    def test_fun_pass(self):
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
