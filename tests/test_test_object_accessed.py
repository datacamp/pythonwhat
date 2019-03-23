import pytest
import tests.helper as helper


@pytest.mark.parametrize(
    "sct, passes, mess",
    [
        ('test_object_accessed("arr")', True, None),
        ('test_object_accessed("ar")', False, None),
        ('test_object_accessed("arr", times=2)', True, None),
        (
            'test_object_accessed("arr", times=3)',
            False,
            "Have you accessed <code>arr</code> at least three times?",
        ),
        (
            'test_object_accessed("arr", times=3, not_accessed_msg="silly")',
            False,
            "silly",
        ),
        ('test_object_accessed("arr.shape")', True, None),
        (
            'test_object_accessed("arr.shape", times=2)',
            False,
            "Have you accessed <code>arr.shape</code> at least twice?",
        ),
        (
            'test_object_accessed("arr.shape", times=2, not_accessed_msg="silly")',
            False,
            "silly",
        ),
        (
            'test_object_accessed("arr.dtype")',
            False,
            "Have you accessed <code>arr.dtype</code>?",
        ),
        ('test_object_accessed("arr.dtype", not_accessed_msg="silly")', False, "silly"),
        ('test_object_accessed("math.e")', True, None),
        (
            'test_object_accessed("math.pi")',
            False,
            "Have you accessed <code>m.pi</code>?",
        ),
        ('test_object_accessed("math.pi", not_accessed_msg="silly")', False, "silly"),
    ],
)
def test_test_object_accessed(sct, passes, mess):
    res = helper.run(
        {
            "DC_CODE": """
import numpy as np
import math as m
arr = np.array([1, 2, 3])
x = arr.shape
print(arr.data)
print(m.e)
            """,
            "DC_SOLUTION": "# not used",
            "DC_SCT": sct,
        }
    )
    assert res["correct"] == passes
    if mess:
        assert res["message"] == mess


# ObjectAccess parser -------------------------------------------------------------

from pythonwhat.parsing import ObjectAccessParser
import ast


@pytest.mark.parametrize(
    "code",
    ["x.a[1]", "x.a", "print(x.a)", "print(kw = x.a)", "(x.a, y.a)", "[x.a, y.a]"],
)
def test_object_access_parser(code):
    p = ObjectAccessParser()
    p.visit(ast.parse(code))
    assert "x.a" in p.out
