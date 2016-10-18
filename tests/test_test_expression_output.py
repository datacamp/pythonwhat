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

if __name__ == "__main__":
    unittest.main()
