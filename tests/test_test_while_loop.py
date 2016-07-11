import unittest
import helper

class TestWhileLoop(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '''
# Initialize offset
offset = 8

# Code the while loop
while offset != 0 :
    print("correcting...")
    offset = offset - 1
    print(offset)
            ''',
            "DC_SOLUTION": '''
# Initialize offset
offset = 8

# Code the while loop
while offset != 0 :
    print("correcting...")
    offset = offset - 1
    print(offset)
'''
        }

    def test_Pass(self):
        self.data["DC_SCT"] = '''
test_object("offset")

for i in range(-1,2):
    test_while_loop(1, test=lambda i=i: test_expression_result({"offset": i}))

for i in range(3,4):
    test_while_loop(1, body=lambda i=i: test_object_after_expression("offset", {"offset": i}))
    test_while_loop(1, body=lambda i=i: test_expression_output({"offset": i}))

success_msg("Great!")
        '''
        sct_payload = helper.run(self.data)
        self.assertEqual(sct_payload['correct'], True)
        self.assertEqual(sct_payload['message'], "Great!")


if __name__ == "__main__":
    unittest.main()
