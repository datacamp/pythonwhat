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
    "sct",
    [
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
    assert res["correct"] == passes


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
