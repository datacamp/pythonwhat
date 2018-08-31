import pytest
import helper
from pythonwhat.local import setup_state
from pythonwhat.Test import TestFail as TF
from pythonwhat.Feedback import InstructorError
from inspect import signature
from pythonwhat.check_function import bind_args

@pytest.mark.parametrize('arg, stu', [
        ('a', 'my_fun(1, 10)'),
        ('a', 'my_fun(1, b=10)'),
        ('a', 'my_fun(a = 1, b=10)'),
        ('b', 'my_fun(10, 2)'),
        ('b', 'my_fun(10, b=2)'),
        ('b', 'my_fun(a = 10, b=2)')
    ])
def test_basic_check_function_passing(arg, stu):
    pec = 'def my_fun(a, b): pass'
    sol = 'my_fun(1, 2)'
    s = setup_state(stu_code=stu, sol_code=sol, pec=pec)
    helper.passes(s.check_function('my_fun'))

    helper.passes(s.check_function('my_fun').check_args(arg))
    helper.passes(s.check_function('my_fun').check_args(arg).has_equal_value())

def test_basic_check_function_failing():
    pec = 'def my_fun(a=1): pass'
    sol = 'my_fun(1)'
    s = setup_state(stu_code = '', sol_code=sol, pec=pec)
    with pytest.raises(TF):
        s.check_function('my_fun')

    s = setup_state(stu_code = 'my_fun()', sol_code=sol, pec=pec)
    helper.passes(s.check_function('my_fun'))
    with pytest.raises(TF):
        s.check_function('my_fun').check_args('a')

    s = setup_state(stu_code = 'my_fun(a = 10)', sol_code=sol, pec=pec)
    helper.passes(s.check_function('my_fun'))
    helper.passes(s.check_function('my_fun').check_args('a'))
    with pytest.raises(TF):
        s.check_function('my_fun').check_args('a').has_equal_value()

def test_bind_args():
    from pythonwhat.local import setup_state
    from inspect import signature
    from pythonwhat.check_function import bind_args
    pec = "def my_fun(a, b, *args, **kwargs): pass"
    s = setup_state(pec = pec, stu_code = "my_fun(1, 2, 3, 4, c = 5)")
    args = s._state.student_function_calls['my_fun'][0]['args']
    sig = signature(s._state.student_process.shell.user_ns['my_fun'])
    binded_args = bind_args(sig, args)
    assert binded_args['a']['node'].n == 1
    assert binded_args['b']['node'].n == 2
    assert binded_args['args'][0]['node'].n == 3
    assert binded_args['args'][1]['node'].n == 4
    assert binded_args['kwargs']['c']['node'].n == 5

@pytest.mark.parametrize('argspec', [
    ['args', 0], ['args', 1], ['kwargs', 'c']
])
def test_args_kwargs_check_function_passing(argspec):
    code = 'my_fun(1, 2, 3, 4, c = 5)'
    s = setup_state(pec = 'def my_fun(a, b, *args, **kwargs): pass',
                    stu_code = code, sol_code = code)
    x = s.check_function('my_fun')
    helper.passes(x.check_args(argspec).has_equal_value())

@pytest.mark.parametrize('argspec, msg', [
    (['args', 0], 'Did you specify the first argument passed as a variable length argument'),
    (['args', 1], 'Did you specify the second argument passed as a variable length argument'),
    (['kwargs', 'c'], 'Did you specify the argument `c`')
])
def test_args_kwargs_check_function_failing_not_specified(argspec, msg):
    s = setup_state(pec = 'def my_fun(a, b, *args, **kwargs): pass',
                    sol_code = 'my_fun(1, 2, 3, 4, c = 5)',
                    stu_code = 'my_fun(1, 2)')
    x = s.check_function('my_fun')
    with pytest.raises(TF, match=msg):
        x.check_args(argspec)

@pytest.mark.parametrize('argspec, msg', [
    (['args', 0], 'Did you correctly specify the first argument passed as a variable length argument'),
    (['args', 1], 'Did you correctly specify the second argument passed as a variable length argument'),
    (['kwargs', 'c'], 'Did you correctly specify the argument `c`')
])
def test_args_kwargs_check_function_failing_not_correct(argspec, msg):
    s = setup_state(pec = 'def my_fun(a, b, *args, **kwargs): pass',
                    sol_code = 'my_fun(1, 2, 3, 4, c = 5)',
                    stu_code = 'my_fun(1, 2, 4, 5, c = 6)')
    x = s.check_function('my_fun')
    with pytest.raises(TF, match=msg):
        x.check_args(argspec).has_equal_value()

