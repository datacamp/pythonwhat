import unittest
import helper
import pytest

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
        self.assertIn("Check the first for loop. Did you correctly specify the sequence part?", sct_payload['message'])
        self.assertIn("Check your call of <code>range()</code>.", sct_payload['message'])
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
        self.assertIn("Check the first for loop. Did you correctly specify the body?", sct_payload['message'])
        self.assertIn("Are you sure you assigned the correct value to <code>size</code>?", sct_payload['message'])
        # should be detailed
        helper.test_lines(self, sct_payload, 4, 4, 5, 23)

    def test_Pass_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Pass()

    def test_Fail_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Fail()
        
    def test_Fail_mix_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"], count=1)
        self.test_Fail()

    def test_Pass_exchain(self):
        self.data["DC_SCT"] = "Ex().\\" + helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Pass()

    def test_has_context_pass(self):
        self.data["DC_CODE"] = "for i in range(10): pass"
        self.data["DC_SCT"] = "Ex().check_for_loop(0).has_context()"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_has_context_mult_pass(self):
        self.data["DC_SOLUTION"] = "for x,y in zip(range(10), range(10)): pass"
        self.data["DC_CODE"] = "for i,j in zip(range(10), range(10)): pass"
        self.data["DC_SCT"] = "Ex().check_for_loop(0).has_context()"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_has_context_fail(self):
        self.data["DC_CODE"] = "for i in range(10): pass"
        self.data["DC_SCT"] = "Ex().check_for_loop(0).has_context(exact_names=True)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_has_context_mult_fail(self):
        self.data["DC_SOLUTION"] = "for x,y in zip(range(10), range(10)): pass"
        self.data["DC_CODE"] = "for i,j in zip(range(10), range(10)): pass"
        self.data["DC_SCT"] = "Ex().check_for_loop(0).has_context(exact_names=True)"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

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
        self.assertEqual("blabla", sct_payload['message'])
        helper.test_lines(self, sct_payload, 4, 4, 5, 67)

    def test_Pass_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Pass()

    def test_Fail_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Fail()

    def test_Fail_mix_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"], count=1)
        self.test_Fail()

    def test_Pass_spec(self):
        self.data["DC_SCT"] = '''
SPEC2 = True
msg = "loopinggonewrong"
forl = Ex().check_for_loop(0)

forl.check_iter()\
    .multi(test_function("enumerate", incorrect_msg=msg))

msg = "blabla"
forl.check_body()\
    .multi(test_expression_output(incorrect_msg = msg, context_vals = [2, "test"]))

success_msg("Well done!")
'''
        self.test_Pass()

class TestForLoopNested(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
for ii in range(1, 2):
    for jj in list(range(ii)):
        x = sum([ii,jj])
            ''',
            "DC_SCT": '''

Ex().check_for_loop(0)\
    .check_body()\
    .set_context(ii=1)\
        .check_for_loop(0)\
        .check_body()\
        .set_context(jj=2)\
        .multi(test_function('sum', incorrect_msg="wronginnerfor"))
        '''
        }

    def test_Pass(self):
        self.data["DC_CODE"] = self.data['DC_SOLUTION'].replace('ii', 'aa').replace('jj', 'bb')
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail(self):
        self.data["DC_CODE"] = '''
for ii in range(1, 2):
    for jj in list(range(ii)):
        x = sum([ii+1,jj])
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('wronginnerfor', sct_payload['message'])

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
