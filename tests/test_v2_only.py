import pytest
import os
from contextlib import contextmanager
import helper
import importlib

@contextmanager
def set_pw_env(new):
    key = 'PYTHONWHAT_V2_ONLY'
    old = os.environ.get(key)
    try:
        os.environ[key] = new
        yield
    finally:
        if old is None:
            del os.environ[key]
        else:
            os.environ[key] = old

@pytest.fixture
def data():
    return {
        'DC_CODE': 'x = round(4)',
        'DC_SOLUTION': 'x = round(5)'
    }

@pytest.mark.parametrize('sct, should_err', [
    ("test_object('x')", True),
    ("test_function('round')", True),
    ("Ex().test_object('x')", True),
    ("Ex().test_or(check_object('x').has_equal_value()", True),
    ("Ex().check_or(test_object('x'))", True),
    ("Ex().check_object('x').has_equal_value()", False),
    ("Ex() >> check_object('x').has_equal_value()", False),
    ("Ex().check_or(check_object('x').has_equal_value(), check_object('x').has_equal_value())", False),
    ("x = check_object('x').has_equal_value(); Ex() >> x", False)
])
def test_with_env_old_fail(data, sct, should_err):
    data['DC_SCT'] = sct
    with set_pw_env('1'):
        import pythonwhat.check_syntax
        importlib.reload(pythonwhat.check_syntax)
        if should_err:
            with pytest.raises(Exception):
                sct_payload = helper.run(data)
        else:
            sct_payload = helper.run(data)
            assert not sct_payload['correct']

@pytest.mark.parametrize('sct', [
    "test_object('x')",
    "Ex().test_object('x')",
    "test_function('round')",
    "Ex().check_object('x').has_equal_value()",
    "Ex() >> check_object('x').has_equal_value()",
    "x = check_object('x').has_equal_value(); Ex() >> x"
])
def test_without_env_all_works(data, sct):
    data['DC_SCT'] = sct
    with set_pw_env(''):
        import pythonwhat
        importlib.reload(pythonwhat.check_syntax)
        sct_payload = helper.run(data)
        assert not sct_payload['correct']

