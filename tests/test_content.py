import unittest
import helper

class TestFunctionBase(unittest.TestCase):

    def test_fun_pass(self):
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

if __name__ == "__main__":
    unittest.main()
