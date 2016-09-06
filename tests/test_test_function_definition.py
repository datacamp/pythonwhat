import unittest
import helper

# class TestExercise1(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": '',
#             "DC_SOLUTION": '''
# def shout ( word ):
#     shout_word = word + '!!!'
#     print( shout_word )
# shout( 'help' )
#             ''',
#             "DC_SCT": '''
# test_function_definition("shout", body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'Make sure to output the correct string.'))
# success_msg("Nice work!")
#             '''
#         }

#     def test_Pass(self):
#         self.data["DC_CODE"] = '''
# def shout ( word ):
#     shout_word = word + '!!!'
#     print( shout_word )
# shout( 'help' )
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_Fail(self):
#         self.data["DC_CODE"] = '''
# def shout ( word ):
#     shout_word = word + '!!!'
#     print( shout_word + "!!" )
# shout( 'help' )
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], "In your definition of <code>shout()</code>, make sure to output the correct string.")
#         helper.test_lines(self, sct_payload, 3, 4, 5, 30)

# class TestExercise2(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": '''''',
#             "DC_CODE": '''
# def shout ( word ):
#     shout_word = word + '!!!'
#     print( shout_word )
# shout( 'help' )
#             ''',
#             "DC_SOLUTION": '''
# def shout ( word, times = None):
#     shout_word = word + '!!!'
#     print( shout_word )
# shout( 'help' )
# '''
#         }

#     def test_Pass(self):
#         self.data["DC_SCT"] = '''
# test_function_definition("shout", arg_names=False, arg_defaults=False, body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'make sure to output the correct string.'))
# success_msg("Nice work man!")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_Fail(self):
#         self.data["DC_SCT"] = '''
# test_function_definition("shout", body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'make sure to output the correct string.'))
# success_msg("Nice work!")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], "You should define <code>shout()</code> with 2 arguments, instead got 1.")
#         helper.test_lines(self, sct_payload, 2, 4, 1, 23)

# class TestExercise3(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": '''''',
#             "DC_CODE": '''
# def shout ( word, times = 3 ):
#     shout_word = word + '???'
#     print( shout_word )
#     return word * times
#             ''',
#             "DC_SOLUTION": '''
# def shout ( word = 'help', times = 3 ):
#     shout_word = word + '!!!'
#     print( shout_word )
#     return word * times
# '''
#         }

#     def test_Fail1(self):
#         self.data["DC_SCT"] = '''
# test_function_definition('shout')
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         helper.test_lines(self, sct_payload, 2, 5, 1, 23)

#     def test_Pass1(self):
#         self.data["DC_SCT"] = '''
# test_function_definition('shout', arg_defaults = False)
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_Fail2(self):
#         self.data["DC_SCT"] = '''
# test_function_definition('shout', arg_defaults = False, outputs = [('help')], wrong_output_msg = "WRONG")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], "WRONG")
#         self.assertFalse(sct_payload['correct'])

#     def test_Pass2(self):
#         self.data["DC_SCT"] = '''
# test_function_definition('shout', arg_defaults = False, results = [('help')])
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_Pass3(self):
#         self.data["DC_SCT"] = '''
# test_function_definition('shout', arg_defaults = False, body = lambda: test_function('print', args=[]))
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])


# class TestExercise4(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": '''''',
#             "DC_CODE": '''
# def shout (word1, word2):
#     shout1 = word1 + '!!!'
#     shout2 = word2 + '!!!'
#     new_shout = word1 + word2
#     return new_shout
#             ''',
#             "DC_SOLUTION": '''
# def shout (word1, word2):
#     shout1 = word1 + '!!!'
#     shout2 = word2 + '!!!'
#     new_shout = word1 + word2
#     print(new_shout)
#     return new_shout
# '''
#         }

#     def test_Pass1(self):
#         self.data["DC_SCT"] = '''
# test_function_definition("shout")
# success_msg("Nice work man!")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_Pass2(self):
#         self.data["DC_SCT"] = '''
# test_function_definition("shout", results=[('help', 'fire')])
# success_msg("Nice work!")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_Fail1(self):
#         self.data["DC_SCT"] = '''
# test_function_definition("shout", outputs=[('help', 'fire')])
# success_msg("Nice work!")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], "Calling <code>shout('help', 'fire')</code> should output <code>helpfire</code>, instead got ``.")

# class TestExercise5(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": '',
#             "DC_CODE": '''
# def shout (word1, word2):
#     shout1 = word1 + '!!!'
#     shout2 = word2 + '!!!'
#     new_shout = word1 + word2
#     return new_shout
#                 ''',
#             "DC_SOLUTION": '''
# def shout (word1, word2, word3 = "nothing"):
#     shout1 = word1 + '!!!'
#     shout2 = word2 + '!!!'
#     new_shout = word1 + word2
#     print(new_shout)
#     return new_shout
#     '''
#             }

