import unittest
import helper

class TestExercise1(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''''',
            "DC_CODE": '''
def shout():
    shout_word = 'congratulation' + '!!!'
    return(shout_word)
            ''',
            "DC_SOLUTION": '''
def shout():
    shout_word = 'congratulations' + '!!!'
    return(shout_word)
            ''',
            "DC_SCT": '''
# Test the value of shout_word
test_function_definition("shout", arg_names = False,body = lambda: test_object_after_expression("shout_word",undefined_msg = "have you defined `shout_word`?", incorrect_msg = "test"))
success_msg("Nice work!")
        '''
        }

    def test_Pass(self):
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'test')
        helper.test_lines(self, sct_payload, 3, 3, 5, 41)

    def test_Pass2(self):
        self.data["DC_SCT"] = '''
# Test the value of shout_word
test_function_definition("shout", arg_names = False, body = lambda: test_object_after_expression("shout_word", undefined_msg = "have you defined `shout_word`?"))
success_msg("Nice work!")
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Check your definition of <code>shout()</code>. Did you correctly specify the body? Are you sure you assigned the correct value to <code>shout_word</code>?')
        helper.test_lines(self, sct_payload, 3, 3, 5, 41)

    def test_Pass_expr_code(self):
        self.data["DC_SCT"] = '''
# Test the value of shout_word
test_function_definition("shout", arg_names = False, body = lambda: test_object_after_expression("a", expr_code = "a = 1", undefined_msg = "have you defined `a`?"))
success_msg("Nice work!")
'''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


    def test_Pass_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Pass()

if __name__ == "__main__":
    unittest.main()
