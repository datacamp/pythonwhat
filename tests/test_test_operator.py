import unittest
import helper

class TestTestOperatorSameOperation(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '# pec comes here',
            "DC_CODE": '5 / 8',
            "DC_SOLUTION": '5 / 8'
        }

    def test_operatorArgument(self):
        self.data["DC_SCT"] = '''
test_operator(1)
success_msg("Great!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Great!")

    def test_operatorNoArgument(self):
        self.data["DC_SCT"] = '''
test_operator()
success_msg("Great! No arguments!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Great! No arguments!")

        

class TestTestOperatorSameOperationInFunction(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '# pec comes here',
            "DC_CODE": '5 / 8',
            "DC_SOLUTION": '5 / 8'
        }

    def test_operatorArgument(self):
        self.data["DC_SCT"] = '''
test_operator(1)
success_msg("Great!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Great!")

    def test_operatorNoArgument(self):
        self.data["DC_SCT"] = '''
test_operator()
success_msg("Great! No arguments!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Great! No arguments!")

class TestTestOperatorLessOperations(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '# pec comes here',
            "DC_CODE": '5 / 8',
            "DC_SOLUTION": 'print(5 / 8)\nprint(7 + 10)'
        }

    def test_firstOperation(self):
        self.data["DC_SCT"] = '''
test_operator(1)
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Well done!")

    def test_secondOperation(self):
        self.data["DC_SCT"] = '''
test_operator(2)
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "You didn't define enough operations in your code.")

class TestTestOperatorSameTwoOperations(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": 'print(5 / 8)\nprint(7 + 10)',
            "DC_SOLUTION": 'print(5 / 8)\nprint(7 + 10)'
        }

    def test_firstOperation(self):
        self.data["DC_SCT"] = '''
test_operator(1)
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Well done!")

    def test_secondOperation(self):
        self.data["DC_SCT"] = '''
test_operator(2)
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Well done!")

    def test_bothOperations(self):
        self.data["DC_SCT"] = '''
test_operator(1)
test_operator(2)
success_msg("Well done! Both correct!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Well done! Both correct!")

class TestTestOperatorTwoOperationsOneIncorrect(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": 'print(5 / 8)\nprint(7 + 10)',
            "DC_SOLUTION": 'print(5 / 8)\nprint(3 + 10)'
        }

    def test_firstOperation(self):
        self.data["DC_SCT"] = '''
test_operator(1)
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Well done!")

    def test_secondOperation(self):
        self.data["DC_SCT"] = '''
test_operator(2)
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Your operation at line 3 evaluates to 17, should be 13.")

    def test_bothOperations(self):
        self.data["DC_SCT"] = '''
test_operator(1)
test_operator(2)
success_msg("Well done! Both correct!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Your operation at line 3 evaluates to 17, should be 13.")

class TestTestOperatorTwoOperationsOneIncorrect(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": 'print(4 / 8)\nprint(7 + 10)',
            "DC_SOLUTION": 'print(5 / 8)\nprint(3 + 10)'
        }

    def test_firstOperation(self):
        self.data["DC_SCT"] = '''
test_operator(1)
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Your operation at line 2 evaluates to 0.5, should be 0.625.")

    def test_secondOperation(self):
        self.data["DC_SCT"] = '''
test_operator(2)
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Your operation at line 3 evaluates to 17, should be 13.")

    def test_bothOperations(self):
        self.data["DC_SCT"] = '''
test_operator(1)
test_operator(2)
success_msg("Well done! Both correct!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Your operation at line 2 evaluates to 0.5, should be 0.625.")

class TestTestOperatorTwoOperationsOneIncorrect(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": 'print(4 / 8)\nprint(7 + 10)',
            "DC_SOLUTION": 'print(5 / 8)\nprint(3 + 10)\nprint(3 - 5)'
        }

    def test_firstOperation(self):
        self.data["DC_SCT"] = '''
test_operator(3, not_found_msg = 'Not enough operations!')
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Not enough operations!")

    def test_secondOperation(self):
        self.data["DC_SCT"] = '''
test_operator(2, incorrect_result_msg = 'Not quite right...')
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Not quite right...")

class TestTestOperatorIncorrectOperation(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": 'print(3 + 3)',
            "DC_SOLUTION": 'print(3 * 2)'
        }

    def test_allOperations(self):
        self.data["DC_SCT"] = '''
test_operator(1)
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Your operation at line 1 is missing a <code>*</code> operation.")

    def test_allOperationsWithCustomFeedback(self):
        self.data["DC_SCT"] = '''
test_operator(1, incorrect_op_msg = "Nope")
success_msg("Well done!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], False)
        self.assertEqual(sct_payload['message'], "Nope")
    def test_ignoreOperations(self):
        self.data["DC_SCT"] = '''
test_operator(1, used=[])
success_msg("You don't have to use the same operations.")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "You don't have to use the same operations.")

if __name__ == "__main__":
    unittest.main()
