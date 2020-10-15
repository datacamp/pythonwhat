import pytest
import tests.helper as helper
from protowhat.Reporter import Reporter
from difflib import Differ


def message(output, patt):
    return Reporter.to_html(patt) == output["message"]


def lines(output, s, e):
    if s and e:
        return output["column_start"] == s and output["column_end"] == e
    else:
        return True


# Check Function Call ---------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        ("", "Did you call `round()`?", None, None),
        (
            "round(1)",
            "Check your call of `round()`. Did you specify the second argument?",
            1,
            8,
        ),
        (
            "round(1, a)",
            "Check your call of `round()`. Did you correctly specify the second argument? Running it generated an error: `name 'a' is not defined`.",
            10,
            10,
        ),
        (
            "round(1, 2)",
            "Check your call of `round()`. Did you correctly specify the second argument? Expected `3`, but got `2`.",
            10,
            10,
        ),
        (
            "round(1, ndigits = 2)",
            "Check your call of `round()`. Did you correctly specify the second argument? Expected `3`, but got `2`.",
            10,
            20,
        ),
    ],
)
def test_check_function_pos(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "round(1, 3)",
            "DC_SCT": 'Ex().check_function("round").check_args(1).has_equal_value()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "round(1)",
            "Check your call of `round()`. Did you specify the argument `ndigits`?",
            1,
            8,
        ),
        (
            "round(1, a)",
            "Check your call of `round()`. Did you correctly specify the argument `ndigits`? Running it generated an error: `name 'a' is not defined`.",
            10,
            10,
        ),
        (
            "round(1, 2)",
            "Check your call of `round()`. Did you correctly specify the argument `ndigits`? Expected `3`, but got `2`.",
            10,
            10,
        ),
    ],
)
def test_check_function_named(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "round(1, 3)",
            "DC_SCT": 'Ex().check_function("round").check_args("ndigits").has_equal_value()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "round(3)",
            "Check your call of `round()`. Did you correctly specify the first argument? Expected `2`, but got `3`.",
            7,
            7,
        ),
        (
            "round(1 + 1)",
            "Check your call of `round()`. Did you correctly specify the first argument? Expected `2`, but got `1 + 1`.",
            7,
            11,
        ),
    ],
)
def test_check_function_ast(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "round(2)",
            "DC_SCT": 'Ex().check_function("round").check_args(0).has_equal_ast()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            'list("wrong")',
            'Check your call of `list()`. Did you correctly specify the first argument? Expected `"test"`, but got `"wrong"`.',
            6,
            12,
        ),
        (
            'list("te" + "st")',
            'Check your call of `list()`. Did you correctly specify the first argument? Expected `"test"`, but got `"te" + "st"`.',
            6,
            16,
        ),
    ],
)
def test_check_function_ast2(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": 'list("test")',
            "DC_SCT": 'Ex().check_function("list", signature = False).check_args(0).has_equal_ast()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "round(a)",
            "Check your call of `round()`. Did you correctly specify the first argument? Expected `b`, but got `a`.",
            7,
            7,
        ),
        (
            "round(b + 1 - 1)",
            "Check your call of `round()`. Did you correctly specify the first argument? Expected `b`, but got `b + 1 - 1`.",
            7,
            15,
        ),
    ],
)
def test_check_function_ast3(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_PEC": "a = 3\nb=3",
            "DC_CODE": stu,
            "DC_SOLUTION": "round(b)",
            "DC_SCT": 'Ex().check_function("round", signature = False).check_args(0).has_equal_ast()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("import pandas as pd", "Did you call `pd.DataFrame()`?"),
        ("import pandas as pad", "Did you call `pad.DataFrame()`?"),
    ],
)
def test_check_function_pkg1(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "import pandas as pd; pd.DataFrame({'a': [1, 2, 3]})",
            "DC_CODE": stu,
            "DC_SCT": "test_function_v2('pandas.DataFrame')",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("import numpy as nump", "Did you call `nump.random.rand()`?"),
        ("from numpy.random import rand as r", "Did you call `r()`?"),
    ],
)
def test_check_function_pkg2(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "import numpy as np; x = np.random.rand(1)",
            "DC_CODE": stu,
            "DC_SCT": "test_function_v2('numpy.random.rand')",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("", "Did you call `round()`?"),
        ("round(1)", "Did you call `round()` twice?"),
        (
            "round(1)\nround(5)",
            "Check your second call of `round()`. Did you correctly specify the first argument? Expected `2`, but got `5`.",
        ),
        ("round(1)\nround(2)", "Did you call `round()` three times?"),
        (
            "round(1)\nround(2)\nround(5)",
            "Check your third call of `round()`. Did you correctly specify the first argument? Expected `3`, but got `5`.",
        ),
    ],
)
def test_multiple_check_functions(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "round(1)\nround(2)\nround(3)",
            "DC_SCT": 'Ex().multi([ check_function("round", index=i).check_args(0).has_equal_value() for i in range(3) ])',
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "df.groupby('a')",
            "Check your call of `df.groupby()`. Did you correctly specify the first argument? Expected `'b'`, but got `'a'`.",
            12,
            14,
        ),
        (
            "df.groupby('b').a.value_counts()",
            "Check your call of `df.groupby.a.value_counts()`. Did you specify the argument `normalize`?",
            1,
            32,
        ),
        (
            "df[df.b == 'x'].groupby('b').a.value_counts()",
            "Check your call of `df.groupby.a.value_counts()`. Did you specify the argument `normalize`?",
            1,
            45,
        ),
    ],
)
def test_check_method(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_PEC": "import pandas as pd; df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'x', 'y']})",
            "DC_CODE": stu,
            "DC_SOLUTION": "df.groupby('b').a.value_counts(normalize = True)",
            "DC_SCT": """
from pythonwhat.signatures import sig_from_obj
import pandas as pd
Ex().check_function('df.groupby').check_args(0).has_equal_ast()
Ex().check_function('df.groupby.a.value_counts', signature = sig_from_obj(pd.Series.value_counts)).check_args('normalize').has_equal_ast()
        """,
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


