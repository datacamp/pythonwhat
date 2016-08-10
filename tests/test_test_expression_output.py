import unittest
import helper

# class TestExpressionResultBasic(unittest.TestCase):

#     def test_fun_pass(self):
#         self.data = {
#             "DC_PEC": "",
#             "DC_SOLUTION": "x = {'a': 1, 'b':2, 'c':3}",
#             "DC_CODE": "my_fun(1)",
#             "DC_SCT": "test_function_v2('my_fun', params = ['a'])"
#         }
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_fun_fail(self):
#         self.data = {
#             "DC_PEC": "def my_fun(a):\n    pass",
#             "DC_SOLUTION": "my_fun(2)",
#             "DC_CODE": "my_fun(1)",
#             "DC_SCT": "test_function_v2('my_fun', params = ['a'])"
#         }
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertIn('The argument you specified for <code>a</code> seems to be incorrect.', sct_payload['message'])
#         helper.test_lines(self, sct_payload, 1, 1, 8, 8)


if __name__ == "__main__":
    unittest.main()
