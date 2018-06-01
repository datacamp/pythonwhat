import pytest
import helper

@pytest.mark.compiled
def test_converter_err():
    data = {
            "DC_SOLUTION": "import numpy as np; x = np.array([1, 2, 3])",
            "DC_SCT": """def convert(): return abc\nset_converter('numpy.ndarray', convert); test_object('x') """
            }
    data['DC_CODE'] = data['DC_SOLUTION']
    with pytest.raises(TypeError):
        helper.run(data)

def test_check_syntax_double_getattr():
    data = {
            "DC_SOLUTION": "",
            "DC_CODE": "",
            "DC_SCT": """Ex().check_list_comp.check_body()"""
            }
    with pytest.raises(AttributeError):
        helper.run(data)

def test_check_syntax_check_index_no_index():
    data = {
            "DC_SOLUTION": "[i for i in range(1)]",
            "DC_CODE": "[i for i in range(1)]",
            "DC_SCT": """Ex().check_list_comp()"""
            }
    with pytest.raises(TypeError):
        helper.run(data)

def test_context_vals_wrong_place_in_chain():
    data = {"DC_SOLUTION": "[(i,j) for i,j in enumerate(range(10))]"}
    data["DC_CODE"] = data["DC_SOLUTION"]
    data["DC_SCT"] = """Ex().check_list_comp(0).set_context(i=1,j=2).check_iter()"""
    with pytest.raises(KeyError):
        helper.run(data)
