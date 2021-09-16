import pytest
import tests.helper as helper
from pythonwhat.test_exercise import setup_state


@pytest.mark.parametrize(
    "sct",
    [
        "test_object('x', undefined_msg='udm', incorrect_msg='icm')",
        "Ex().check_object('x', missing_msg='udm').has_equal_value(incorrect_msg='icm')",
    ],
)
@pytest.mark.parametrize(
    "stu_code, passes, msg",
    [("", False, "udm"), ("x = 1", False, "icm"), ("x = 100", True, None)],
)
def test_check_object(sct, stu_code, passes, msg):
    output = helper.run({"DC_SOLUTION": "x = 100", "DC_CODE": stu_code, "DC_SCT": sct})
    assert output["correct"] == passes
    if msg:
        assert output["message"] == msg


@pytest.mark.parametrize(
    "stu_code, passes",
    [
        ("x = filter(lambda x: x > 0, [0, 1])", False),
        ("x = filter(lambda x: x > 0, [1, 1])", True),
    ],
)
def test_check_object_exotic_compare(stu_code, passes):
    output = helper.run(
        {
            "DC_SOLUTION": "x = filter(lambda x: x > 0, [1, 1])",
            "DC_SCT": "Ex().check_object('x').has_equal_value()",
            "DC_CODE": stu_code,
        }
    )
    assert output["correct"] == passes


@pytest.mark.parametrize(
    "stu_code, passes",
    [
        ("x = (np.array([1, 2]), np.array([1, 2]))", False),
        ("x = (np.array([1, 2]), np.array([3, 4]))", True),
    ],
)
def test_check_object_exotic_compare2(stu_code, passes):
    output = helper.run(
        {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "x = (np.array([1, 2]), np.array([3, 4]))",
            "DC_SCT": "Ex().check_object('x').has_equal_value()",
            "DC_CODE": stu_code,
        }
    )
    assert output["correct"] == passes


@pytest.mark.parametrize(
    "stu_code, passes", [("x = [1, 2, 3]", True), ("x = [1, 2, 3, 4]", False)]
)
def test_check_object_custom_compare(stu_code, passes):
    output = helper.run(
        {
            "DC_SOLUTION": "x = [4, 5, 6]",
            "DC_CODE": stu_code,
            "DC_SCT": 'Ex().check_object("x").has_equal_value(func = lambda x,y: len(x) == len(y))',
        }
    )
    assert output["correct"] == passes


def test_check_object_single_process():
    state1pid = setup_state("x = 3", "", pid=1)
    helper.passes(state1pid.check_object("x"))


@pytest.mark.parametrize(
    "stu_code, passes", [("arr = 4", False), ("arr = np.array([1])", True)]
)
def test_is_instance(stu_code, passes):
    output = helper.run(
        {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "arr = np.array([1, 2, 3, 4])",
            "DC_SCT": "import numpy; Ex().check_object('arr').is_instance(numpy.ndarray)",
            "DC_CODE": stu_code,
        }
    )
    assert output["correct"] == passes


@pytest.mark.parametrize(
    "sct",
    [
        "test_data_frame('df', columns=['a'], undefined_msg='udm', not_data_frame_msg='ndfm', undefined_cols_msg='ucm', incorrect_msg='icm')",
        "test_data_frame('df', columns=None, undefined_msg='udm', not_data_frame_msg='ndfm', undefined_cols_msg='ucm', incorrect_msg='icm')",
        """
import pandas as pd
Ex().check_object('df', missing_msg='udm', expand_msg='').\
     is_instance(pd.DataFrame, not_instance_msg='ndfm').\
     check_keys('a', missing_msg='ucm').has_equal_value(incorrect_msg='icm')
    """,
        """
import pandas as pd
Ex().check_df('df', missing_msg='udm', expand_msg='', not_instance_msg='ndfm').\
     check_keys('a', missing_msg='ucm').has_equal_value(incorrect_msg='icm')
    """,
    ],
)
@pytest.mark.parametrize(
    "stu_code, passes, msg",
    [
        ("", False, "udm"),
        ("df = 3", False, "ndfm"),
        ('df = pd.DataFrame({ "b": [1]})', False, "ucm"),
        ('df = pd.DataFrame({ "a": [1]})', False, "icm"),
        ('df = pd.DataFrame({ "a": [1, 2, 3] })', True, None),
        ('df = pd.DataFrame({ "a": [1, 2, 3], "b": [3, 4, 5] })', True, None),
    ],
)
def test_test_data_frame(sct, stu_code, passes, msg):
    output = helper.run(
        {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": 'df = pd.DataFrame({"a": [1, 2, 3]})',
            "DC_CODE": stu_code,
            "DC_SCT": sct,
        }
    )
    assert output["correct"] == passes
    if msg:
        assert output["message"] == msg


@pytest.mark.parametrize(
    "stu_code, passes",
    [
        ("x = {}", False),
        ('x = {"b": 3}', False),
        ('x = {"a": 3}', False),
        ('x = {"a": 2}', True),
        ('x = {"a": 2, "b": 3}', True),
    ],
)
def test_check_keys(stu_code, passes):
    output = helper.run(
        {
            "DC_SOLUTION": 'x = {"a": 2}',
            "DC_CODE": stu_code,
            "DC_SCT": 'Ex().check_object("x").check_keys("a").has_equal_value()',
        }
    )
    assert output["correct"] == passes


