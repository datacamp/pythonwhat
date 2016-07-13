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
        self.assertEqual(sct_payload['line_start'], 6)
        self.assertEqual(sct_payload['line_end'], 6)
        self.assertEqual(sct_payload['column_start'], 4)
        self.assertEqual(sct_payload['column_end'], 14)

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
        self.assertEqual(sct_payload['line_start'], 7)
        self.assertEqual(sct_payload['line_end'], 7)
        self.assertEqual(sct_payload['column_start'], 5)
        self.assertEqual(sct_payload['column_end'], 9)

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
        self.assertEqual(sct_payload['line_start'], 7)
        self.assertEqual(sct_payload['line_end'], 8)
        self.assertEqual(sct_payload['column_start'], 5)
        self.assertEqual(sct_payload['column_end'], 10)

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
        self.assertEqual(sct_payload['line_start'], 9)
        self.assertEqual(sct_payload['line_end'], 9)
        self.assertEqual(sct_payload['column_start'], 5)
        self.assertEqual(sct_payload['column_end'], 9)

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
        self.assertEqual(sct_payload['line_start'], 9)
        self.assertEqual(sct_payload['line_end'], 9)
        self.assertEqual(sct_payload['column_start'], 15)
        self.assertEqual(sct_payload['column_end'], 23)


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
        self.assertEqual(sct_payload['line_start'], 3)
        self.assertEqual(sct_payload['line_end'], 3)
        self.assertEqual(sct_payload['column_start'], 4)
        self.assertEqual(sct_payload['column_end'], 13)

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
        self.assertEqual(sct_payload['line_start'], 4)
        self.assertEqual(sct_payload['line_end'], 4)
        self.assertEqual(sct_payload['column_start'], 5)
        self.assertEqual(sct_payload['column_end'], 9)

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
        self.assertEqual(sct_payload['line_start'], 5)
        self.assertEqual(sct_payload['line_end'], 5)
        self.assertEqual(sct_payload['column_start'], 6)
        self.assertEqual(sct_payload['column_end'], 15)

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
        self.assertEqual(sct_payload['line_start'], 6)
        self.assertEqual(sct_payload['line_end'], 6)
        self.assertEqual(sct_payload['column_start'], 5)
        self.assertEqual(sct_payload['column_end'], 9)

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
        self.assertEqual(sct_payload['line_start'], 8)
        self.assertEqual(sct_payload['line_end'], 8)
        self.assertEqual(sct_payload['column_start'], 15)
        self.assertEqual(sct_payload['column_end'], 16)

if __name__ == "__main__":
    unittest.main()
