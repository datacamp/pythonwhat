import pytest
import tests.helper as helper


@pytest.mark.slow
def test_excel():
    data = {
        "DC_PEC": "import pandas as pd; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/battledeath.xlsx', 'battledeath.xlsx')",
        "DC_SOLUTION": "xl = pd.ExcelFile('battledeath.xlsx')",
        "DC_SCT": "test_object('xl')",
        "DC_CODE": "xl = pd.ExcelFile('battledeath.xlsx')",
    }
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


@pytest.mark.slow
def test_dict_keys():
    data = {
        "DC_PEC": "",
        "DC_SOLUTION": "x = {'a': 1, 'b': 2}; print(x.keys())",
        "DC_CODE": "x = {'b':2, 'a': 1}; print(x.keys())",
        "DC_SCT": "Ex().check_function('print').check_args('value').has_equal_value()",
    }
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


@pytest.mark.slow
def test_dictitems():
    data = {
        "DC_PEC": "",
        "DC_SOLUTION": "x = {'france':'paris', 'spain':'madrid'}.items()",
        "DC_CODE": "x = {'spain':'madrid', 'france':'paris'}.items()",
        "DC_SCT": "Ex().check_object('x').has_equal_value()",
    }
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


@pytest.mark.slow
def test_beautiful_soup():
    data = {
        "DC_PEC": "import requests; from bs4 import BeautifulSoup",
        "DC_SOLUTION": "soup = BeautifulSoup(requests.get('https://www.python.org/~guido/').text, 'html5lib'); print(soup.title); a_tags = soup.find_all('a')",
        "DC_CODE": "soup = BeautifulSoup(requests.get('https://www.python.org/~guido/').text, 'html5lib'); print(soup.title); a_tags = soup.find_all('a')",
        "DC_SCT": "Ex().check_object('soup').has_equal_value(); Ex().check_function('print').check_args('value').has_equal_value(); Ex().check_object('a_tags').has_equal_value()",
    }
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


@pytest.mark.slow
def test_hdf5():
    data = {
        "DC_PEC": "import numpy as np; import h5py; file = 'LIGO_data.hdf5'; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/L-L1_LOSC_4_V1-1126259446-32.hdf5', 'LIGO_data.hdf5')",
        "DC_SOLUTION": "data = h5py.File(file, 'r'); group = data['strain']",
        "DC_CODE": "data = h5py.File(file, 'r'); group = data['strain']",
        "DC_SCT": "Ex().check_object('file').has_equal_value(); Ex().check_object('data').has_equal_value(); Ex().check_object('group').has_equal_value()",
    }
    sct_payload = helper.run(data)
    assert sct_payload["correct"]