#     def test_Fail1(self):
#         self.data["DC_SCT"] = '''
# test_function_definition("shout")
# success_msg("Nice work!")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], 'You should define <code>shout()</code> with 3 arguments, instead got 2.')
#         helper.test_lines(self, sct_payload, 2, 6, 1, 20)

# class TestExercise6(unittest.TestCase):
#     def setUp(self):
#         self.data = {
#             "DC_PEC": '',
#             "DC_CODE": '''
# def shout (word1, word2):
#     shout1 = word1 + '!!!'
#     shout2 = word2 + '!!!'
#     new_shout = word1 + word2
#     return new_shout
#             ''',
#             "DC_SOLUTION": '''
# def shout (word1, word2):
#     shout1 = word1 + '!!!'
#     shout2 = word2 + '!!!'
#     new_shout = word1 + word2
#     print(new_shout)
#     return new_shout
# '''
#         }

#     def test_Pass1(self):
#         self.data["DC_SCT"] = '''
# test_function_definition("shout")
# success_msg("Nice work man!")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_Pass2(self):
#         self.data["DC_SCT"] = '''
# test_function_definition("shout", results=[('help', 'fire')])
# success_msg("Nice work!")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_Fail1(self):
#         self.data["DC_SCT"] = '''
# test_function_definition("shout", outputs=[('help', 'fire')])
# success_msg("Nice work!")
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], "Calling <code>shout('help', 'fire')</code> should output <code>helpfire</code>, instead got ``.")


# class TestExercise7(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": '''''',
#             "DC_SOLUTION": '''
# def to_decimal(number, base = 2):
#     print("Converting %d from base %s to base 10" % (number, base))
#     number_str = str(number)
#     number_range = range(len(number_str))
#     multipliers = [base ** ((len(number_str) - 1) - i) for i in number_range]
#     decimal = sum([int(number_str[i]) * multipliers[i] for i in number_range])
#     return decimal
#             ''',
#             "DC_SCT": '''
# test_function_definition("to_decimal", arg_defaults = True, arg_names = False)
# test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
#     results = [(1001101, 2),(1212357, 8)])
# test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
#     outputs = [(1234, 6),(8888888, 9)])
# test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
#     body = lambda: test_function("sum", args = [], incorrect_msg = "you should use the `sum()` function."))
# '''
#         }

#     def test_Fail1(self):
#         self.data["DC_CODE"] = '''
# def to_decimal(number, base = 3):
#     print("Converting %d from base %s to base 10" % (number, base))
#     number_str = str(number)
#     number_range = range(len(number_str))
#     multipliers = [base ** ((len(number_str) - 1) - i) for i in number_range]
#     decimal = sum([int(number_str[i]) * multipliers[i] for i in number_range])
#     return decimal
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], 'In your definition of <code>to_decimal()</code>, the second argument should have <code>2</code> as default, instead got <code>3</code>.')
#         helper.test_lines(self, sct_payload, 2, 8, 1, 18)

#     def test_Fail2(self):
#         self.data["DC_CODE"] = '''
# from numpy import sum
# def to_decimal(number, base = 2):
#     print("Converting %d from base %s to base 10" % (number, base))
#     number_str = str(number)
#     number_range = range(len(number_str))
#     multipliers = [base ** ((len(number_str) - 1) - i) for i in number_range]
#     decimal = sum([int(number_str[i]) * multipliers[i] for i in number_range])
#     return decimal
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

# class TestExercise8(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": '''''',
#             "DC_SOLUTION": '''
# def shout():
#     shout_word = 'congratulations' + '!!!'
#     print(shout_word)
#             ''',
#             "DC_SCT": '''
# test_function_definition(
#     "shout",
#     arg_names = False,
#     body = lambda: test_object_after_expression("shout_word"))

# '''
#         }

#     def test_Pass(self):
#         self.data["DC_CODE"] = '''
# def shout():
#     shout_word = 'congratulations' + '!!!'
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_Fail1(self):
#         self.data["DC_CODE"] = '''
# def shout():
#     shout_word = 'congratulations' + '!!'
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], 'In your definition of <code>shout()</code>, are you sure you assigned the correct value to <code>shout_word</code>?')
#         # line info specific to test_object_after_expression!
#         helper.test_lines(self, sct_payload, 3, 3, 5, 41)

# class TestExercise9(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": '''''',
#             "DC_SOLUTION": '''
# def shout(word):
#     shout_word = word + '!!!'
#     print(shout_word)
# shout('congratulations')
#             ''',
#             "DC_SCT": '''
# test_function_definition("shout", arg_names = True)
# test_function_definition(
#         "shout",
#         arg_names = False,
#         body = lambda: test_object_after_expression("word", context_vals = ["congratulations"])
# )

