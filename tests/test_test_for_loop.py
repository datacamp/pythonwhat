import unittest
import helper

class TestForLoop(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
size = 1
for n in range(10):
    size = size + 2*n
    size = size - n
    x = "%d:%d" % (n, size)
''',
            "DC_SCT": '''
test_for_loop(1,
              lambda: test_function("range"),
              lambda: test_object_after_expression("size", {"size": 1}, [1]))
success_msg("Great!")
'''
        }

    def test_Pass(self):
        self.data["DC_CODE"] = '''
size = 1
for i in range(10):
    size = size + i
    x = "%d:%d" % (i, size)
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Great!")

    def test_Fail(self):
        self.data["DC_CODE"] = '''
size = 1
for i in range(20):
    size = size + i
    x = "%d:%d" % (i, size)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the sequence part of the first <code>for</code> loop", sct_payload['message'])
        self.assertIn("Did you call <code>range()</code> with the correct arguments?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 3, 3, 16, 17)

    def test_Fail2(self):
        self.data["DC_CODE"] = '''
size = 1
for i in range(10):
    size = size + i + 1
    x = "%d:%d" % (i, size)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the body of the first <code>for</code> loop", sct_payload['message'])
        self.assertIn("Are you sure you assigned the correct value to <code>size</code>?", sct_payload['message'])
        # should be detailed
        helper.test_lines(self, sct_payload, 4, 4, 5, 23)

class TestForLoop2(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
areas = [11.25, 18.0, 20.0, 10.75, 9.50]
for index, area in enumerate(areas) :
    print("room " + str(index) + ": " + str(area))
            ''',
            "DC_SCT": '''
msg = "loopinggonewrong"
test_for_loop(1, for_iter=lambda msg=msg: test_function("enumerate", incorrect_msg = msg))

msg = "blabla"
test_for_loop(1, body=lambda msg=msg: test_expression_output(incorrect_msg = msg, context_vals = [2, "test"]))
success_msg("Well done!")
        '''
        }

    def test_Pass(self):
        self.data["DC_CODE"] = '''
areas = [11.25, 18.0, 20.0, 10.75, 9.50]
for test in enumerate(areas) :
    print("room " + str(test[0]) + ": " + str(test[1]))
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Well done!")

    def test_Fail(self):
        self.data["DC_CODE"] = '''
areas = [11.25, 18.0, 20.0, 10.75, 9.50]
for test in enumerate(areas) :
    print("roomrettektetetet" + str(test[0]) + ": " + str(test[1]))
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the body of the first <code>for</code> loop", sct_payload['message'])
        self.assertIn("blabla", sct_payload['message'])
        helper.test_lines(self, sct_payload, 4, 4, 5, 67)

if __name__ == "__main__":
    unittest.main()
