import unittest
import helper

class TestWhileLoop(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
offset = 8
while offset != 0 :
    offset = offset - 1
            ''',
            "DC_SCT": '''
for i in range(-1,2):
    test_while_loop(1, test=lambda i=i: test_expression_result({"offset": i}))

for i in range(3,4):
    test_while_loop(1, body=lambda i=i: test_object_after_expression("offset", {"offset": i}))

success_msg("Great!")
            '''
        }

    def test_Pass(self):
        self.data["DC_CODE"] = '''
offset = 8
while offset != 0 :
    offset = offset - 1
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Great!")

    def test_Fail(self):
        self.data["DC_CODE"] = '''
offset = 8
while offset != 4 :
    offset = offset - 1
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check the first while loop. Did you correctly specify the condition?", sct_payload['message'])
        self.assertIn("Expected <code>", sct_payload['message'])
        helper.test_lines(self, sct_payload, 3, 3, 7, 17)

    def test_Fail2(self):
        self.data["DC_CODE"] = '''
offset = 8
while offset != 0 :
    offset = offset - 2
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check the first while loop. Did you correctly specify the body?", sct_payload['message'])
        self.assertIn("Are you sure you assigned the correct value to <code>offset</code>", sct_payload['message'])
        helper.test_lines(self, sct_payload, 4, 4, 5, 23)

    def test_Pass_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"], with_args=True)
        self.test_Pass()

    def test_Fail2_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"], with_args=True)
        self.test_Fail2()

if __name__ == "__main__":
    unittest.main()
