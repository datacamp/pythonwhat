import unittest
import helper

class TestBuiltInConverters(unittest.TestCase):

    def test_excel(self):
        self.data = {
            "DC_PEC": "import pandas as pd; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/battledeath.xlsx', 'battledeath.xlsx')",
            "DC_SOLUTION": "xl = pd.ExcelFile('battledeath.xlsx')",
            "DC_SCT": "test_object('xl')",
            "DC_CODE": "xl = pd.ExcelFile('battledeath.xlsx')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_dict_keys(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = {'a': 1, 'b': 2}; print(x.keys())",
            "DC_CODE": "x = {'b':2, 'a': 1}; print(x.keys())",
            "DC_SCT": "test_function_v2('print', params = ['value'])"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_dictitems(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = {'france':'paris', 'spain':'madrid'}.items()",
            "DC_CODE": "x = {'spain':'madrid', 'france':'paris'}.items()",
            "DC_SCT": "test_object('x')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_beautiful_soup(self):
        self.data = {
            "DC_PEC": "import requests; from bs4 import BeautifulSoup",
            "DC_SOLUTION": "soup = BeautifulSoup(requests.get('https://www.python.org/~guido/').text); print(soup.title); a_tags = soup.find_all('a')",
            "DC_CODE": "soup = BeautifulSoup(requests.get('https://www.python.org/~guido/').text); print(soup.title); a_tags = soup.find_all('a')",
            "DC_SCT": "test_object('soup'); test_function_v2('print', params = ['value']); test_object('a_tags')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_hdf5(self):
        self.data = {
            "DC_PEC": "import numpy as np; import h5py; file = 'LIGO_data.hdf5'; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/L-L1_LOSC_4_V1-1126259446-32.hdf5', 'LIGO_data.hdf5')",
            "DC_SOLUTION": "data = h5py.File(file, 'r'); group = data['strain']",
            "DC_CODE": "data = h5py.File(file, 'r'); group = data['strain']",
            "DC_SCT": "test_object('file'); test_object('data'); test_object('group')"
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])



if __name__ == "__main__":
    unittest.main()
