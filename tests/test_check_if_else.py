import pytest
import tests.helper as helper


@pytest.mark.parametrize(
    "sct",
    [
        """
def condition_test():
    test_expression_result({"offset": 7})
    test_expression_result({"offset": 8})
    test_expression_result({"offset": 9})
test_if_else(index=1,
             test = condition_test,
             body = lambda: test_student_typed(r'x\s*=\s*5'),
             orelse = lambda: test_function('round'))
    """,
        """
condition_test = [
    test_expression_result({"offset": 7}),
    test_expression_result({"offset": 8}),
    test_expression_result({"offset": 9})
]

test_if_else(index=1,
             test = condition_test,
             body = test_student_typed(r'x\s*=\s*5'),
             orelse = test_function('round'))
    """,
        """
Ex().check_if_else().multi(
    check_test().multi([ set_env(offset = i).has_equal_value() for i in range(7,10) ]),
    check_body().has_code(r'x\s*=\s*5'),
    check_orelse().check_function('round').check_args(0).has_equal_value()
)
    """,
    ],
)
@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("if offset > 10: x = 5\nelse: x = round(2.123)", False),
        ("if offset > 8: x = 7\nelse: x = round(2.123)", False),
        ("if offset > 8: x,y = 7,12\nelse: x = round(2.123)", False),
        ("if offset > 8: x = 5\nelse: x = 8", False),
        ("if offset > 8: x = 5\nelse: x = round(2.2121314)", False),
        ("if offset > 8: x = 5\nelse: x = round(2.123)", True),
    ],
)
def test_check_if_else_basic(sct, stu, passes):
    res = helper.run(
        {
            "DC_PEC": "offset = 8",
            "DC_SOLUTION": "if offset > 8: x = 5\nelse: x = round(2.123)",
            "DC_CODE": stu,
            "DC_SCT": sct,
        }
    )
    assert res["correct"] == passes


@pytest.mark.parametrize(
    "sct",
    [
        """
def test_test():
    test_expression_result({"offset": 7})
    test_expression_result({"offset": 8})
    test_expression_result({"offset": 9})

def body_test():
    test_student_typed('5')

def orelse_test():
    def test_test2():
        test_expression_result({"offset": 4})
        test_expression_result({"offset": 5})
        test_expression_result({"offset": 6})
    def body_test2():
        test_student_typed('7')
    def orelse_test2():
        test_function('round')
    test_if_else(index = 1,
                  test = test_test2,
                  body = body_test2,
                  orelse = orelse_test2)

test_if_else(index=1,
             test=test_test,
             body=body_test,
             orelse=orelse_test)
    """,
        """
test_if_else(index=1,
    test=[
        test_expression_result({"offset": 7}),
        test_expression_result({"offset": 8}),
        test_expression_result({"offset": 9})
    ],
    body=test_student_typed('5'),
    orelse=test_if_else(index = 1,
        test=[
            test_expression_result({"offset": 4}),
            test_expression_result({"offset": 5}),
            test_expression_result({"offset": 6})
        ],
        body = test_student_typed('7'),
        orelse = test_function('round')
    )
)
    """,
        """
Ex().check_if_else().multi(
    check_test().multi([ set_env(offset = i).has_equal_value() for i in range(7, 10) ]),
    check_body().has_code(r'x\s*=\s*5'),
    check_orelse().check_if_else().multi(
        check_test().multi([ set_env(offset = i).has_equal_value() for i in range(4, 7) ]),
        check_body().has_code('7'),
        check_orelse().check_function('round').check_args(0).has_equal_value()
    )
)
    """,
    ],
)
@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("if offset > 9: x = 5\nelif offset > 5: x = 7\nelse: x = round(9)", False),
        ("if offset > 8: x = 6\nelif offset > 5: x = 7\nelse: x = round(9)", False),
        ("if offset > 8: x = 5\nelif offset > 6: x = 7\nelse: x = round(9)", False),
        ("if offset > 8: x = 5\nelif offset > 5: x = 8\nelse: x = round(9)", False),
        ("if offset > 8: x = 5\nelif offset > 5: x = 7\nelse: x = round(10)", False),
        ("if offset > 8: x = 5\nelif offset > 5: x = 7\nelse: x = round(9)", True),
    ],
)
def test_check_if_else_embedded(sct, stu, passes):
    res = helper.run(
        {
            "DC_PEC": "offset = 8",
            "DC_SOLUTION": "if offset > 8: x = 5\nelif offset > 5: x = 7\nelse: x = round(9)",
            "DC_CODE": stu,
            "DC_SCT": sct,
        }
    )
    assert res["correct"] == passes


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("x = 5 if offset > 9 else 7 if offset > 5 else round(9)", False),
        ("x = 6 if offset > 8 else 7 if offset > 5 else round(9)", False),
        ("x = 5 if offset > 8 else 7 if offset > 6 else round(9)", False),
        ("x = 5 if offset > 8 else 8 if offset > 5 else round(9)", False),
        ("x = 5 if offset > 8 else 7 if offset > 5 else round(10)", False),
        ("x = 5 if offset > 8 else 7 if offset > 5 else round(9)", True),
    ],
)
def test_if_exp(stu, passes):
    res = helper.run(
        {
            "DC_PEC": "offset = 8",
            "DC_SOLUTION": "x = 5 if offset > 8 else 7 if offset > 5 else round(9)",
            "DC_CODE": stu,
            "DC_SCT": """
Ex().check_if_exp().multi(
    check_test().multi([ set_env(offset = i).has_equal_value() for i in range(7, 10) ]),
    check_body().has_code('5'),
    check_orelse().check_if_exp().multi(
        check_test().multi([ set_env(offset = i).has_equal_value() for i in range(4, 7) ]),
        check_body().has_code('7'),
        check_orelse().check_function('round').check_args(0).has_equal_value()
    )
)
""",
        }
    )
    assert res["correct"] == passes


from pythonwhat.parsing import IfExpParser
import ast


@pytest.mark.parametrize(
    "stu",
    [
        "x = 3 if True else False",
        "x += 3 if True else False",
        "y = x or 3 if True else False",
        "3 if True else False + 4 if True else False",
        "not 3 if True else False",
    ],
)
def test_if_exp_findable(stu):
    p = IfExpParser()
    p.visit(ast.parse(stu))
    assert "test" in p.out[0]
    assert "body" in p.out[0]
    assert "orelse" in p.out[0]
