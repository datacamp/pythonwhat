import pytest
import helper
from pythonwhat.Reporter import Reporter
from difflib import Differ

def message(output, patt):
    return Reporter.to_html(patt) == output['message']

def lines(output, s, e):
    if s and e:
        return output['column_start'] == s and output['column_end'] == e
    else:
        return True

# Check Function Call ---------------------------------------------------------

@pytest.mark.parametrize('stu, patt, cols, cole', [
    ('', 'Did you call `round()`?', None, None),
    ('round(1)', 'Check your call of `round()`. Did you specify the second argument?', 1, 8),
    ('round(1, a)', 'Check your call of `round()`. Did you correctly specify the second argument? Running it generated an error: `name \'a\' is not defined`.', 10, 10),
    ('round(1, 2)', 'Check your call of `round()`. Did you correctly specify the second argument? Expected `3`, but got `2`.', 10, 10),
    ('round(1, ndigits = 2)', 'Check your call of `round()`. Did you correctly specify the second argument? Expected `3`, but got `2`.', 10, 20)
])
def test_check_function_pos(stu, patt, cols, cole):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'round(1, 3)',
        'DC_SCT': 'Ex().check_function("round").check_args(1).has_equal_value()'
    })
    assert not output['correct']
    assert message(output, patt)
    assert lines(output, cols, cole)

@pytest.mark.parametrize('stu, patt, cols, cole', [
    ('round(1)', 'Check your call of `round()`. Did you specify the argument `ndigits`?', 1, 8),
    ('round(1, a)', 'Check your call of `round()`. Did you correctly specify the argument `ndigits`? Running it generated an error: `name \'a\' is not defined`.', 10, 10),
    ('round(1, 2)', 'Check your call of `round()`. Did you correctly specify the argument `ndigits`? Expected `3`, but got `2`.', 10, 10)
])
def test_check_function_named(stu, patt, cols, cole):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'round(1, 3)',
        'DC_SCT': 'Ex().check_function("round").check_args("ndigits").has_equal_value()'
    })
    assert not output['correct']
    assert message(output, patt)
    assert lines(output, cols, cole)

@pytest.mark.parametrize('stu, patt, cols, cole', [
    ('round(3)', 'Check your call of `round()`. Did you correctly specify the first argument? Expected `2`, but got `3`.', 7, 7),
    ('round(1 + 1)', 'Check your call of `round()`. Did you correctly specify the first argument? Expected `2`, but got `1 + 1`.', 7, 11)
])
def test_check_function_ast(stu, patt, cols, cole):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'round(2)',
        'DC_SCT': 'Ex().check_function("round").check_args(0).has_equal_ast()'
    })
    assert not output['correct']
    assert message(output, patt)
    assert lines(output, cols, cole)

@pytest.mark.parametrize('stu, patt, cols, cole', [
    ('list("wrong")', 'Check your call of `list()`. Did you correctly specify the first argument? Expected `"test"`, but got `"wrong"`.', 6, 12),
    ('list("te" + "st")', 'Check your call of `list()`. Did you correctly specify the first argument? Expected `"test"`, but got `"te" + "st"`.', 6, 16)
])
def test_check_function_ast2(stu, patt, cols, cole):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'list("test")',
        'DC_SCT': 'Ex().check_function("list", signature = False).check_args(0).has_equal_ast()'
    })
    assert not output['correct']
    assert message(output, patt)
    assert lines(output, cols, cole)

@pytest.mark.parametrize('stu, patt, cols, cole', [
    ('round(a)', 'Check your call of `round()`. Did you correctly specify the first argument? Expected `b`, but got `a`.', 7, 7),
    ('round(b + 1 - 1)', 'Check your call of `round()`. Did you correctly specify the first argument? Expected `b`, but got `b + 1 - 1`.', 7, 15)
])
def test_check_function_ast3(stu, patt, cols, cole):
    output = helper.run({
        'DC_PEC': 'a = 3\nb=3',
        'DC_CODE': stu,
        'DC_SOLUTION': 'round(b)',
        'DC_SCT': 'Ex().check_function("round", signature = False).check_args(0).has_equal_ast()'
    })
    assert not output['correct']
    assert message(output, patt)
    assert lines(output, cols, cole)

@pytest.mark.parametrize('stu, patt', [
    ('import pandas as pd', 'Did you call `pd.DataFrame()`?'),
    ('import pandas as pad', 'Did you call `pad.DataFrame()`?'),
])
def test_check_function_pkg1(stu, patt):
    output = helper.run({
        "DC_SOLUTION": "import pandas as pd; pd.DataFrame({'a': [1, 2, 3]})",
        "DC_CODE": stu,
        "DC_SCT": "test_function_v2('pandas.DataFrame')"
    })
    assert not output['correct']
    assert message(output, patt)

@pytest.mark.parametrize('stu, patt', [
    ('import numpy as nump', 'Did you call `nump.random.rand()`?'),
    ('from numpy.random import rand as r', 'Did you call `r()`?'),
])
def test_check_function_pkg2(stu, patt):
    output = helper.run({
        "DC_SOLUTION": "import numpy as np; x = np.random.rand(1)",
        "DC_CODE": stu,
        "DC_SCT": "test_function_v2('numpy.random.rand')"
    })
    assert not output['correct']
    assert message(output, patt)