# Check Object ----------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        ("", "Did you define the variable `x` without errors?", None, None),
        (
            "x = 2",
            "Did you correctly define the variable `x`? Expected `5`, but got `2`.",
            1,
            5,
        ),
    ],
)
def test_check_object(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "x = 5",
            "DC_SCT": 'Ex().check_object("x").has_equal_value()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "sct",
    [
        "test_data_frame('df', columns=['a'])",
        "import pandas as pd; Ex().check_object('df', typestr = 'pandas DataFrame').is_instance(pd.DataFrame).check_keys('a').has_equal_value()",
    ],
)
@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "df = 3",
            "Did you correctly define the pandas DataFrame `df`? Is it a DataFrame?",
            1,
            6,
        ),
        (
            'df = pd.DataFrame({"b": [1]})',
            "Did you correctly define the pandas DataFrame `df`? There is no column `'a'`.",
            1,
            29,
        ),
        (
            'df = pd.DataFrame({"a": [1]})',
            "Did you correctly define the pandas DataFrame `df`? Did you correctly set the column `'a'`? Expected something different.",
            1,
            29,
        ),
        (
            'y = 3; df = pd.DataFrame({"a": [1]})',
            "Did you correctly define the pandas DataFrame `df`? Did you correctly set the column `'a'`? Expected something different.",
            8,
            36,
        ),
    ],
)
def test_test_data_frame_no_msg(sct, stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": 'df = pd.DataFrame({"a": [1, 2, 3]})',
            "DC_CODE": stu,
            "DC_SCT": sct,
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu_code, patt, cols, cole",
    [
        (
            "x = {}",
            "Did you correctly define the variable `x`? There is no key `'a'`.",
            1,
            6,
        ),
        (
            'x = {"b": 3}',
            "Did you correctly define the variable `x`? There is no key `'a'`.",
            1,
            12,
        ),
        (
            'x = {"a": 3}',
            "Did you correctly define the variable `x`? Did you correctly set the key `'a'`? Expected `2`, but got `3`.",
            1,
            12,
        ),
        (
            'y = 3; x = {"a": 3}',
            "Did you correctly define the variable `x`? Did you correctly set the key `'a'`? Expected `2`, but got `3`.",
            8,
            19,
        ),
    ],
)
def test_check_keys(stu_code, patt, cols, cole):
    output = helper.run(
        {
            "DC_SOLUTION": 'x = {"a": 2}',
            "DC_CODE": stu_code,
            "DC_SCT": 'Ex().check_object("x").check_keys("a").has_equal_value()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("round(2.34)", "argrwong"),
        ("round(1.23)", "objectnotdefined"),
        ("x = round(1.23) + 1", "objectincorrect"),
    ],
)
def test_check_object_manual(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "x = round(1.23)",
            "DC_SCT": """
Ex().check_function('round').check_args(0).has_equal_value(incorrect_msg = 'argrwong')
Ex().check_object('x', missing_msg='objectnotdefined').has_equal_value('objectincorrect')
""",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


# Check function def et al ----------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        (
            "",
            "The system wants to check the definition of `test()` but hasn't found it.",
        ),
        (
            "def test(b): return b",
            "Check the definition of `test()`. Did you specify the argument `a`?",
        ),
        (
            "def test(a): return a",
            "Check the definition of `test()`. Did you correctly specify the argument `a`? not default",
        ),
        (
            "def test(a = 2): return a",
            "Check the definition of `test()`. Did you correctly specify the argument `a`? Expected `1`, but got `2`.",
        ),
    ],
)
def test_check_function_def(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "def test(a = 1): return a",
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_function_def('test').check_args('a').has_equal_part('is_default', msg='not default').has_equal_value()",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


# Check call ------------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        (
            "",
            "The system wants to check the definition of `test()` but hasn't found it.",
        ),
        (
            "def test(a, b): return 1",
            "Check the definition of `test()`. To verify it, we reran `test(1, 2)`. Expected `3`, but got `1`.",
        ),
        (
            "def test(a, b): return a + b",
            "Check the definition of `test()`. To verify it, we reran `test(1, 2)`. Expected the output `3`, but got `no printouts`.",
        ),
        (
            """
def test(a, b):
    if a == 3:
        raise ValueError('wrong')
    print(a + b)
    return a + b
""",
            "Check the definition of `test()`. To verify it, we reran `test(3, 1)`. Running the highlighted expression generated an error: `wrong`.",
        ),
        (
            "def test(a, b): print(int(a) + int(b)); return int(a) + int(b)",
            'Check the definition of `test()`. To verify it, we reran `test(1, "2")`. Running the highlighted expression didn\'t generate an error, but it should!',
        ),
    ],
)
def test_check_call(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "def test(a, b): print(a + b); return a + b",
            "DC_SCT": """
Ex().check_function_def('test').multi(
    check_call('f(1, 2)').has_equal_value(),
    check_call('f(1, 2)').has_equal_output(),
    check_call('f(3, 1)').has_equal_value(),
    check_call('f(1, "2")').has_equal_error()
)""",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt",
    [
        (
            "echo_word = (lambda word1, echo: word1 * echo * 2)",
            "Check the first lambda function. To verify it, we reran it with the arguments `('test', 2)`. Expected `'testtest'`, but got `'testtesttesttest'`.",
        )
    ],
)
def test_check_call_lambda(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "echo_word = (lambda word1, echo: word1 * echo)",
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_lambda_function().check_call(\"f('test', 2)\").has_equal_value()",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


# Check class definition ------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        (
            "",
            "The system wants to check the class definition of `A` but hasn't found it.",
        ),
        (
            "def A(x): pass",
            "The system wants to check the class definition of `A` but hasn't found it.",
        ),
        (
            "class A(): pass",
            "Check the class definition of `A`. Are you sure you defined the first base class?",
        ),
        (
            "class A(int): pass",
            "Check the class definition of `A`. Did you correctly specify the first base class? Expected `str`, but got `int`.",
        ),
        (
            "class A(str):\n  def __not_init__(self): pass",
            "Check the class definition of `A`. Did you correctly specify the body? The system wants to check the definition of `__init__()` but hasn't found it.",
        ),
        (
            "class A(str):\n  def __init__(self): print(1)",
            "Check the definition of `__init__()`. Did you correctly specify the body? Expected `pass`, but got `print(1)`.",
        ),
    ],
)
def test_check_class_def_pass(stu, patt):
    sol = "class A(str):\n  def __init__(self): pass"
    output = helper.run(
        {
            "DC_SOLUTION": sol,
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_class_def('A').multi( check_bases(0).has_equal_ast(), check_body().check_function_def('__init__').check_body().has_equal_ast() )",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


## has_import -----------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("", "Did you import `pandas`?"),
        ("import pandas", "Did you import `pandas` as `pd`?"),
        ("import pandas as pan", "Did you import `pandas` as `pd`?"),
    ],
)
def test_has_import(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "import pandas as pd",
            "DC_SCT": "Ex().has_import('pandas', same_as=True)",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt",
    [("", "wrong"), ("import pandas", "wrongas"), ("import pandas as pan", "wrongas")],
)
def test_has_import_custom(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "import pandas as pd",
            "DC_SCT": "Ex().has_import('pandas', same_as=True, not_imported_msg='wrong', incorrect_as_msg='wrongas')",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


## Check has_equal_x ----------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "my_dict = {'a': 1, 'b': 2}\nfor key, value in my_dict.items(): x = key + ' -- ' + str(value)",
            "Check the first for loop. Did you correctly specify the body? Are you sure you assigned the correct value to `x`?",
            36,
            64,
        ),
        (
            "my_dict = {'a': 1, 'b': 2}\nfor key, value in my_dict.items(): x = key + ' - ' + str(value)",
            "Check the first for loop. Did you correctly specify the body? Expected the output `a - 1`, but got `no printouts`.",
            36,
            63,
        ),
    ],
)
def test_has_equal_x(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_SOLUTION": "my_dict = {'a': 1, 'b': 2}\nfor key, value in my_dict.items():\n    x = key + ' - ' + str(value)\n    print(x)",
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_for_loop().check_body().set_context('a', 1).multi(has_equal_value(name = 'x'), has_equal_output())",
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "result = (num for num in range(3))",
            "Check the first generator expression. Did you correctly specify the iterable part? Expected `range(0, 31)`, but got `range(0, 3)`.",
            26,
            33,
        ),
        (
            "result = (num*2 for num in range(31))",
            "Check the first generator expression. Did you correctly specify the body? Expected `4`, but got `8`.",
            11,
            15,
        ),
    ],
)
def test_has_equal_x_2(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_SOLUTION": "result = (num for num in range(31))",
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_generator_exp().multi(check_iter().has_equal_value(), check_body().set_context(4).has_equal_value())",
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


def test_has_equal_value_wrap_string():
    sol = """print(' , ')"""
    stu = """print(', ')"""
    sct = """Ex().check_function('print', index=0, signature=False).check_args(0).has_equal_value(copy = False)"""
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": sol,
            "DC_SCT": sct,
        }
    )
    assert not output["correct"]
    assert output["message"] == "Check your call of <code>print()</code>. Did you correctly specify the first argument? Expected <code>' , '</code>, but got <code>', '</code>."  # nopep8


