import pytest
import helper
from pythonwhat.Reporter import Reporter

def message(output, patt):
    return Reporter.to_html(patt) == output['message']

def lines(output, s, e):
    if s and e:
        return output['column_start'] == s and output['column_end'] == e
    else:
        return True

@pytest.mark.parametrize('stu, patt, cols, cole', [
        ('', 'Did you call `round()`?', None, None),
        ('round(1)', 'Check your call of `round()`. Did you specify the second argument?', 1, 8),
        ('round(1, a)', 'Check your call of `round()`. Did you correctly specify the second argument? Running it generated an error: `name \'a\' is not defined`.', 10, 10),
        ('round(1, 2)', 'Check your call of `round()`. Did you correctly specify the second argument? Expected `3`, but got `2`.', 10, 10)
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

@pytest.mark.parametrize('stu, patt', [
    ('', 'Did you call `round()`?'),
    ('round(1)', 'Did you call `round()` twice?'),
    ('round(1)\nround(5)', 'Check your second call of `round()`. Did you correctly specify the first argument? Expected `2`, but got `5`.'),
    ('round(1)\nround(2)', 'Did you call `round()` 3 times?'),
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