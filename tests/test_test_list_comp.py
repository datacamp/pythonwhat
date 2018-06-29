import unittest
import helper
import pytest

class TestListCompStepByStep(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "x = {'a': 2, 'b':3, 'c':4, 'd':'test'}",
            "DC_SOLUTION": "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int)]",
            "DC_SCT": '''
test_list_comp(index=1,
               not_called_msg=None,
               comp_iter=lambda: test_expression_result(),
               iter_vars_names=True,
               incorrect_iter_vars_msg=None,
               body=lambda: test_expression_result(context_vals = ['a', 2]),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False]),
                    lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False])],
               insufficient_ifs_msg=None,
               expand_message=True)
            '''
        }

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the first list comprehension but hasn't found it.")

    def test_fail_2(self):
        self.data["DC_CODE"] = "[key for key in x.keys()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check the first list comprehension. Did you correctly specify the iterable part?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 17, 24)

    def test_fail_3(self):
        self.data["DC_CODE"] = "[a + str(b) for a,b in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you used the correct iterator variables in the first list comprehension? Be sure to use the correct names.")
        helper.test_lines(self, sct_payload, 1, 1, 17, 19)

    def test_fail_4(self):
        self.data["DC_CODE"] = "[key + '_' + str(val) for key,val in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertIn("Check the first list comprehension. Did you correctly specify the body?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 2, 21)

    def test_fail_5(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Have you used 2 ifs inside the first list comprehension?", sct_payload['message'])
        # helper.test_lines(self, sct_payload, 1, 1, 2, 41) # small hiccup!

    def test_fail_6(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test')]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check the first list comprehension. Did you correctly specify the first if? Did you call <code>isinstance()</code>?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 45, 64)

    def test_fail_7(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test')]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check the first list comprehension. Did you correctly specify the second if? Did you call <code>isinstance()</code>?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 69, 88)

    def test_fail_8(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str)]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check the first list comprehension. Did you correctly specify the second if?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 80, 82)

    def test_pass(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_no_lam(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]"
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_mix_lam(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]"
        self.data["DC_SCT"] = '''
test_list_comp(index=1,
               not_called_msg=None,
               comp_iter=lambda: test_expression_result(),
               iter_vars_names=True,
               incorrect_iter_vars_msg=None,
               body=test_expression_result(context_vals = ['a', 2]),
               ifs=[test_function_v2('isinstance', params = ['obj'], do_eval = [False]),
                    test_function_v2('isinstance', params = ['obj'], do_eval = [False])],
               insufficient_ifs_msg=None,
               expand_message=True)
            '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_exchain(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]"
        self.data["DC_SCT"] = "Ex().\\" + helper.remove_lambdas(self.data["DC_SCT"])
        
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestListCompStepByStepCustom(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "x = {'a': 2, 'b':3, 'c':4, 'd':'test'}",
            "DC_SOLUTION": "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int)]",
            "DC_SCT": '''
test_list_comp(index=1,
               not_called_msg='notcalled',
               comp_iter=lambda: test_expression_result(incorrect_msg = 'iterincorrect'),
               iter_vars_names=True,
               incorrect_iter_vars_msg='incorrectitervars',
               body=lambda: test_expression_result(context_vals = ['a', 2], incorrect_msg = 'bodyincorrect'),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False], not_called_msg = 'notcalled1', incorrect_msg = 'incorrect2'),
                    lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False], not_called_msg = 'notcalled2', incorrect_msg = 'incorrect2')],
               insufficient_ifs_msg='insufficientifs')
            '''
        }

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "notcalled")

    def test_fail_2(self):
        self.data["DC_CODE"] = "[key for key in x.keys()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("iterincorrect", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 17, 24)

    def test_fail_3(self):
        self.data["DC_CODE"] = "[a + str(b) for a,b in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "incorrectitervars")
        helper.test_lines(self, sct_payload, 1, 1, 17, 19)

    def test_fail_4(self):
        self.data["DC_CODE"] = "[key + '_' + str(val) for key,val in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertEqual("bodyincorrect", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 2, 21)

    def test_fail_5(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("insufficientifs", sct_payload['message'])
        # helper.test_lines(self, sct_payload, 1, 1, 2, 41) # small hiccup!

    def test_fail_6(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test')]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("notcalled1", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 45, 64)

    def test_fail_7(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test')]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("notcalled2", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 69, 88)

    def test_fail_8(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str)]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("incorrect2", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 80, 82)

    def test_pass(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


    def test_pass_no_lam(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]"
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestListCompNested(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "[[col for col in range(5)] for row in range(5)]",
            "DC_SCT": "test_list_comp(1, body = lambda: test_list_comp(1, body = lambda: test_expression_result(context_vals = [4])))"
        }

    def test_fail(self):
        self.data["DC_CODE"] = "[[col + 1 for col in range(5)] for row in range(5)]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_pass(self):
        self.data["DC_CODE"] = "[[col for col in range(5)] for row in range(5)]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail_no_lam(self):
        self.data["DC_CODE"] = "[[col + 1 for col in range(5)] for row in range(5)]"
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_pass_no_lam(self):
        self.data["DC_CODE"] = "[[col for col in range(5)] for row in range(5)]"
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_mix_lam1(self):
        self.data["DC_CODE"] = "[[col for col in range(5)] for row in range(5)]"
        self.data["DC_SCT"] = "test_list_comp(1, body = test_list_comp(1, body = lambda: test_expression_result(context_vals = [4])))"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_mix_lam2(self):
        self.data["DC_CODE"] = "[[col for col in range(5)] for row in range(5)]"
        self.data["DC_SCT"] = "test_list_comp(1, body = lambda: test_list_comp(1, body = test_expression_result(context_vals = [4])))"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestListIterVars(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "x = {'a':1, 'b':2}",
            "DC_SOLUTION": "[key for key, value in x.items()]",
            "DC_SCT": "test_list_comp(1, iter_vars_names=False)"
        }

    def test_fail(self):
        self.data["DC_CODE"] = "[a for a in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you used 2 iterator variables in the first list comprehension?")

    def test_pass(self):
        self.data["DC_CODE"] = "[a for a,b in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail_spec2(self):
        self.data["DC_SCT"] = "Ex().check_list_comp(0).has_context()"
        self.data["DC_CODE"] = "[a for a in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_pass_spec2(self):
        self.data["DC_SCT"] = "Ex().check_list_comp(0).has_context()"
        self.test_pass()

    def test_fail_spec2_exact_names(self):
        self.data["DC_CODE"] = "[a for a,b in x.items()]"
        self.data["DC_SCT"] = "Ex().check_list_comp(0).has_context(exact_names=True)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])


class TestListDestructuring(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "x = {'a':1, 'b':2}",
            "DC_SOLUTION": "[key for key, value in x.items()]",
            "DC_SCT": "test_list_comp(1, body=test_expression_result(context_vals=[(1,2)]), iter_vars_names=False)"
        }

    @unittest.expectedFailure
    def test_pass_destructuring1(self):
        # TODO: fails because context_vals set by simple iteration and for reason below
        self.data["DC_CODE"] = "[a[0] for *a in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_destructuring2(self):
        self.data["DC_CODE"] = "[a for *a, b in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_destructuring3(self):
        self.data["DC_CODE"] = "[b for b, *a in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    @unittest.expectedFailure
    def test_pass_destructuring4(self):
        # TODO: fails because it tests for exact same number of iter vars
        self.data["DC_CODE"] = "[k for k, v, *a in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail_destructuring(self):
        self.data["DC_CODE"] = "[a for k, v, *a in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

if __name__ == "__main__":
     unittest.main()
