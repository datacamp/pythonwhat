import pytest
import tests.helper as helper
from pythonwhat.test_exercise import setup_state
from pythonwhat.sct_syntax import v2_check_functions

globals().update(v2_check_functions)


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("", False),
        ("[key for key in x.keys()]", False),
        ("[a + str(b) for a,b in x.items()]", False),
        ("[key + '_' + str(val) for key,val in x.items()]", False),
        ("[key + str(val) for key,val in x.items()]", False),
        (
            "[key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test')]",
            False,
        ),
        (
            "[key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test')]",
            False,
        ),
        (
            "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str)]",
            False,
        ),
        (
            "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]",
            True,
        ),
    ],
)
def test_check_list_comp_basic(stu, passes):
    pec = "x = {'a': 2, 'b':3, 'c':4, 'd':'test'}"
    sol = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int)]"
    s = setup_state(stu, sol, pec)
    with helper.verify_sct(passes):
        s.check_list_comp().multi(
            check_iter().has_equal_value(),
            check_ifs(0).check_function("isinstance").check_args("obj").has_equal_ast(),
            check_ifs(1).check_function("isinstance").check_args("obj").has_equal_ast(),
            check_body()
            .has_context(exact_names=True)
            .set_context("a", 2)
            .has_equal_value(),
        )


@pytest.mark.parametrize(
    "stu, passes, patt, lines",
    [
        (
            "",
            False,
            "The system wants to check the first list comprehension but hasn't found it.",
            [],
        ),
        (
            "[key for key in x.keys()]",
            False,
            "Check the first list comprehension. Did you correctly specify the iterable part?",
            [1, 1, 17, 24],
        ),
        (
            "[a + str(b) for a,b in x.items()]",
            False,
            "Check the first list comprehension. Have you used the correct iterator variables?",
            [1, 1, 17, 19],
        ),
        (
            "[key + '_' + str(val) for key,val in x.items()]",
            False,
            "Did you correctly specify the body?",
            [1, 1, 2, 21],
        ),
        (
            "[key + str(val) for key,val in x.items()]",
            False,
            "Check the first list comprehension. Have you used 2 ifs?",
            [],
        ),
        (
            "[key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test')]",
            False,
            "Did you correctly specify the first if? Did you call <code>isinstance()</code>?",
            [1, 1, 45, 64],
        ),
        (
            "[key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test')]",
            False,
            "Did you correctly specify the second if? Did you call <code>isinstance()</code>?",
            [1, 1, 69, 88],
        ),
        (
            "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str)]",
            False,
            "Did you correctly specify the argument <code>obj</code>? Expected <code>val</code>, but got <code>key</code>.",
            [1, 1, 80, 82],
        ),
        (
            "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]",
            True,
            "Great",
            [],
        ),
    ],
)
def test_test_list_comp_messaging(stu, passes, patt, lines):
    pec = "x = {'a': 2, 'b':3, 'c':4, 'd':'test'}"
    sol = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int)]"
    sct = """
test_list_comp(index=1,
               not_called_msg=None,
               comp_iter=lambda: test_expression_result(),
               iter_vars_names=True,
               incorrect_iter_vars_msg=None,
               body=lambda: test_expression_result(context_vals = ['a', 2]),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False]),
                    lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False])],
               insufficient_ifs_msg=None)
    """
    res = helper.run({"DC_PEC": pec, "DC_CODE": stu, "DC_SOLUTION": sol, "DC_SCT": sct})
    assert res["correct"] == passes
    assert patt in res["message"]
    if lines:
        helper.with_line_info(res, *lines)


