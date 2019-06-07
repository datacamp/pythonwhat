from tempfile import NamedTemporaryFile

import pytest
import tests.helper as helper
from protowhat.sct_syntax import F

from pythonwhat.test_exercise import setup_state
from protowhat.checks import check_files as cf


@pytest.fixture
def temp_py_file():
    with NamedTemporaryFile() as tmp:
        tmp.file.write(
            b"""
if True:
    a = 1"""
        )
        tmp.file.flush()
        yield tmp


@pytest.fixture
def temp_txt_file():
    with NamedTemporaryFile() as tmp:
        tmp.file.write(b"this is a text file")
        tmp.file.flush()
        yield tmp


@pytest.fixture(params=["temp_py_file", "temp_txt_file"])
def temp_file(request):
    return request.getfuncargvalue(request.param)


def test_python_file_existence(temp_py_file):
    expected_content = cf.get_file_content(temp_py_file.name)
    chain = setup_state("", "", pec="")

    # test with just student content
    child = cf.check_file(chain._state, temp_py_file.name)
    assert expected_content in child.student_code
    assert child.student_ast is not None
    assert child.solution_code is None
    assert child.solution_ast is None

    # test with solution content
    child = cf.check_file(
        chain._state, temp_py_file.name, solution_code=expected_content
    )
    assert expected_content in child.student_code
    assert child.student_ast is not None
    assert expected_content in child.solution_code
    assert child.solution_ast is not None


def test_file_existence_syntax(temp_py_file):
    """test integration of protowhat checks in pythonwhat"""
    expected_content = cf.get_file_content(temp_py_file.name)
    chain = setup_state("", "", pec="")

    file_chain = chain.check_file(temp_py_file.name)
    assert expected_content in file_chain._state.student_code

    with helper.verify_sct(True):
        file_chain = chain >> F(attr_scts={"check_file": cf.check_file}).check_file(
            temp_py_file.name
        )
        assert expected_content in file_chain._state.student_code


def test_file_parsing(temp_py_file):
    expected_content = cf.get_file_content(temp_py_file.name)
    chain = setup_state("", "", pec="")

    file_chain = chain.check_file(temp_py_file.name, solution_code=expected_content)
    file_chain.check_if_else().check_test().has_equal_value()
    file_chain.check_if_else().check_test().has_equal_value(expr_code="False")


def test_file_content(temp_file):
    expected_content = cf.get_file_content(temp_file.name)
    chain = setup_state("", "", pec="")

    chain.check_file(temp_file.name, parse=False).has_code(expected_content)
    chain.check_file(
        temp_file.name, parse=False, solution_code=expected_content
    ).has_code(expected_content)
