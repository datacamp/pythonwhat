import pytest
from pythonwhat.local import setup_state
import helper

def test_has_expr_override_pass():
    stu = 'x = [1, 2, 3]'
    sol = 'x = [1, 2, 5]'
    s = setup_state(stu_code=stu, sol_code=sol)
    helper.passes(s.check_object('x').has_equal_value(expr_code = 'x[2]', override=3))

def test_has_expr_override_pass_2():
    stu = 'x = [1, 2, 3]'
    sol = 'x = [1, 2, 5]'
    s = setup_state(stu_code=stu, sol_code=sol)
    helper.passes(s.check_object('x').has_equal_value(override=[1, 2, 3]))
