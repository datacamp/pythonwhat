import pytest
import tests.helper as helper
from pythonwhat.test_exercise import setup_state
from pythonwhat.sct_syntax import v2_check_functions

globals().update(v2_check_functions)


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("def A(x): pass", False),
        ("class A(): pass", False),
        ("class A(int): pass", False),
        ("class A(str):\n  def __not_init__(self): pass", False),
        ("class A(str):\n  def __init__(self): print(1)", False),
        ("class A(str):\n  def __init__(self): pass", True),
    ],
)
def test_check_class_def_pass(stu, passes):
    sol = "class A(str):\n  def __init__(self): pass"
    s = setup_state(stu, sol)
    with helper.verify_sct(passes):
        s.check_class_def("A").multi(
            check_bases(0).has_equal_ast(),
            check_body().check_function_def("__init__").check_body().has_equal_ast(),
        )


def test_check_wiki_example():
    code = """
class MyInt(int):
    def __init__(self, i):
        super().__init__(i + 1)
"""
    s = setup_state(code, code)
    s.check_class_def("MyInt").multi(
        check_bases(0).has_equal_ast(),
        check_body()
        .check_function_def("__init__")
        .multi(
            check_args("self"),
            check_args("i"),
            check_body()
            .set_context(i=2)
            .multi(
                check_function("super", signature=False),
                check_function("super.__init__").check_args(0).has_equal_value(),
            ),
        ),
    )
