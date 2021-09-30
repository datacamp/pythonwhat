import pytest
import tests.helper as helper


@pytest.mark.parametrize(
    "sct, passes, patt, lines",
    [
        (
            "test_with(1, body = lambda: [test_function('print', index = i + 1) for i in range(3)])",
            False,
            "Check your third call of <code>print()</code>. Did you correctly specify the first argument? Expected something different.",
            [6, 6, 11, 16],
        ),
        (
            "test_with(2, body = lambda: test_for_loop(1, body = lambda: test_if_else(1, body = lambda: test_function('print'))))",
            True,
            None,
            None,
        ),
        (
            "test_with(1, body = [test_function('print', index = i + 1) for i in range(3)])",
            False,
            None,
            [6, 6, 11, 16],
        ),
        (
            "test_with(2, body = test_for_loop(1, body = test_if_else(1, body = test_function('print'))))",
            True,
            None,
            None,
        ),
        (
            """
for_test = test_for_loop(1, body = test_if_else(1, body = test_function('print')))
Ex().check_with(1).check_body().with_context(for_test)
        """,
            True,
            None,
            None,
        ),
        (
            "Ex().check_with(0).check_body().with_context([test_function('print', index = i+1) for i in range(3)])",
            False,
            "Check your third call of <code>print()</code>",
            [6, 6, 11, 16],
        ),
        (
            """
# since the print func is being tested w/o SCTs setting any variables, don't need with_context
for_test = test_for_loop(1, body = test_if_else(1, body = test_function('print')))
Ex().check_with(1).check_body().multi(for_test)
        """,
            True,
            None,
            None,
        ),
    ],
)
def test_test_with_1(sct, passes, patt, lines):
    res = helper.run(
        {
            "DC_PEC": """
from urllib.request import urlretrieve; urlretrieve('http://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/moby_opens.txt', 'moby_dick.txt')
        """,
            "DC_CODE": """
# Read & print the first 3 lines
with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readline())
    print('test')

# The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# Print out these rows
with open('moby_dick.txt') as file:
    for i, row in enumerate(file):
        if i in I:
            print(row)
        """,
            "DC_SOLUTION": """
# Read & print the first 3 lines
with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readline())
    print(file.readline())

# The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# Print out these rows
with open('moby_dick.txt') as file:
    for i, row in enumerate(file):
        if i in I:
            print(row)
""",
            "DC_SCT": sct,
        }
    )
    assert res["correct"] == passes
    if patt:
        assert patt in res["message"]
    if lines:
        helper.with_line_info(res, *lines)


@pytest.mark.parametrize(
    "sct, passes, patt, lines",
    [
        (
            "test_with(1, context_vals=True)",
            False,
            "Check the first <code>with</code> statement. Make sure to use the correct number of context variables. It seems you defined too many.",
            [3, 6, 1, 17],
        ),
        (
            "test_with(2, context_vals=True)",
            False,
            "Check the second <code>with</code> statement. Did you correctly specify the first context? Make sure to use the correct context variable names. Was expecting <code>file</code> but got <code>not_file</code>.",
            [12, 15, 1, 22],
        ),
    ],
)
def test_test_with_2(sct, passes, patt, lines):
    res = helper.run(
        {
            "DC_PEC": """
from urllib.request import urlretrieve; urlretrieve('http://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/moby_opens.txt', 'moby_dick.txt')
""",
            "DC_CODE": """
# Read & print the first 3 lines
with open('moby_dick.txt') as file, open('moby_dick.txt'):
    print(file.readline())
    print(file.readline())
    print('test')

# The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# Print out these rows
with open('moby_dick.txt') as not_file:
    for i, row in enumerate(not_file):
        if i in I:
            print(row)
            """,
            "DC_SOLUTION": """
# Read & print the first 3 lines
with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readline())
    print(file.readline())

# The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# Print out these rows
with open('moby_dick.txt') as file:
    for i, row in enumerate(file):
        if i in I:
            print(row)
""",
            "DC_SCT": sct,
        }
    )
    assert res["correct"] == passes
    if patt:
        assert patt in res["message"]
    if lines:
        helper.with_line_info(res, *lines)


