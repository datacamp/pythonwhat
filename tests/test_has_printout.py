import pytest
from pythonwhat.local import setup_state
from pythonwhat.Test import TestFail as TF
import helper

@pytest.mark.parametrize('stu', [
        "print(1, 2, 3)",
        "print('1 2 3')",
        "print('1', '2 3')",
        "print(1, '2 3')",
        "print('1 2', '3')",
        "print('1 2', 3)",
    ])
def test_basic_has_printout_passing(stu):
    sol = 'print(1, 2, 3)'
    s = setup_state(stu_code=stu, sol_code=sol)
    helper.passes(s.has_printout(0))

@pytest.mark.parametrize('stu', [
        "print(1, 2)",
        "print('1 2')",
        "print('1 3 2')",
        "print(1, 3, 2)",
        "print(1, 2, 4, 3)",
        "print('1 2 4 3')",
        "print('1 2', 4, 3)"
    ])
def test_basic_has_printout_failing(stu):
    sol = 'print(1, 2, 3)'
    s = setup_state(stu_code=stu, sol_code=sol)
    with pytest.raises(TF, match=r'Have you used `print\(1, 2, 3\)`'):
        s.has_printout(0)

def test_basic_has_printout_failing_custom():
    sol = 'print(1, 2, 3)'
    stu = 'print(1, 2)'
    s = setup_state(stu_code=stu, sol_code=sol)
    with pytest.raises(TF, match='wrong'):
        s.has_printout(0, not_printed_msg='wrong')

@pytest.mark.parametrize('stu', [
        "print(1, 2, 3)",
        "print('1 2 3')",
        "print('1', '2 3')",
        "print(1, '2 3')",
        "print('1 2', '3')",
        "print('1 2', 3)",
    ])
def test_has_printout_multiple(stu):
    sol = 'print("randomness")\nprint(1, 2, 3)'
    s = setup_state(stu_code=stu, sol_code=sol)
    helper.passes(s.has_printout(1))

def test_incorrect_use():
    s = setup_state(stu_code='', sol_code='')
    with pytest.raises(ValueError, match='Using has_printout'):
        s.has_printout(1)