def test_check_function_with_has_equal_value():
    code = 'import numpy as np\narr = np.array([1, 2, 3, 4, 5])\nnp.mean(arr)'
    s = setup_state(stu_code=code, sol_code=code)
    helper.passes(s.check_function('numpy.mean').has_equal_value())

def check_function_sig_false():
    code = "f(color = 'blue')"
    s = setup_state(pec="def f(*args, **kwargs): pass",
                    sol_code=code, stu_code=code)
    helper.passes(s.check_function('f', 0, signature=False).check_args('color').has_equal_ast())

def check_function_sig_false_override():
    s = setup_state(pec="def f(*args, **kwargs): pass",
                    sol_code="f(color = 'blue')",
                    stu_code="f(c = 'blue')")
    helper.passes(s.override("f(c = 'blue')").check_function('f', 0, signature=False)\
                .check_args('c').has_equal_ast())

def check_function_multiple_times():
    from pythonwhat.local import setup_state
    s = setup_state(sol_code = "print('test')",
                    stu_code = "print('test')")
    helper.passes(s.check_function('print'))
    helper.passes(s.check_function('print').check_args(0))
    helper.passes(s.check_function('print').check_args('value'))

@pytest.mark.parametrize('stu', [
    'round(1.23, 2)',
    'round(1.23, ndigits=2)',
    'round(number=1.23, ndigits=2)'
])
def test_named_vs_positional(stu):
    s = setup_state(sol_code = 'round(1.23, 2)', stu_code = stu)
    helper.passes(s.check_function('round').check_args(0).has_equal_value())
    helper.passes(s.check_function('round').check_args("number").has_equal_value())
    helper.passes(s.check_function('round').check_args(1).has_equal_value())
    helper.passes(s.check_function('round').check_args("ndigits").has_equal_value())

def test_method_1():
    code = "df.groupby('b').sum()"
    s = setup_state(sol_code = code,
                    stu_code = code,
                    pec = "import pandas as pd; df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'x', 'y']})")
    helper.passes(s.check_function('df.groupby').check_args(0).has_equal_value())
    helper.passes(s.check_function('df.groupby.sum', signature = False))
    from pythonwhat.signatures import sig_from_obj
    import pandas as pd
    helper.passes(s.check_function('df.groupby.sum', signature = sig_from_obj(pd.Series.sum)))

def test_method_2():
    code = "df[df.b == 'x'].a.sum()"
    s = setup_state(sol_code = code,
                    stu_code = code,
                    pec = "import pandas as pd; df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'x', 'y']})")
    helper.passes(s.check_function('df.a.sum', signature = False))
    from pythonwhat.signatures import sig_from_obj
    import pandas as pd
    helper.passes(s.check_function('df.a.sum', signature = sig_from_obj(pd.Series.sum)))

@pytest.mark.parametrize('code', [
    'print(round(1.23))',
    'x = print(round(1.23))',
    'x = [round(1.23)]',
    'x = {"a": round(1.23)}',
    'x = 0; x += round(1.23)',
    'x = 0; x > round(1.23)'
])
def test_function_parser(code):
    output = helper.run({
        'DC_CODE': code,
        'DC_SOLUTION': code,
        'DC_SCT': 'Ex().check_function("round").check_args(0).has_equal_value()'
    })
    assert output['correct']

@pytest.mark.parametrize('sct', [
    "Ex().check_function('round').check_args('ndigits').has_equal_value()",
    "Ex().check_correct(check_object('x').has_equal_value(), check_function('round').check_args('ndigits').has_equal_value())",
    "Ex().check_function('round', signature = False).check_args('ndigits').has_equal_value()",
    "Ex().check_correct(check_object('x').has_equal_value(), check_function('round', signature = False).check_args('ndigits').has_equal_value())"
])
@pytest.mark.parametrize('sol', [
    'x = 5',
    'x = round(5.23)'
])
def test_check_function_weirdness(sct, sol):
    data = {
        'DC_CODE': 'round(1.23, ndigits = 1)',
        'DC_SOLUTION': sol,
        'DC_SCT': sct
    }
    with pytest.raises(InstructorError):
        helper.run(data)