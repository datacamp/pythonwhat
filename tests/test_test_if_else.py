import unittest
import helper

class TestIfElse(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
# Initialize offset
offset = 8

# Code the while loop
if offset > 8:
    x = 5
else:
    x = round(2.123)
            ''',
            "DC_SCT": '''
def condition_test():
    test_expression_result({"offset": 7})
    test_expression_result({"offset": 8})
    test_expression_result({"offset": 9})


test_if_else(index=1,
             test = condition_test,
             body = lambda: test_student_typed('x\s*=\s*5', not_typed_msg = "you did something wrong"),
             orelse = lambda: test_function('round'))
success_msg("Nice")
            '''
        }

    def test_Pass(self):
        self.data["DC_CODE"] = '''
# Initialize offset
offset = 8

# Code the while loop
if offset > 8:
    x = 5
else:
    x = round(2.123)
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Nice")

    def test_Fail0(self):
        self.data["DC_CODE"] = '''
# Initialize offset
offset = 8
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the first if statement, but it hasn't found it. Have another look at your code.")

    def test_Fail1(self):
        self.data["DC_CODE"] = '''
# Initialize offset
offset = 8

# Code the while loop
if offset > 10:
    x = 5
else:
    x = round(2.123)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Unexpected expression", sct_payload['message'])
        helper.test_lines(self, sct_payload, 6, 6, 4, 14)

    def test_Fail2(self):
        self.data["DC_CODE"] = '''
# Initialize offset
offset = 8

# Code the while loop
if offset > 8:
    x = 7
else:
    x = round(2.123)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the body of the first <code>if</code> statement. you did something wrong", sct_payload['message'])
        helper.test_lines(self, sct_payload, 7, 7, 5, 9)

    def test_Fail2a(self):
        self.data["DC_CODE"] = '''
# Initialize offset
offset = 8

# Code the while loop
if offset > 8:
    x = 7
    y = 12
else:
    x = round(2.123)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the body of the first <code>if</code> statement. you did something wrong", sct_payload['message'])
        helper.test_lines(self, sct_payload, 7, 8, 5, 10)

    def test_Fail3(self):
        self.data["DC_CODE"] = '''
# Initialize offset
offset = 8

# Code the while loop
if offset > 8:
    x = 5
else:
    x = 8
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Have you called <code>round()</code>", sct_payload["message"])
        helper.test_lines(self, sct_payload, 9, 9, 5, 9)

    def test_Fail3b(self):
        self.data["DC_CODE"] = '''
# Initialize offset
offset = 8

# Code the while loop
if offset > 8:
    x = 5
else:
    x = round(2.2121314)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        # should give line numbers of more detailed test_function test.
        helper.test_lines(self, sct_payload, 9, 9, 15, 23)


class TestIfElseEmbedded(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
offset = 8
if offset > 8:
    x = 5
elif offset > 5:
    x = 7
else:
    x = round(9)
            ''',
            "DC_SCT": '''
def test_test():
    test_expression_result({"offset": 7})
    test_expression_result({"offset": 8})
    test_expression_result({"offset": 9})

def body_test():
    test_student_typed('5', not_typed_msg = "incorrect_if")

def orelse_test():
    def test_test2():
        test_expression_result({"offset": 4})
        test_expression_result({"offset": 5})
        test_expression_result({"offset": 6})
    def body_test2():
        test_student_typed('7', not_typed_msg = 'incorrect_elif')
    def orelse_test2():
        test_function('round')
    test_if_else(index = 1,
                  test = test_test2,
                  body = body_test2,
                  orelse = orelse_test2,
                  expand_message = False)

test_if_else(index=1,
             test=test_test,
             body=body_test,
             orelse=orelse_test,
             expand_message = False)

success_msg("Nice")
            '''
        }
        self.IF_EXP_SOLUTION = '''
offset = 8
x = 5 if offset > 8 else 7 if offset > 5 else round(9)
'''

    def testPass(self):
        self.data["DC_CODE"] = '''
offset = 8
if offset > 8:
    x = 5
elif offset > 5:
    x = 7
else:
    x = round(9)
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_file_if_cond(self):
        self.data["DC_CODE"] = '''
offset = 8
if offset > 9:
    x = 5
elif offset > 5:
    x = 7
else:
    x = round(9)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Unexpected expression", sct_payload['message'])
        helper.test_lines(self, sct_payload, 3, 3, 4, 13)

    def test_fail_if_body(self):
        self.data["DC_CODE"] = '''
offset = 8
if offset > 8:
    x = 6
elif offset > 5:
    x = 7
else:
    x = round(9)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "incorrect_if")
        helper.test_lines(self, sct_payload, 4, 4, 5, 9)

    def test_fail_elif_cond(self):
        self.data["DC_CODE"] = '''
offset = 8
if offset > 8:
    x = 5
elif offset > 6:
    x = 7
else:
    x = round(9)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Unexpected expression", sct_payload['message'])
        helper.test_lines(self, sct_payload, 5, 5, 6, 15)

    def test_fail_elif_body(self):
        self.data["DC_CODE"] = '''
offset = 8
if offset > 8:
    x = 5
elif offset > 5:
    x = 8
else:
    x = round(9)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "incorrect_elif")
        helper.test_lines(self, sct_payload, 6, 6, 5, 9)

    def test_fail_else_body(self):
        self.data["DC_CODE"] = '''
offset = 8
if offset > 8:
    x = 5
elif offset > 5:
    x = 7
else:
    x = round(10)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>round()</code> with the correct arguments?", sct_payload['message'])
        # should be localized
        helper.test_lines(self, sct_payload, 8, 8, 15, 16)

    def testPass_if_exp(self):
        self.data["DC_SOLUTION"] = self.IF_EXP_SOLUTION
        self.data["DC_SCT"] = helper.replace_test_if(self.data["DC_SCT"])
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail_if_cond_if_exp(self):
        self.data["DC_SOLUTION"] = self.IF_EXP_SOLUTION
        self.data["DC_CODE"] = "x = 5 if offset > 9 else 7 if offset > 5 else round(9)"
        self.data["DC_SCT"] = helper.replace_test_if(self.data["DC_SCT"])
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Unexpected expression", sct_payload['message'])
        #helper.test_lines(self, sct_payload, 3, 3, 4, 13)

    def test_fail_if_body_if_exp(self):
        self.data["DC_SOLUTION"] = self.IF_EXP_SOLUTION
        self.data["DC_CODE"] = "x = 6 if offset > 8 else 7 if offset > 5 else round(9)"
        self.data["DC_SCT"] = helper.replace_test_if(self.data["DC_SCT"])
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "incorrect_if")

    def test_fail_elif_cond_if_exp(self):
        self.data["DC_SOLUTION"] = self.IF_EXP_SOLUTION
        self.data["DC_CODE"] = "x = 5 if offset > 8 else 7 if offset > 6 else round(9)"
        self.data["DC_SCT"] = helper.replace_test_if(self.data["DC_SCT"])
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Unexpected expression", sct_payload['message'])

    def test_fail_else_body_if_exp(self):
        self.data["DC_SOLUTION"] = self.IF_EXP_SOLUTION
        self.data["DC_CODE"] = "5 if offset > 8 else 7 if offset > 5 else round(10)"
        self.data["DC_SCT"] = helper.replace_test_if(self.data["DC_SCT"])
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Did you call <code>round()</code> with the correct arguments?", sct_payload['message'])

class TestIfExp(unittest.TestCase):
    def setUp(self):
        self.data = {
                "DC_SOLUTION": """
x = 2 if True else 1
def f(): 4 if True else 3
y = 5 if True else 4
                """,
                "DC_SCT": "test_if_exp(index=2, body=lambda: test_expression_result())",
                "DC_CODE": "x = 2 if True else 1; y = 5 if True else 4"
                }

    def test_if_exp_skips_func_body(self):
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_if_exp_within_func(self):
        self.data["DC_SCT"] = "test_function_definition('f', body=lambda: test_if_exp(1, body=lambda: test_expression_result()))"
        self.data["DC_CODE"] = "def f(): return 4 if True else 3"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_if_exp_within_func_fail(self):
        self.data["DC_SCT"] = "test_function_definition('f', body=lambda: test_if_exp(body=lambda: test_expression_result()))"
        self.data["DC_CODE"] = "def f(): return 'wrong' if True else 3"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()