# test_function_definition(
#         "shout",
#         arg_names = False,
#         body = lambda: test_object_after_expression("shout_word", context_vals = ["congratulations!!!"])
# )

# test_function_definition("shout", arg_names = False, arg_defaults = False, # Already tested this
#         body = lambda: [
#             set_extra_env(extra_env={'shout_word': "congratulations"}),
#             test_function("print", incorrect_msg = "You should use the `print()` function with the correct argument.")])
# '''
#         }

#     def test_Fail1(self):
#         self.data["DC_CODE"] = '''
# def shout(word):
#     shout_word = word + '!!!'
#     print(shout_word + '!')
# shout('congratulations')
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], 'In your definition of <code>shout()</code>, you should use the <code>print()</code> function with the correct argument.')
#         # line info specific to test_function!
#         helper.test_lines(self, sct_payload, 4, 4, 11, 26)

#     def test_Fail2(self):
#         self.data["DC_CODE"] = '''
# def shout(word):
#     shout_word = 'congratulations' + '!!'
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual(sct_payload['message'], 'In your definition of <code>shout()</code>, are you sure you assigned the correct value to <code>shout_word</code>?')
#         # line info specific to test_object_after_expression!
#         helper.test_lines(self, sct_payload, 3, 3, 5, 41)

# class TestFunctionDefintionError1(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": "",
#             "DC_SOLUTION": '''
# def inc(num):
#     if num < 0:
#         raise ValueError('num is negative')
#     return(num + 1)
#             ''',
#             "DC_SCT": '''
# test_function_definition("inc",
#                          errors = [[-1]])
#             '''
#         }

#     def test_pass(self):
#         self.data["DC_CODE"] = '''
# def inc(num):
#     if num < 0:
#         raise ValueError('num is negative')
#     return(num + 1)
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_fail_1(self):
#         self.data["DC_CODE"] = '''
# def inc(num):
#     return(num + 1)
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual("Calling <code>inc(-1)</code> doesn't result in an error, but it should!", sct_payload['message'])

#     def test_fail_2(self):
#         self.data["DC_CODE"] = '''
# def inc(num):
#     if num < 0:
#         raise NameError('num is negative')
#     return(num + 1)
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual("Calling <code>inc(-1)</code> should result in a <code>ValueError</code>, instead got a <code>NameError</code>.", sct_payload['message'])

# class TestFunctionDefintionError2(unittest.TestCase):

#     def setUp(self):
#         self.data = {
#             "DC_PEC": "",
#             "DC_SOLUTION": '''
# def inc(num):
#     if num < 0:
#         raise ValueError('num is negative')
#     return(num + 1)
#             ''',
#             "DC_SCT": '''
# test_function_definition("inc",
#                          errors = [[-1]],
#                          no_error_msg = 'noerror!',
#                          wrong_error_msg = 'wrongerror!')
#             '''
#         }

#     def test_pass(self):
#         self.data["DC_CODE"] = '''
# def inc(num):
#     if num < 0:
#         raise ValueError('num is negative')
#     return(num + 1)
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertTrue(sct_payload['correct'])

#     def test_fail_1(self):
#         self.data["DC_CODE"] = '''
# def inc(num):
#     return(num + 1)
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual("noerror!", sct_payload['message'])

#     def test_fail_2(self):
#         self.data["DC_CODE"] = '''
# def inc(num):
#     if num < 0:
#         raise NameError('num is negative')
#     return(num + 1)
#         '''
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual("wrongerror!", sct_payload['message'])

# class TestFunctionDefinitionOnlyReturn(unittest.TestCase):
#     def test_pass(self):
#         self.data = {
#             "DC_PEC": "",
#             "DC_SCT": '''
# def inner_test():
#     test_object_after_expression("shout_word",
#     context_vals = ["congratulations"])
# test_function_definition("shout",  body = inner_test, results = [("congratulations")])
#             ''',
#             "DC_SOLUTION": '''
# def shout(word):
#     shout_word = word + '!!!'
#     return shout_word
#             ''',
#             "DC_CODE": '''
# def shout(word):
#     # shout_word = word + '!!!'
#     return shout_word
#             '''
#         }
#         sct_payload = helper.run(self.data)
#         self.assertFalse(sct_payload['correct'])
#         self.assertEqual("In your definition of <code>shout()</code>, have you defined <code>shout_word</code>?", sct_payload['message'])

class TestFunctionDefinitionArgsAndKwargs(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
def my_fun(x, *args, **kwargs):
    print(x)
    print(args)
    print(kwargs)
my_fun('test', 'a', 'b', y = 2, z = 3)
            ''',
            "DC_SCT": '''
test_function_definition("my_fun")
            '''}

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTruee(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()
