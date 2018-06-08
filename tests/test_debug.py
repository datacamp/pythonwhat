import pytest
import helper

def test_normal_pass():
    code = """
print(df.groupby('sex')['tip'].mean())
print(df.groupby(['sex', 'time'])['tip'].mean())
"""
    data = {
		"DC_PEC": """
import seaborn as sns
import pandas as pd
import numpy as np
df = sns.load_dataset('tips')
""",
		"DC_CODE": code,
        "DC_SOLUTION": code,
		"DC_SCT": """
Ex().check_function("print", index=0, expand_msg = '', signature = False).check_args(0).has_equal_value("Informative message")
"""
	}
    output = helper.run(data)
    assert output['correct']