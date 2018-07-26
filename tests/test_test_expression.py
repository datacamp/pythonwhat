import unittest
import helper

class TestExpressionOutputBasic(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = {'a': 1, 'b':2, 'c':3}",
            "DC_SCT": "test_expression_output(expr_code = \"print(x['a'])\")"
        }

    def test_fun_step1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_fun_step2(self):
        self.data["DC_CODE"] = "x = {'a': 2}"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_fun_step3(self):
        self.data["DC_CODE"] = "x = {'a': 1}"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestExpressionOutputInsideFor(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "for i in range(10):\n    print(i)",
            "DC_SCT": "test_for_loop(body = lambda: test_expression_output())"
        }

    def test_fun_step1(self):
        self.data["DC_CODE"] = "for i in range(10):\n    print(i + 1)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_fun_step2(self):
        self.data["DC_CODE"] = "for i in range(10):\n    print(i)"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fun_step1_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_fun_step1()

    def test_fun_step2_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_fun_step2()

class TestExpressionOutputInsideFor2(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "for i in range(10):\n    print(i)",
            "DC_SCT": "test_for_loop(body = lambda: test_expression_output(context_vals = [1]))"
        }

    def test_fun_step1(self):
        self.data["DC_CODE"] = "for i in range(10):\n    print(i + 1)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_fun_step2(self):
        self.data["DC_CODE"] = "for i in range(10):\n    print(i)"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fun_step1_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_fun_step1()

    def test_fun_step2_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_fun_step2()

class TestExpressionOutputBasic(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "a = 2",
            "DC_SCT": "test_expression_result(expr_code = 'a', error_msg = 'cough')"
        }

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'cough')

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_no_copy_bad_sct_passes(self):
        self.data["DC_SOLUTION"] = "a = [2]"
        self.data["DC_CODE"] = "a = [1]"
        self.data["DC_SCT"] = "Ex().has_equal_value(expr_code = 'a[0] = 3', name = 'a', copy = False).has_equal_value(expr_code = 'a', name = 'a')"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_copy_sct_fails(self):
        self.data["DC_SOLUTION"] = "a = [2]"
        self.data["DC_CODE"] = "a = [1]"
        self.data["DC_SCT"] = "Ex().has_equal_value(expr_code = 'a[0] = 3', name = 'a', copy = True).has_equal_value(name = 'a')"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_test_expression_result_copy_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        self.data["DC_SCT"] = "test_expression_result(expr_code = 'a', error_msg = 'cough', copy = False)"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_test_custom_equality_func(self):
        self.data["DC_SOLUTION"] = "a = [1.01]"
        self.data["DC_CODE"] = "a = [1.011]"
        self.data["DC_SCT"] = "import numpy as np; Ex().check_object('a').has_equal_value(func = lambda x, y: np.allclose(x, y, atol = .001))"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_test_custom_equality_func_fail(self):
        self.data["DC_SOLUTION"] = "a = [1.01]"
        self.data["DC_CODE"] = "a = [1.011]"
        self.data["DC_SCT"] = "import numpy as np; Ex().check_object('a').has_equal_value(func = lambda x, y: np.allclose(x, y, atol = .0001))"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])


if __name__ == "__main__":
    unittest.main()
