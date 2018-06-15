import pytest
import helper
import unittest
from pythonwhat.local import setup_state
from pythonwhat.Test import TestFail as TF
from pythonwhat.check_syntax import Chain
from inspect import signature
from pythonwhat.check_function import bind_args

def passes(st):
    assert isinstance(st, Chain)

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
    passes(s.check_function('my_fun'))

    passes(s.check_function('my_fun').check_args(arg))
    passes(s.check_function('my_fun').check_args(arg).has_equal_value())

def test_basic_check_function_failing():
    pec = 'def my_fun(a=1): pass'
    sol = 'my_fun(1)'
    s = setup_state(stu_code = '', sol_code=sol, pec=pec)
    with pytest.raises(TF):
        s.check_function('my_fun')

    s = setup_state(stu_code = 'my_fun()', sol_code=sol, pec=pec)
    passes(s.check_function('my_fun'))
    with pytest.raises(TF):
        s.check_function('my_fun').check_args('a')

    s = setup_state(stu_code = 'my_fun(a = 10)', sol_code=sol, pec=pec)
    passes(s.check_function('my_fun'))
    passes(s.check_function('my_fun').check_args('a'))
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

def test_args_kwargs_check_function_passing():
    code = 'my_fun(1, 2, 3, 4, c = 5)'
    s = setup_state(pec = 'def my_fun(a, b, *args, **kwargs): pass',
                    stu_code = code, sol_code = code)
    x = s.check_function('my_fun')
    passes(x.check_args(['args', 0]).has_equal_value())
    passes(x.check_args(['args', 1]).has_equal_value())
    passes(x.check_args(['kwargs', 'c']).has_equal_value())

def test_args_kwargs_check_function_failing_not_specified():
    s = setup_state(pec = 'def my_fun(a, b, *args, **kwargs): pass',
                    sol_code = 'my_fun(1, 2, 3, 4, c = 5)',
                    stu_code = 'my_fun(1, 2)')
    x = s.check_function('my_fun')
    msg = "Are you sure it is defined"
    with pytest.raises(TF, match=msg):
        x.check_args(['args', 0])
    with pytest.raises(TF, match=msg):
        x.check_args(['args', 1])
    with pytest.raises(TF, match=msg):
        x.check_args(['kwargs', 'c'])

def test_args_kwargs_check_function_failing_not_correct():
    s = setup_state(pec = 'def my_fun(a, b, *args, **kwargs): pass',
                    sol_code = 'my_fun(1, 2, 3, 4, c = 5)',
                    stu_code = 'my_fun(1, 2, 4, 5, c = 6)')
    x = s.check_function('my_fun')
    with pytest.raises(TF):
        x.check_args(['args', 0]).has_equal_value()
    with pytest.raises(TF):
        x.check_args(['args', 1]).has_equal_value()
    with pytest.raises(TF):
        x.check_args(['kwargs', 'c']).has_equal_value()

def test_check_function_with_has_equal_value():
    code = 'import numpy as np\narr = np.array([1, 2, 3, 4, 5])\nnp.mean(arr)'
    s = setup_state(stu_code=code, sol_code=code)
    passes(s.check_function('numpy.mean').has_equal_value())

def check_function_sig_false():
    code = "f(color = 'blue')"
    s = setup_state(pec="def f(*args, **kwargs): pass",
                    sol_code=code, stu_code=code)
    passes(s.check_function('f', 0, signature=False).check_args('color').has_equal_ast())

def check_function_sig_false_override():
    s = setup_state(pec="def f(*args, **kwargs): pass",
                    sol_code="f(color = 'blue')",
                    stu_code="f(c = 'blue')")
    passes(s.override("f(c = 'blue')").check_function('f', 0, signature=False)\
                .check_args('c').has_equal_ast())

def check_function_multiple_times():
    from pythonwhat.local import setup_state
    s = setup_state(sol_code = "print('test')",
                    stu_code = "print('test')")
    passes(s.check_function('print'))
    passes(s.check_function('print').check_args(0))
    passes(s.check_function('print').check_args('value'))

@pytest.mark.parametrize('stu', [
        'round(1.23, 2)',
        'round(1.23, ndigits=2)',
        'round(number=1.23, ndigits=2)'
])
def test_named_vs_positional(stu):
    s = setup_state(sol_code = 'round(1.23, 2)', stu_code = stu)
    passes(s.check_function('round').check_args(0).has_equal_value())
    passes(s.check_function('round').check_args("number").has_equal_value())
    passes(s.check_function('round').check_args(1).has_equal_value())
    passes(s.check_function('round').check_args("ndigits").has_equal_value())