## Testing output edge cases -------------------------------------------------


def test_has_equal_value_dont_wrap_newline():
    sol = """print('\\n')"""
    stu = """print('text')"""
    sct = """Ex().check_function('print', index=0, signature=False).check_args(0).has_equal_value()"""
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": sol,
            "DC_SCT": sct,
        }
    )
    assert not output["correct"]
    assert output["message"] == "Check your call of <code>print()</code>. Did you correctly specify the first argument? Expected something different."  # nopep8


def test_has_equal_value_shorten_submission():
    sol = """print('short text')"""
    stu = """print('This text is longer than 50 characters if I copy it 3 times. This text is longer than 50 characters if I copy it 3 times. This text is longer than 50 characters if I copy it 3 times.')"""  # nopep8
    sct = """Ex().check_function('print', index=0, signature=False).check_args(0).has_equal_value()"""
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": sol,
            "DC_SCT": sct,
        }
    )
    assert not output["correct"]
    assert output["message"] == "Check your call of <code>print()</code>. Did you correctly specify the first argument? Expected <code>'short text'</code>, but got <code>'This text is longer than 50 characters if I ...</code>."  # nopep8


def test_has_equal_value_dont_shorten_solution():
    sol = """print('This solution is really really really really really really really really long!')"""
    stu = """print('short text')"""  # nopep8
    sct = """Ex().check_function('print', index=0, signature=False).check_args(0).has_equal_value()"""
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": sol,
            "DC_SCT": sct,
        }
    )
    assert not output["correct"]
    assert output["message"] == "Check your call of <code>print()</code>. Did you correctly specify the first argument? Expected something different."  # nopep8

