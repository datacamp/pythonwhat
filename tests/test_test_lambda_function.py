import unittest
import helper


class TestLambdaFunctionStepByStep(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "echo_word = lambda word, echo = 1: word * echo",
            "DC_SCT": '''
test_lambda_function(1,
                     body = lambda: test_student_typed('word'),
                     results = ["lam('test', 2)"],
                     errors = ["lam('a', '2')"])
            '''
        }

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the first lambda function you defined but hasn't found it.")

    def test_fail_2(self):
        self.data["DC_CODE"] = "echo_word = lambda wrd: wrd * 1"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "You should define the first lambda function with 2 arguments, instead got 1.")
        helper.test_lines(self, sct_payload, 1, 1, 13, 31)

    def test_fail_3(self):
        self.data["DC_CODE"] = "echo_word = lambda wrd, echo: wrd * echo"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "In your definition of the first lambda function, the first argument should be called <code>word</code>, instead got <code>wrd</code>.")
        helper.test_lines(self, sct_payload, 1, 1, 13, 40)

    def test_fail_4(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 2: word * echo"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "In your definition of the first lambda function, the second argument should have <code>1</code> as default, instead got <code>2</code>.")        
        helper.test_lines(self, sct_payload, 1, 1, 13, 46)

    def test_fail_5(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: 2 * echo"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "In your definition of the first lambda function, could not find the correct pattern in your code.")        
        helper.test_lines(self, sct_payload, 1, 1, 36, 43)

    def test_fail_6(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: word * echo + 1"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Calling the the first lambda function with arguments <code>('test', 2)</code> should result in <code>testtest</code>, instead got an error.")
        helper.test_lines(self, sct_payload, 1, 1, 13, 50)

    def test_fail_7(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: word * echo * 2"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Calling the first lambda function with arguments <code>('test', 2)</code> should result in <code>testtest</code>, instead got <code>testtesttesttest</code>.")
        helper.test_lines(self, sct_payload, 1, 1, 13, 50)

    def test_fail_8(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: word * int(echo)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Calling the first lambda function with the arguments <code>('a', '2')</code> doesn't result in an error, but it should!")
        helper.test_lines(self, sct_payload, 1, 1, 13, 51)

    def test_pass(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: word * echo"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestLambdaFunctionStepByStepCustom(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "echo_word = lambda word, echo = 1: word * echo",
            "DC_SCT": '''
test_lambda_function(1,
                     body = lambda: test_student_typed('word'),
                     results = ["lam('test', 2)"],
                     errors = ["lam('a', '2')"],
                     not_called_msg='notcalled',
                     nb_args_msg='nbargs',
                     arg_names_msg='argnames',
                     arg_defaults_msg='argdefaults',
                     wrong_result_msg='wrongresult',
                     no_error_msg='noerror',
                     expand_message=False)
            '''
        }

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "notcalled")

    def test_fail_2(self):
        self.data["DC_CODE"] = "echo_word = lambda wrd: wrd * 1"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "nbargs")

    def test_fail_3(self):
        self.data["DC_CODE"] = "echo_word = lambda wrd, echo: wrd * echo"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "argnames")

    def test_fail_4(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 2: word * echo"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "argdefaults")        

    def test_fail_5(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: 2 * echo"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Could not find the correct pattern in your code.")        

    def test_fail_6(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: word * echo + 1"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "wrongresult")

    def test_fail_7(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: word * echo * 2"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "wrongresult")

    def test_fail_8(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: word * int(echo)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "noerror")

    def test_pass(self):
        self.data["DC_CODE"] = "echo_word = lambda word, echo = 1: word * echo"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestLambdaFunctionDifferentform(unittest.TestCase):
    def test_pass(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "echo_word = lambda word, echo = 1: word * echo",
            "DC_CODE": "(lambda word, echo = 1: word * echo)('test', 3)",
            "DC_SCT": '''
test_lambda_function(1,
                     body = lambda: test_student_typed('word'),
                     results = ["lam('test', 2)"],
                     errors = ["lam('a', '2')"])
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

if __name__ == "__main__":
     unittest.main()