@pytest.mark.parametrize(
    "sct",
    [
        "Ex().test_data_frame('pivot')",
        "Ex().check_df('pivot').check_keys(('visitors', 'Austin')).has_equal_value()",
    ],
)
def test_check_keys_exotic(sct):
    code = "pivot = users.pivot(index='weekday', columns='city')"
    output = helper.run(
        {
            "DC_PEC": """
import pandas as pd
users = pd.read_csv('https://s3.amazonaws.com/assets.datacamp.com/production/course_1650/datasets/users.csv')
""",
            "DC_SOLUTION": code,
            "DC_CODE": code,
            "DC_SCT": sct,
        }
    )
    assert output["correct"]


def test_non_dillable():
    # xlrd and openpyxl needed for Excel support
    code = "xl = pd.ExcelFile('battledeath.xlsx')"
    res = helper.run(
        {
            "DC_PEC": "import pandas as pd; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/battledeath.xlsx', 'battledeath.xlsx')",
            "DC_SOLUTION": code,
            "DC_CODE": code,
            "DC_SCT": "Ex().check_object('xl').has_equal_value()",
        }
    )
    assert res["correct"]


@pytest.mark.compiled
def test_manual_converter():
    res = helper.run(
        {
            "DC_CODE": "xl = pd.ExcelFile('battledeath2.xlsx')",
            "DC_SOLUTION": "xl = pd.ExcelFile('battledeath.xlsx')",
            "DC_PEC": "import pandas as pd; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/battledeath.xlsx', 'battledeath.xlsx'); from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/battledeath.xlsx', 'battledeath2.xlsx')",
            "DC_SCT": """
def my_converter(x): return(x.sheet_names)
set_converter(key = "pandas.io.excel.ExcelFile", fundef = my_converter)
Ex().check_object('xl').has_equal_value()
""",
        }
    )
    assert res["correct"]


from pythonwhat.State import set_converter


def test_manual_converter_2():
    s = setup_state(
        stu_code="my_array = np.array([[0,0], [0,0], [0,0]])",
        sol_code="my_array = np.array([[1,2], [3,4], [5,6]])",
        pec="import numpy as np",
    )
    set_converter(key="numpy.ndarray", fundef=lambda x: x.shape)
    s.check_object("my_array").has_equal_value()


@pytest.mark.parametrize(
    "stu, sol",
    [
        ("x = 2", "import numpy as np; x = np.mean([1, 2, 3])"),
        ("x = 2", "x = 2.0"),
        ("x = None", "x = None"),
    ],
)
def test_equality_challenges(stu, sol):
    s = setup_state(stu, sol)
    s.check_object("x").has_equal_value()


def test_equality_challenge_2():
    code = "mat = scipy.io.loadmat('albeck_gene_expression.mat')"
    res = helper.run(
        {
            "DC_CODE": code,
            "DC_SOLUTION": code,
            "DC_PEC": "import scipy.io; from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/ja_data2.mat', 'albeck_gene_expression.mat')",
            "DC_SCT": "Ex().check_object('mat').has_equal_value()",
        }
    )
    assert res["correct"]


@pytest.mark.parametrize(
    "name, ls, le, cs, ce",
    [
        ("a", 3, 3, 5, 9),
        ("c", 8, 8, 5, 9),
        ("d", 11, 11, 5, 9),
        ("e", 15, 15, 5, 9),
        ("f", 19, 19, 5, 9),
        ("g", 24, 24, 5, 9),
        ("h", 28, 28, 5, 9),
        ("i", 0, 0, 0, 0),
    ],
)
def test_parsing(name, ls, le, cs, ce):
    stu_code = """
if True:
    a = 1

if False:
    b = 2
else:
    c = 3

for i in range(2):
    d = 4

x = 2
while x > 0:
    e = 5
    x -= 1

try:
    f = 6
except:
    pass

try:
    g = 7
except:
    pass
finally:
    h = 8

# 2 assignments
i = 9
if True:
    i = 9
"""
    sol_code = """
if True:
    a = 10

if False:
    b = 20
else:
    c = 30

for i in range(2):
    d = 40

x = 2
while x > 0:
    e = 50
    x -= 1

try:
    f = 60
except:
    pass

try:
    g = 70
except:
    pass
finally:
    h = 80

# 2 assignments
i = 90
if True:
    i = 90
"""
    res = helper.run(
        {
            "DC_CODE": stu_code,
            "DC_SOLUTION": sol_code,
            "DC_SCT": 'Ex().check_object("%s").has_equal_value()' % name,
        }
    )
    assert not res["correct"]
    if name == "i":
        helper.no_line_info(res)
    else:
        helper.with_line_info(res, ls, le, cs, ce)


@pytest.fixture()
def diff_assign_data():
    return {
        "DC_CODE": """
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df.columns = ["c", "d"]

df2 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df2.columns = ["e", "f"]
            """,
        "DC_SOLUTION": """
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df.columns = ["c", "d"]

df2 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df2.columns = ["c", "d"]
            """,
    }


def test_several_assignments(diff_assign_data):
    res = helper.run(
        {**diff_assign_data, "DC_SCT": "Ex().check_object('df').has_equal_value()"}
    )
    assert res["correct"]


def test_several_assignments_2(diff_assign_data):
    res = helper.run(
        {**diff_assign_data, "DC_SCT": "Ex().check_object('df2').has_equal_value()"}
    )
    assert not res["correct"]
    helper.no_line_info(res)


# Object Assignment parser -------------------------------------------------------------

from pythonwhat.parsing import ObjectAssignmentParser
import ast


@pytest.mark.parametrize(
    "code",
    [
        "x = 2",
        "x = a[1]",
        "x = a.b[1]",
        'x = sales.loc[(["ca", "tx"], 2), :]',
        "x = fun(a)",
        "x = a + b",
        "x = (a + b) + c",
        "x = [ a for b in c ]",
    ],
)
def test_object_assignment_parser(code):
    p = ObjectAssignmentParser()
    p.visit(ast.parse(code))
    assert "x" in p.out