## Check has no error ---------------------------------------------------------


def test_has_no_error():
    output = helper.run(
        {"DC_CODE": "c", "DC_SOLUTION": "", "DC_SCT": "Ex().has_no_error()"}
    )
    assert not output["correct"]
    assert message(
        output,
        "Have a look at the console: your code contains an error. Fix it and try again!",
    )


## test_correct ---------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("", "Did you define the variable `a` without errors?"),
        ("a = 1", "Did you define the variable `b` without errors?"),
        ("a = 1; b = a + 1", "Did you define the variable `c` without errors?"),
        (
            "a = 1; b = a + 1; c = b + 1",
            "Have you used `print(c)` to do the appropriate printouts?",
        ),
        ("print(4)", "Did you define the variable `a` without errors?"),
        (
            "c = 3; print(c + 1)",
            "Have you used `print(c)` to do the appropriate printouts?",
        ),
        (
            "b = 3; c = b + 1; print(c)",
            "Did you define the variable `a` without errors?",
        ),
        (
            "a = 2; b = a + 1; c = b + 1",
            "Did you correctly define the variable `a`? Expected `1`, but got `2`.",
        ),
    ],
)
def test_nesting(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "a = 1; b = a + 1; c = b + 1; print(c)",
            "DC_CODE": stu,
            "DC_SCT": """
Ex().test_correct(
    has_printout(0),
    F().test_correct(
        check_object('c').has_equal_value(),
        F().test_correct(
            check_object('b').has_equal_value(),
            check_object('a').has_equal_value()
        )
    )
)
        """,
        }
    )
    assert not output["correct"]
    assert message(output, patt)