@pytest.mark.parametrize(
    "stu, passes, patt, lines",
    [
        ("", False, "notcalled", []),
        ("[key for key in x.keys()]", False, "iterincorrect", [1, 1, 17, 24]),
        (
            "[a + str(b) for a,b in x.items()]",
            False,
            "incorrectitervars",
            [1, 1, 17, 19],
        ),
        (
            "[key + '_' + str(val) for key,val in x.items()]",
            False,
            "bodyincorrect",
            [1, 1, 2, 21],
        ),
        (
            "[key + str(val) for key,val in x.items()]",
            False,
            "insufficientifs",
            [],
        ),  # [1, 1, 2, 41] doesn't work...
        (
            "[key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test')]",
            False,
            "notcalled1",
            [1, 1, 45, 64],
        ),
        (
            "[key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test')]",
            False,
            "notcalled2",
            [1, 1, 69, 88],
        ),
        (
            "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str)]",
            False,
            "incorrect2",
            [1, 1, 80, 82],
        ),
        (
            "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]",
            True,
            "Great",
            [],
        ),
    ],
)
def test_test_list_comp_custom_messaging(stu, passes, patt, lines):
    pec = "x = {'a': 2, 'b':3, 'c':4, 'd':'test'}"
    sol = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int)]"
    sct = """
test_list_comp(index=1,
               not_called_msg='notcalled',
               comp_iter=lambda: test_expression_result(incorrect_msg = 'iterincorrect'),
               iter_vars_names=True,
               incorrect_iter_vars_msg='incorrectitervars',
               body=lambda: test_expression_result(context_vals = ['a', 2], incorrect_msg = 'bodyincorrect'),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False], not_called_msg = 'notcalled1', incorrect_msg = 'incorrect2'),
                    lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False], not_called_msg = 'notcalled2', incorrect_msg = 'incorrect2')],
               insufficient_ifs_msg='insufficientifs')
    """
    res = helper.run({"DC_PEC": pec, "DC_CODE": stu, "DC_SOLUTION": sol, "DC_SCT": sct})
    assert res["correct"] == passes
    assert patt in res["message"]
    if lines:
        helper.with_line_info(res, *lines)


@pytest.mark.parametrize(
    "stu, passes",
    [
        ("[[col + 1 for col in range(5)] for row in range(5)]", False),
        ("[[col for col in range(5)] for row in range(5)]", True),
    ],
)
def test_list_comp_nested(stu, passes):
    res = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "[[col for col in range(5)] for row in range(5)]",
            "DC_SCT": "test_list_comp(1, body = lambda: test_list_comp(1, body = lambda: test_expression_result(context_vals = [4])))",
        }
    )
    assert res["correct"] == passes


@pytest.mark.parametrize(
    "sct",
    [
        "test_list_comp(1, iter_vars_names=False)",
        "Ex().check_list_comp(0).has_context()",
    ],
)
@pytest.mark.parametrize(
    "stu, passes",
    [("[a for a in x.items()]", False), ("[a for a,b in x.items()]", True)],
)
def test_list_iter_vars(sct, stu, passes):
    res = helper.run(
        {
            "DC_PEC": "x = {'a':1, 'b':2}",
            "DC_SOLUTION": "[key for key, value in x.items()]",
            "DC_CODE": stu,
            "DC_SCT": sct,
        }
    )
    res["correct"] == passes


# TODO
# class TestListDestructuring(unittest.TestCase):
#     def setUp(self):
#         self.data = {
#             "DC_PEC": "x = {'a':1, 'b':2}",
#             "DC_SOLUTION": "[key for key, value in x.items()]",
#             "DC_SCT": "test_list_comp(1, body=test_expression_result(context_vals=[(1,2)]), iter_vars_names=False)"
#         }

#     @unittest.expectedFailure
#     def test_pass_destructuring1(self):
#         # TODO: fails because context_vals set by simple iteration and for reason below
#         self.data["DC_CODE"] = "[a[0] for *a in x.items()]"
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_pass_destructuring2(self):
#         self.data["DC_CODE"] = "[a for *a, b in x.items()]"
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_pass_destructuring3(self):
#         self.data["DC_CODE"] = "[b for b, *a in x.items()]"
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     @unittest.expectedFailure
#     def test_pass_destructuring4(self):
#         # TODO: fails because it tests for exact same number of iter vars
#         self.data["DC_CODE"] = "[k for k, v, *a in x.items()]"
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_fail_destructuring(self):
#         self.data["DC_CODE"] = "[a for k, v, *a in x.items()]"
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
