import pytest
from tempfile import NamedTemporaryFile, TemporaryDirectory
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import check_node
import ast

from pythonwhat import check_files as cf

def assert_equal_ast(a, b):
    assert ast.dump(a) == ast.dump(b)

@pytest.fixture(scope="function")
def state():
    Reporter.active_reporter = Reporter()

    s = State(
        student_code = "",
        solution_code = "",
        full_student_code = "",
        full_solution_code = "",
        # args below should be ignored
        pre_exercise_code = "NA", 
        student_process = None, solution_process = None,
        raw_student_output = ""
        )
    State.root_state = s
    yield s
    Reporter.active_reporter = Reporter()

@pytest.fixture(scope="function")
def tf():
    with NamedTemporaryFile() as tmp:
        tmp.file.write(b'1 if True else False')
        tmp.file.flush()
        yield tmp

def test_initial_state():
    State(student_code = {'script.py': '1'}, solution_code = {'script.py': '1'}, pre_exercise_code = "",
          full_student_code = "", full_solution_code = "")

def test_check_file_use_fs(state, tf):
    state.solution_code = { tf.name: '3 if True else False' }
    child = cf.check_file(tf.name, use_fs = True, state = state)
    assert child.student_code == '1 if True else False'
    assert_equal_ast(child.student_tree, ast.parse(child.student_code))
    assert child.solution_code == '3 if True else False'
    assert_equal_ast(child.solution_tree, ast.parse(child.solution_code))
    assert check_node('if_exps', 0, 'first inline if', state = child)

def test_check_file_use_fs_no_parse(state, tf):
    state.solution_code = { tf.name: '3 if True else False' }
    child = cf.check_file(tf.name, parse = False, use_fs = True, state = state)
    assert child.student_code == '1 if True else False'
    assert child.student_tree is None
    assert child.solution_tree is None

@pytest.mark.xfail #'TODO: implement requires_ast decorator'
def test_check_file_use_fs_no_parse_check_node_fail(state, tf):
    state.solution_code = { tf.name: '3 if True else False' }
    child = cf.check_file(tf.name, parse = False, use_fs = True, state = state)
    with pytest.raises(TypeError):
        assert check_node('if_exps', 0, 'first inline if', state = child)

#def test_check_no_sol(state, tf):
#    child = cf.check_file(state, tf.name, use_fs = True, use_solution = False)
#    assert child.solution_code == None

def test_check_dir(state):
    with TemporaryDirectory() as td:
        child = cf.test_dir(td, state = state)


@pytest.fixture(scope="function")
def code_state():
    Reporter.active_reporter = Reporter()

    s = State(
        student_code = {'script1.py': '1 + 1', 'script2.py': '2 + 2'},
        solution_code = {'script1.py': '3 + 3', 'script2.py': '4 + 4'},
        full_student_code = {},
        full_solution_code = {},
        # args below should be ignored
        pre_exercise_code = "NA", 
        raw_student_output = "",
        student_process = None, solution_process = None
        )
    State.root_state = s

    yield s

    Reporter.active_reporter = Reporter()

def test_check_file(code_state):
    child = cf.check_file('script1.py', state = code_state)
    assert child.student_code == "1 + 1"
    assert_equal_ast(child.student_tree, ast.parse(child.student_code))
    assert_equal_ast(child.solution_tree, ast.parse(child.solution_code))

def test_check_file_no_parse(code_state):
    child = cf.check_file('script1.py', parse = False, state = code_state)
    assert child.student_code == "1 + 1"
    assert child.student_tree is None
    assert child.solution_tree is None