## test limited stacking ------------------------------------------------------


@pytest.mark.parametrize(
    "sct, patt",
    [
        (
            "Ex().check_for_loop().check_body().check_for_loop().check_body().has_equal_output()",
            "Check the first for loop. Did you correctly specify the body? Expected the output `1+1`, but got `1-1`.",
        ),
        (
            "Ex().check_for_loop().check_body().check_for_loop().disable_highlighting().check_body().has_equal_output()",
            "Check the first for loop. Did you correctly specify the body? Check the first for loop. Did you correctly specify the body? Expected the output `1+1`, but got `1-1`.",
        ),
    ],
)
def test_limited_stacking(sct, patt):
    code = """
for i in range(2):
    for j in range(2):
        print(str(i) + "%s" + str(j))
"""
    output = helper.run(
        {"DC_CODE": code % "-", "DC_SOLUTION": code % "+", "DC_SCT": sct}
    )
    assert not output["correct"]
    assert message(output, patt)


# test has_expr --------------------------------------------------------------


@pytest.mark.parametrize(
    "sct, patt",
    [
        (
            "Ex().check_object('x').has_equal_value()",
            "Did you correctly define the variable `x`? Expected `[1]`, but got `[0]`.",
        ),
        (
            "Ex().has_equal_value(name = 'x')",
            "Are you sure you assigned the correct value to `x`?",
        ),
        (
            "Ex().has_equal_value(expr_code = 'x[0]')",
            "Running the expression `x[0]` didn't generate the expected result.",
        ),
    ],
)
def test_has_expr(sct, patt):
    output = helper.run({"DC_SOLUTION": "x = [1]", "DC_CODE": "x = [0]", "DC_SCT": sct})
    assert not output["correct"]
    assert message(output, patt)