@pytest.mark.parametrize('stu, patt', [
    ('', 'Did you call `round()`?'),
    ('round(1)', 'Did you call `round()` twice?'),
    ('round(1)\nround(5)', 'Check your second call of `round()`. Did you correctly specify the first argument? Expected `2`, but got `5`.'),
    ('round(1)\nround(2)', 'Did you call `round()` three times?'),
    ('round(1)\nround(2)\nround(5)', 'Check your third call of `round()`. Did you correctly specify the first argument? Expected `3`, but got `5`.'),
])
def test_multiple_check_functions(stu, patt):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'round(1)\nround(2)\nround(3)',
        'DC_SCT': 'Ex().multi([ check_function("round", index=i).check_args(0).has_equal_value() for i in range(3) ])'
    })
    assert not output['correct']
    assert message(output, patt)

@pytest.mark.debug
@pytest.mark.parametrize('stu, patt, cols, cole', [
    ("df.groupby('a')", "Check your call of `df.groupby()`. Did you correctly specify the first argument? Expected `'b'`, but got `'a'`.", 12, 14),
    ("df.groupby('b').a.value_counts()", 'Check your call of `df.groupby.a.value_counts()`. Did you specify the argument `normalize`?', 1, 32),
    ("df[df.b == 'x'].groupby('b').a.value_counts()", 'Check your call of `df.groupby.a.value_counts()`. Did you specify the argument `normalize`?', 1, 45),
])
def test_check_method(stu, patt, cols, cole):
    output = helper.run({
        'DC_PEC': "import pandas as pd; df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'x', 'y']})",
        'DC_CODE': stu,
        'DC_SOLUTION': "df.groupby('b').a.value_counts(normalize = True)",
        'DC_SCT': """
from pythonwhat.signatures import sig_from_obj
import pandas as pd
Ex().check_function('df.groupby').check_args(0).has_equal_ast()
Ex().check_function('df.groupby.a.value_counts', signature = sig_from_obj(pd.Series.value_counts)).check_args('normalize').has_equal_ast()
        """
    })
    assert not output['correct']
    assert message(output, patt)
    assert lines(output, cols, cole)


# Check Object ----------------------------------------------------------------

@pytest.mark.parametrize('stu, patt, cols, cole', [
    ('', 'Did you define the variable `x` without errors?', None, None),
    ('x = 2', 'Did you correctly define the variable `x`? Expected `5`, but got `2`.', 1, 5)
])
def test_check_object(stu, patt, cols, cole):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'x = 5',
        'DC_SCT': 'Ex().check_object("x").has_equal_value()'
    })
    assert not output['correct']
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize('stu, patt', [
    ('round(2.34)', 'argrwong'),
    ('round(1.23)', 'objectnotdefined'),
    ('x = round(1.23) + 1', 'objectincorrect')
])
def test_check_object_manual(stu, patt):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'x = round(1.23)',
        'DC_SCT': """
Ex().check_function('round').check_args(0).has_equal_value(incorrect_msg = 'argrwong')
Ex().check_object('x', missing_msg='objectnotdefined').has_equal_value('objectincorrect')
"""
    })
    assert not output['correct']
    assert message(output, patt)

# Check call ------------------------------------------------------------------

@pytest.mark.parametrize('stu, patt', [
    ('', 'The system wants to check the definition of `test()` but hasn\'t found it.'),
    ('def test(a, b): return 1', 'Check the definition of `test()`. Calling `test(1, 2)` should return `3`, instead got `1`.'),
    ('def test(a, b): return a + b', 'Check the definition of `test()`. Calling `test(1, 2)` should print out `3`, instead got no printouts.'),
    ('''
def test(a, b):
    if a == 3:
        raise ValueError('wrong')
    print(a + b)
    return a + b
''', 'Check the definition of `test()`. Calling `test(3, 1)` should return `4`, instead it errored out: `wrong`.'),
    ('def test(a, b): print(int(a) + int(b)); return int(a) + int(b)', 'Check the definition of `test()`. Calling `test(1, \'2\')` should error out with the message `unsupported operand type(s) for +: \'int\' and \'str\'`, instead got `3`.'),
])
def test_check_call(stu, patt):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'def test(a, b): print(a + b); return a + b',
        'DC_SCT': """
Ex().check_function_def('test').multi(
    call([1, 2], 'value'),
    call([1, 2], 'output'),
    call([3, 1], 'value'),
    call([1, "2"], 'error')
)
        """
    })
    assert not output['correct']
    assert message(output, patt)

@pytest.mark.parametrize('stu, patt', [
    ('echo_word = (lambda word1, echo: word1 * echo * 2)', "Check the first lambda function. Calling it with the arguments `('test', 2)` should return `testtest`, instead got `testtesttesttest`.")
])
def test_check_call_lambda(stu, patt):
    output = helper.run({
        'DC_SOLUTION': 'echo_word = (lambda word1, echo: word1 * echo)',
        'DC_CODE': stu,
        'DC_SCT': "Ex().check_lambda_function().call(['test', 2], 'value')"
    })
    assert not output['correct']
    assert message(output, patt)

## has_import -----------------------------------------------------------------

@pytest.mark.parametrize('stu, patt', [
    ('', 'Did you import `pandas`?'),
    ('import pandas', 'Did you import `pandas` as `pd`?'),
    ('import pandas as pan', 'Did you import `pandas` as `pd`?')
])
def test_has_import(stu, patt):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'import pandas as pd',
        'DC_SCT': "Ex().has_import('pandas')"
    })
    assert not output['correct']
    assert message(output, patt)

@pytest.mark.parametrize('stu, patt', [
    ('', 'wrong'),
    ('import pandas', 'wrongas'),
    ('import pandas as pan', 'wrongas')
])
def test_has_import_custom(stu, patt):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'import pandas as pd',
        'DC_SCT': "Ex().has_import('pandas', not_imported_msg='wrong', incorrect_as_msg='wrongas')"
    })
    assert not output['correct']
    assert message(output, patt)