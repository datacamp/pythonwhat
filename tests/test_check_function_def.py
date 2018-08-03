import pytest
import helper

@pytest.mark.parametrize('stu, passes', [
    ('', False),
    ('def test(): print(3)', False),
    ('def test(x): pass', False),
    ('def test(x): print(x + 2)', False),
    ('def test(x): print(x)', True)
])
def test_check_function_def_basic(stu, passes):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'def test(x): print(x)',
        'DC_SCT': '''
Ex().check_function_def('test').multi(
    check_args(0),
    check_body().set_context(1).check_function('print').check_args(0).has_equal_value()
)
'''
    })
    assert output['correct'] == passes

@pytest.mark.parametrize('stu, passes', [
    ('def test(a, b): return 1', False),
    ('def test(a, b): return a + b', False),
    ('''
def test(a, b):
    if a == 3:
        raise ValueError('wrong')
    print(a + b)
    return a + b
''', False),
    ('def test(a, b): print(int(a) + int(b)); return int(a) + int(b)', False),
    ('def test(a, b): print(a + b); return a + b', True)
])
def test_check_call(stu, passes):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'def test(a, b): print(a + b); return a + b',
        'DC_SCT': """
Ex().check_function_def('test').multi(
    check_call("f(1,2)").has_equal_value(),
    check_call("f(1,2)").has_equal_output(),
    check_call("f(3,1)").has_equal_value(),
    check_call("f(1, '2')").has_equal_error()
)
"""})
    assert output['correct'] == passes

@pytest.mark.parametrize('stu, passes', [
    ('lambda a,b: 1', False),
    ('lambda a,b: a + b', True)
])
def test_check_call_lambda(stu, passes):
    output = helper.run({
        'DC_CODE': stu,
        'DC_SOLUTION': 'lambda a, b: a + b',
        'DC_SCT': """
Ex().check_lambda_function().multi(
    check_call("f(1,2)").has_equal_value(),
    check_call("f(1,2)").has_equal_output()
)
"""})
    assert output['correct'] == passes

def test_check_call_error_types():
    output = helper.run({
        'DC_CODE': 'def test(): raise ValueError("boooo")',
        'DC_SOLUTION': 'def test(): raise NameError("boooo")',
        'DC_SCT': 'Ex().check_function_def("test").check_call("f()").has_equal_error()'
    })
    assert output['correct']