@pytest.mark.parametrize(
    "sct, passes, patt, lines",
    [
        ("test_with(1, context_tests=lambda: test_function('open'))", True, None, None),
        (
            """
test_with(1, context_tests=[
    lambda: test_function('open'),
    lambda: test_function('open')])
        """,
            False,
            "Check the first <code>with</code> statement. Make sure to use the correct number of context variables. It seems you defined too little.",
            [3, 6, 1, 17],
        ),
        (
            """
test_with(2, context_tests=[
    lambda: test_function('open'),
    lambda: test_function('open')])
        """,
            False,
            "Check your call of <code>open()</code>.",
            [12, 12, 46, 60],
        ),
    ],
)
def test_test_with_3(sct, passes, patt, lines):
    res = helper.run(
        {
            "DC_PEC": """
from urllib.request import urlretrieve; urlretrieve('http://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/moby_opens.txt', 'moby_dick.txt')
from urllib.request import urlretrieve; urlretrieve('https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/moby_opens.txt', 'not_moby_dick.txt')
        """,
            "DC_CODE": """
# Read & print the first 3 lines
with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readline())
    print('test')

# The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# Print out these rows
with open('moby_dick.txt') as not_file, open('moby_dick.txt') as file:
    for i, row in enumerate(not_file):
        if i in I:
            print(row)
        """,
            "DC_SOLUTION": """
# Read & print the first 3 lines
with open('moby_dick.txt') as file, open('moby_dick.txt'):
    print(file.readline())
    print(file.readline())
    print(file.readline())

# The rows that you wish to print
I = [0,1,3,5,6,7,8,9]

# Print out these rows
with open('moby_dick.txt') as file, open('not_moby_dick.txt') as not_file:
    for i, row in enumerate(file):
        if i in I:
            print(row)
        """,
            "DC_SCT": sct,
        }
    )
    assert res["correct"] == passes
    if patt:
        assert patt in res["message"]
    if lines:
        helper.with_line_info(res, *lines)


@pytest.mark.skip
def test_test_with_destructuring():
    code = """
with A() as (one, *others):
    print(one)
    print(others)
"""
    res = helper.run(
        {
            "DC_PEC": """
class A:
    def __enter__(self): return [1,2, 3]
    def __exit__(self, *args, **kwargs): return
        """,
            "DC_SOLUTION": code,
            "DC_CODE": code,
            "DC_SCT": """
test_with(1, body=[test_function('print'), test_function('print')])
""",
        }
    )
    assert res["correct"]


@pytest.mark.parametrize(
    "sct, stu, passes",
    [
        (
            "Ex().check_with(0).has_context()",
            "with StringIO() as f1, StringIO() as f2: pass",
            True,
        ),
        ("Ex().check_with(0).has_context()", "with StringIO() as f1: pass", False),
        (
            "Ex().check_with(0).has_context(exact_names=True)",
            "with StringIO() as f3, StringIO() as f4: pass",
            False,
        ),
        (
            "Ex().check_with(0).check_context(0).has_context()",
            "with StringIO() as f1, StringIO() as f2: pass",
            True,
        ),
        (
            "Ex().check_with(0).check_context(0).has_context(exact_names=True)",
            "with StringIO() as f3: pass",
            False,
        ),
    ],
)
def test_test_with_has_context(sct, stu, passes):
    res = helper.run(
        {
            "DC_PEC": "from io import StringIO",
            "DC_SOLUTION": "with StringIO() as f1, StringIO() as f2: pass",
            "DC_CODE": stu,
            "DC_SCT": sct,
        }
    )
    assert res["correct"] == passes