def test_has_expr_replace_focus():
    # Given
    sct = "Ex().check_if_else().check_test().has_equal_value(expr_code = '__focus__ == \\'valid\\'')"
    feedback_msg = "Great work!"

    # When
    output = helper.run(
        {
            "DC_SOLUTION": "u = 'valid'\nif u:\n  print('')",
            "DC_CODE": "u = 'valid'\nif u:\n  print('')",
            "DC_SCT": sct,
        }
    )

    # Then
    assert output["correct"]
    assert message(output, feedback_msg)


def test_has_expr_replace_focus_fail():
    # Given
    sct = "Ex().check_if_else().check_test().has_equal_value(expr_code = '__focus__ == \\'valid\\'')"
    feedback_msg = "Check the first if statement. Did you correctly specify the condition? Running the expression <code>u == 'valid'</code> didn't generate the expected result."  # nopep8

    # When
    output = helper.run(
        {
            "DC_SOLUTION": "u = 'valid'\nif u:\n  print('')",
            "DC_CODE": "u = 'wrong'\nif u:\n  print('')",
            "DC_SCT": sct,
        }
    )

    # Then
    assert not output["correct"]
    assert message(output, feedback_msg)


# check_if_else --------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt, lines",
    [
        (
            "",
            "The system wants to check the first if statement but hasn't found it.",
            [],
        ),
        (
            "if offset > 10: x = 5\nelse: x = round(2.123)",
            "Check the first if statement. Did you correctly specify the condition? Expected <code>True</code>, but got <code>False</code>.",
            [1, 1, 4, 14],
        ),
        (
            "if offset > 8: x = 7\nelse: x = round(2.123)",
            "Check the first if statement. Did you correctly specify the body? Could not find the correct pattern in your code.",
            [1, 1, 16, 20],
        ),
        (
            "if offset > 8: x = 5\nelse: x = 8",
            "Check the first if statement. Did you correctly specify the else part? Did you call <code>round()</code>?",
            [2, 2, 7, 11],
        ),
        (
            "if offset > 8: x = 5\nelse: x = round(2.2121314)",
            "Check your call of <code>round()</code>. Did you correctly specify the first argument? Expected <code>2.123</code>, but got <code>2.2121314</code>.",
            [2, 2, 17, 25],
        ),
    ],
)
def test_check_if_else_basic(stu, patt, lines):
    output = helper.run(
        {
            "DC_PEC": "offset = 8",
            "DC_SOLUTION": "if offset > 8: x = 5\nelse: x = round(2.123)",
            "DC_CODE": stu,
            "DC_SCT": """
Ex().check_if_else().multi(
    check_test().multi([ set_env(offset = i).has_equal_value() for i in range(7,10) ]),
    check_body().has_code(r'x\s*=\s*5'),
    check_orelse().check_function('round').check_args(0).has_equal_value()
)
        """,
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    if lines:
        helper.with_line_info(output, *lines)


## Jinja handling -------------------------------------------------------------


@pytest.mark.parametrize(
    "msgpart",
    [
        "__JINJA__:You did {{stu_eval}}, but should be {{sol_eval}}!",
        "You did {{stu_eval}}, but should be {{sol_eval}}!",
    ],
)
def test_jinja_in_custom_msg(msgpart):
    output = helper.run(
        {
            "DC_SOLUTION": "x = 4",
            "DC_CODE": "x = 3",
            "DC_SCT": "Ex().check_object('x').has_equal_value(incorrect_msg=\"%s\")"
            % msgpart,
        }
    )
    assert not output["correct"]
    assert message(output, "You did 3, but should be 4!")
