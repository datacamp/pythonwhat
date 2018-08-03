import unittest
import helper
import pytest

class TestFunctionDefinitionStepByStep(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": "def test(a, b = 2):\n    print('prod of ' + str(a) + ' and ' + str(b))\n    return a * b",
            "DC_SCT": "test_function_definition('test', results = [[2, 3]], outputs = [[2,3]], errors = [['a', 'b']])"
        }
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]

    def tearDown(self):
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_step_x(self):
        pass

    def test_step_x_spec2(self):
        self.data['DC_SCT'] = """
cargs = {'args': [2, 3], 'kwargs': {}}
eargs = {'args': ['a', 'b'], 'kwargs': {}}
(Ex().check_function_def('test').call(cargs, 'value').call(cargs, 'output').call(eargs, 'error'))
        """

    def test_step_x_spec2_str_call(self):
        self.data['DC_SCT'] = """
(Ex().check_function_def('test').call("f(1,2)", 'value').call("f(1,2)", 'output')
                                .call("f('a','b')", 'error'))
"""

    def test_step_x_spec2_func_arg(self):
        self.data['DC_SCT'] = """
import numpy as np
Ex().check_function_def('test').call("f(1,2)", func = lambda x, y: np.allclose(x, y))
"""


class TestExercise1(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
def shout ( word ):
    shout_word = word + '!!!'
    print( shout_word )
shout( 'help' )
            ''',
            "DC_SCT": '''
test_function_definition("shout", body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'Make sure to output the correct string.'))
success_msg("Nice work!")
            '''
        }

    def test_Pass(self):
        self.data["DC_CODE"] = '''
def shout ( word ):
    shout_word = word + '!!!'
    print( shout_word )
shout( 'help' )
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail(self):
        self.data["DC_CODE"] = '''
def shout ( word ):
    shout_word = word + '!!!'
    print( shout_word + "!!" )
shout( 'help' )
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Make sure to output the correct string.")
        helper.test_lines(self, sct_payload, 3, 4, 5, 30)

    def test_Pass_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Pass()

    def test_Fail_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Fail()

    def test_Pass_spec2(self):
        self.data["DC_SCT"] = """Ex().check_function_def("shout").check_body().set_context(word="help").test_expression_output()"""
        self.test_Pass()

class TestExercise2(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''''',
            "DC_CODE": '''
def shout ( word ):
    shout_word = word + '!!!'
    print( shout_word )
shout( 'help' )
            ''',
            "DC_SOLUTION": '''
def shout ( word, times = None):
    shout_word = word + '!!!'
    print( shout_word )
shout( 'help' )
'''
        }

    def test_Pass(self):
        self.data["DC_SCT"] = '''
test_function_definition("shout", arg_names=False, arg_defaults=False, body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'make sure to output the correct string.'))
success_msg("Nice work man!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail(self):
        self.data["DC_SCT"] = '''
test_function_definition("shout", body = lambda: test_expression_output(context_vals = ['help'], incorrect_msg = 'make sure to output the correct string.'))
success_msg("Nice work!")
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "You should define <code>shout()</code> with 2 arguments, instead got 1.")

        helper.test_lines(self, sct_payload, 2, 4, 1, 23)

    def test_Fail_spec2(self):
        self.data["DC_SCT"] = "Ex().check_function_def('shout').has_equal_part_len('args', 'wrong')"
        sct_payload = helper.run(self.data)
        self.assertTrue('wrong' in sct_payload['message'])
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

class TestExercise3(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''''',
            "DC_CODE": '''
def shout ( word, times = 3 ):
    shout_word = word + '???'
    print( shout_word )
    return word * times
            ''',
            "DC_SOLUTION": '''
def shout ( word = 'help', times = 3 ):
    shout_word = word + '!!!'
    print( shout_word )
    return word * times
            '''
        }

    def test_Fail1(self):
        self.data["DC_SCT"] = '''
test_function_definition('shout')
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        helper.test_lines(self, sct_payload, 2, 2, 13, 16)

    def test_Pass1(self):
        self.data["DC_SCT"] = '''
test_function_definition('shout', arg_defaults = False)
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail2(self):
        self.data["DC_SCT"] = '''
test_function_definition('shout', arg_defaults = False, outputs = [('help')], wrong_output_msg = "WRONG")
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "WRONG")
        self.assertFalse(sct_payload['correct'])

    def test_Pass2(self):
        self.data["DC_SCT"] = '''
test_function_definition('shout', arg_defaults = False, results = [('help')])
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass3(self):
        self.data["DC_SCT"] = '''
test_function_definition('shout', arg_defaults = False, body = lambda: test_function('print', args=[]))
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestExercise4(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''''',
            "DC_CODE": '''
def shout (word1, word2):
    shout1 = word1 + '!!!'
    shout2 = word2 + '!!!'
    new_shout = word1 + word2
    return new_shout
            ''',
            "DC_SOLUTION": '''
def shout (word1, word2):
    shout1 = word1 + '!!!'
    shout2 = word2 + '!!!'
    new_shout = word1 + word2
    print(new_shout)
    return new_shout
'''
        }

    def test_Pass1(self):
        self.data["DC_SCT"] = '''
test_function_definition("shout")
success_msg("Nice work man!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass2(self):
        self.data["DC_SCT"] = '''
test_function_definition("shout", results=[('help', 'fire')])
success_msg("Nice work!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail1(self):
        self.data["DC_SCT"] = '''
test_function_definition("shout", outputs=[('help', 'fire')])
success_msg("Nice work!")
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Calling <code>shout('help', 'fire')</code> should print out <code>helpfire</code>, instead got no printouts.")

class TestExercise5(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '''
def shout (word1, word2):
    shout1 = word1 + '!!!'
    shout2 = word2 + '!!!'
    new_shout = word1 + word2
    return new_shout
                ''',
            "DC_SOLUTION": '''
def shout (word1, word2, word3 = "nothing"):
    shout1 = word1 + '!!!'
    shout2 = word2 + '!!!'
    new_shout = word1 + word2
    print(new_shout)
    return new_shout
    '''
            }

    def test_Fail1(self):
        self.data["DC_SCT"] = '''
test_function_definition("shout")
success_msg("Nice work!")
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'You should define <code>shout()</code> with 3 arguments, instead got 2.')
        helper.test_lines(self, sct_payload, 2, 6, 1, 20)

class TestExercise6(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '''
def shout (word1, word2):
    shout1 = word1 + '!!!'
    shout2 = word2 + '!!!'
    new_shout = word1 + word2
    return new_shout
            ''',
            "DC_SOLUTION": '''
def shout (word1, word2):
    shout1 = word1 + '!!!'
    shout2 = word2 + '!!!'
    new_shout = word1 + word2
    print(new_shout)
    return new_shout
'''
        }

    def test_Pass1(self):
        self.data["DC_SCT"] = '''
test_function_definition("shout")
success_msg("Nice work man!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass2(self):
        self.data["DC_SCT"] = '''
test_function_definition("shout", results=[('help', 'fire')])
success_msg("Nice work!")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail1(self):
        self.data["DC_SCT"] = '''
test_function_definition("shout", outputs=[('help', 'fire')])
success_msg("Nice work!")
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Calling <code>shout('help', 'fire')</code> should print out <code>helpfire</code>, instead got no printouts.")


class TestExercise7(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''''',
            "DC_SOLUTION": '''
def to_decimal(number, base = 2):
    print("Converting %d from base %s to base 10" % (number, base))
    number_str = str(number)
    number_range = range(len(number_str))
    multipliers = [base ** ((len(number_str) - 1) - i) for i in number_range]
    decimal = sum([int(number_str[i]) * multipliers[i] for i in number_range])
    return decimal
            ''',
            "DC_SCT": '''
test_function_definition("to_decimal", arg_defaults = True, arg_names = False)
test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
    results = [(1001101, 2),(1212357, 8)])
test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
    outputs = [(1234, 6),(8888888, 9)])
test_function_definition("to_decimal", arg_names = False, arg_defaults = False, # Already tested this
    body = lambda: test_function("sum", args = [], incorrect_msg = "you should use the `sum()` function."))
'''
        }

    def test_Fail1(self):
        self.data["DC_CODE"] = '''
def to_decimal(number, base = 3):
    print("Converting %d from base %s to base 10" % (number, base))
    number_str = str(number)
    number_range = range(len(number_str))
    multipliers = [base ** ((len(number_str) - 1) - i) for i in number_range]
    decimal = sum([int(number_str[i]) * multipliers[i] for i in number_range])
    return decimal
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Check your definition of <code>to_decimal()</code>. The argument <code>base</code> does not have the correct default.')
        helper.test_lines(self, sct_payload, 2, 2, 31, 31)

    def test_Fail2(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail1_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Fail1()

    def test_Fail2_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Fail2()

class TestExercise8(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '''''',
            "DC_SOLUTION": '''
def shout():
    shout_word = 'congratulations' + '!!!'
    print(shout_word)
            ''',
            "DC_SCT": '''
test_function_definition(
    "shout",
    arg_names = False,
    body = lambda: test_object_after_expression("shout_word"))

'''
        }

    def test_Pass(self):
        self.data["DC_CODE"] = '''
def shout():
    shout_word = 'congratulations' + '!!!'
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Fail1(self):
        self.data["DC_CODE"] = '''
def shout():
    shout_word = 'congratulations' + '!!'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Check your definition of <code>shout()</code>. Did you correctly specify the body? Are you sure you assigned the correct value to <code>shout_word</code>?')
        # line info specific to test_object_after_expression!
        helper.test_lines(self, sct_payload, 3, 3, 5, 41)

    def test_Fail2(self):
        self.data["DC_CODE"] = '''
def shout():
    shout_word = 'congratulations' + '!!'
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Check your definition of <code>shout()</code>. Did you correctly specify the body? Are you sure you assigned the correct value to <code>shout_word</code>?')
        # line info specific to test_object_after_expression!
        helper.test_lines(self, sct_payload, 3, 3, 5, 41)

    def test_Pass_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Pass()

    def test_Fail1_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Fail1()

    def test_Fail2_no_lam(self):
        self.data["DC_SCT"] = helper.remove_lambdas(self.data["DC_SCT"])
        self.test_Fail2()

class TestFunctionDefintionError1(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
def inc(num):
    if num < 0:
        raise ValueError('num is negative')
    return(num + 1)
            ''',
            "DC_SCT": '''
test_function_definition("inc",
                         errors = [[-1]])
            '''
        }

    def test_pass(self):
        self.data["DC_CODE"] = '''
def inc(num):
    if num < 0:
        raise ValueError('num is negative')
    return(num + 1)
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_2(self):
        self.data["DC_CODE"] = '''
def inc(num):
    if num < 0:
        raise NameError('num is negative')
    return(num + 1)
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail_1(self):
        self.data["DC_CODE"] = '''
def inc(num):
    return(num + 1)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Calling <code>inc(-1)</code> should error out with the message <code>num is negative</code>, instead got <code>0</code>.", sct_payload['message'])

class TestFunctionDefintionError2(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
def inc(num):
    if num < 0:
        raise ValueError('num is negative')
    return(num + 1)
            ''',
            "DC_SCT": '''
test_function_definition("inc",
                         errors = [[-1]],
                         no_error_msg = 'noerror!',
                         wrong_error_msg = 'wrongerror!')
            '''
        }

    def test_pass(self):
        self.data["DC_CODE"] = '''
def inc(num):
    if num < 0:
        raise ValueError('num is negative')
    return(num + 1)
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass_2(self):
        self.data["DC_CODE"] = '''
def inc(num):
    if num < 0:
        raise NameError('num is negative')
    return(num + 1)
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail_1(self):
        self.data["DC_CODE"] = '''
def inc(num):
    return(num + 1)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("noerror!", sct_payload['message'])



class TestFunctionDefinitionOnlyReturn(unittest.TestCase):
    def test_pass(self):
        self.data = {
            "DC_PEC": "",
            "DC_SCT": '''
def inner_test():
    test_object_after_expression("shout_word",
    context_vals = ["congratulations"])
test_function_definition("shout",  body = inner_test, results = [("congratulations")])
            ''',
            "DC_SOLUTION": '''
def shout(word):
    shout_word = word + '!!!'
    return shout_word
            ''',
            "DC_CODE": '''
def shout(word):
    # shout_word = word + '!!!'
    return shout_word
            '''
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your definition of <code>shout()</code>. Did you correctly specify the body? Running it generated an error: <code>name 'shout_word' is not defined</code>.", sct_payload['message'])

class TestFunctionDefinitionNonLocal(unittest.TestCase):
    def test_pass(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
def echo_shout(word):
    echo_word = word*2
    print(echo_word)
    def shout():
        nonlocal echo_word
        echo_word = echo_word + '!!!'
    shout()
    print(echo_word)
echo_shout('hello')
            ''',
            "DC_SCT": '''
def inner_test():
    test_object_after_expression("echo_word", context_vals=["hello"])
    test_function_definition("shout")
    test_function("shout")
    test_function("print", args=[], index=1)
    test_function("print", args=[], index=2)
test_function_definition("echo_shout", body=inner_test)
test_function("echo_shout")
            '''
        }
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestFunctionDefinitionArgs(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
def my_fun(x, y = 4, z = ['a', 'b'], *args, **kwargs):
    k = len(args)
    l = len(kwargs)
    print("hello mister")
    return k + l
            ''',
            "DC_SCT": '''
def inner_test():
    context = ['r', 's', ['c', 'd'], ['t', 'u'], {'a': 2, 'b': 3, 'd':4}]
    test_object_after_expression('k', context_vals = context)
    test_object_after_expression('l', context_vals = context)
test_function_definition("my_fun", body = inner_test,
        results = [{'args': ['r', 's', ['c', 'd'], 't', 'u', 'v'], 'kwargs': {'a': 2, 'b': 3, 'd': 4}}],
        outputs = [{'args': ['r', 's', ['c', 'd'], 't', 'u', 'v'], 'kwargs': {'a': 2, 'b': 3, 'd': 4}}])
            '''}

    def test_fail_1(self):
        self.data["DC_CODE"] = '''
def my_fun(x):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("You should define <code>my_fun()</code> with 3 arguments, instead got 1.", sct_payload['message'])

    def test_fail_2(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("You should define <code>my_fun()</code> with 3 arguments, instead got 2.", sct_payload['message'])

    def test_fail_2(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 3):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("You should define <code>my_fun()</code> with 3 arguments, instead got 2.", sct_payload['message'])

    def test_fail_3(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 4):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("You should define <code>my_fun()</code> with 3 arguments, instead got 2.", sct_payload['message'])

    def test_fail_4(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 4, z = ['a', 'c']):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your definition of <code>my_fun()</code>. The argument <code>z</code> does not have the correct default.", sct_payload['message'])

    def test_fail_5(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 4, z = ['a', 'b']):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your definition of <code>my_fun()</code>. Have you specified an argument to take a <code>*</code> argument and named it <code>args</code>?", sct_payload['message'])

    def test_fail_6a(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 4, z = ['a', 'b'], *asdfasdf):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your definition of <code>my_fun()</code>. Have you specified an argument to take a <code>*</code> argument and named it <code>args</code>?", sct_payload['message'])


    def test_fail_6b(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 4, z = ['a', 'b'], *args):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your definition of <code>my_fun()</code>. Have you specified an argument to take a <code>**</code> argument and named it <code>kwargs</code>?", sct_payload['message'])

    def test_fail_7a(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 4, z = ['a', 'b'], *args, **asdfasdf):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your definition of <code>my_fun()</code>. Have you specified an argument to take a <code>**</code> argument and named it <code>kwargs</code>?", sct_payload['message'])

    def test_fail_7b(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 4, z = ['a', 'b'], *args, **kwargs):
    print(x)
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your definition of <code>my_fun()</code>. Did you correctly specify the body? Running it should define a variable <code>k</code> without errors, but it doesn't.", sct_payload['message'])

    def test_fail_8(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 4, z = ['a', 'b'], *args, **kwargs):
    k = len(kwargs)
    l = len(args)
    return k + l
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your definition of <code>my_fun()</code>. Did you correctly specify the body? Are you sure you assigned the correct value to <code>k</code>?", sct_payload['message'])

    def test_fail_9(self):
        self.data["DC_CODE"] = '''
def my_fun(x, y = 4, z = ['a', 'b'], *args, **kwargs):
    k = len(args)
    l = len(kwargs)
    return k + l
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        # in two pieces because order of dict not fixed
        self.assertIn("Calling <code>my_fun('r', 's', ['c', 'd'], 't', 'u', 'v'", sct_payload['message'])
        self.assertIn(")</code> should print out <code>hello mister</code>, instead got no printouts.", sct_payload['message'])

    def test_pass(self):
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestFunctionSpec2(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": '''
def my_fun(x, y = 4, z = ('a', 'b'), *args, **kwargs):
    return [x, y, *z, *args]
            '''
            }

        self.MULTI_SCT = """
varnames = ['x', 'y', 'z', '*args', '**kwargs']
test_names = [check_args(name).has_equal_part('name', 'bad%s'%name) for name in varnames]
Ex().check_function_def('my_fun').multi(test_names)
"""
        self.SCT_CHECK = "Ex().check_function_def('my_fun')"
        self.SCT_KW = "Ex().check_function_def('my_fun').check_args('x').has_equal_part('name', 'badx')"
        self.SCT_POS = "Ex().check_function_def('my_fun').check_args(0).has_equal_part('name', 'badx')"
        self.SCT_CHECK_ONE = "Ex().check_function_def('my_fun').check_args(1)"
        self.SCT_CHECK_Y = "Ex().check_function_def('my_fun').check_args('y')"
        self.SCT_CHECK_X = "Ex().check_function_def('my_fun').check_args('x')"
        self.SCT_CHECK_ARGS = "Ex().check_function_def('my_fun').check_args('*args')"
        self.SCT_CHECK_KWARGS = "Ex().check_function_def('my_fun').check_args('**kwargs')"

    def when_code_is_sol(self):
        self.data['DC_CODE'] = self.data['DC_SOLUTION']
        self.sct_payload = helper.run(self.data)
        return self.sct_payload['correct']

    def when_replace(self, orig, new):
        self.data['DC_CODE'] = self.data['DC_SOLUTION'].replace(orig, new)
        self.sct_payload = helper.run(self.data)
        return self.sct_payload['correct']

    def test_pass_kw(self):
        self.data['DC_SCT'] = self.SCT_KW
        self.assertTrue(self.when_code_is_sol())

    def test_fail_kw(self):
        self.data['DC_SCT'] = self.SCT_KW
        self.assertFalse(self.when_replace('x', 'x2'))

    def test_pass_pos(self):
        self.data['DC_SCT'] = self.SCT_POS
        self.assertTrue(self.when_code_is_sol())

    def test_fail_pos(self):
        self.data['DC_SCT'] = self.SCT_POS
        self.assertFalse(self.when_replace('x', 'x2'))

    def test_fail_pos_is_default(self):
        self.data['DC_SCT'] = self.SCT_CHECK_ONE + ".is_default()"
        self.assertFalse(self.when_replace('y = 4', 'y'))

    def test_fail_kw_is_default(self):
        self.data['DC_SCT'] = self.SCT_CHECK_Y + ".is_default()"
        self.assertFalse(self.when_replace('y = 4', 'y'))

    def test_fail_kw_not_default(self):
        self.data['DC_SCT'] = self.SCT_CHECK_X + ".is_default()"
        self.assertFalse(self.when_replace('x, y = 4', 'x = 2, y = 4'))

    def test_fail_star_args_undef(self):
        self.data['DC_CODE'] = """def my_fun(x, y = 4, z = ('a', 'b'), args=2, **kwargs): pass"""
        self.data['DC_SCT'] = self.SCT_CHECK_ARGS
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_fail_star_args_name(self):
        self.data['DC_CODE'] = """def my_fun(x, y = 4, z = ('a', 'b'), *wrongargsname, **kwargs): pass"""
        self.data['DC_SCT'] = self.SCT_CHECK_ARGS + '.has_equal_name()'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_fail_kwargs_undef(self):
        self.data['DC_CODE'] = """def my_fun(x, y = 4, z = ('a', 'b'), args=2, kwargs=2): pass"""
        self.data['DC_SCT'] = self.SCT_CHECK_KWARGS
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_fail_kwargs_name(self):
        self.data['DC_CODE'] = """def my_fun(x, y = 4, z = ('a', 'b'), *args, **wrongkwargsname): pass"""
        self.data['DC_SCT'] = self.SCT_CHECK_KWARGS + '.has_equal_name()'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_pass_equal_value(self):
        self.data['DC_SCT'] = self.SCT_CHECK_Y + ".has_equal_value('unequal values')"
        self.assertTrue(self.when_code_is_sol())

    def test_fail_equal_value(self):
        self.data['DC_SCT'] = self.SCT_CHECK_Y + ".has_equal_value('unequal values')"
        self.assertFalse(self.when_replace('y = 4', 'y = 2'))

    def test_pass_call_str(self):
        self.data['DC_SCT'] = self.SCT_CHECK + """.call("f(1, 2, (3,4), 5, kw_arg='ok')")"""
        self.assertTrue(self.when_replace('x', 'x2'))

    def test_pass_call_list(self):
        self.data['DC_SCT'] = self.SCT_CHECK + """.call([1, 2, (3,4), 5])"""
        self.assertTrue(self.when_replace('x', 'x2'))

    @unittest.skip("Tries to evaluate ast tree but gets None when no default")
    def test_check_value_when_no_default(self):
        self.data['DC_SCT'] = self.SCT_CHECK_X + ".has_equal_value('unequal values')"
        self.assertTrue(self.when_code_is_sol())

    def test_pass_multi(self):
        self.data['DC_SCT'] = self.MULTI_SCT
        self.assertTrue(self.when_code_is_sol())

    def test_fail_multi(self):
        self.data['DC_SCT'] = self.MULTI_SCT
        self.assertFalse(self.when_replace('x', 'x2'))


class TestLambdaFunctionSpec2(TestFunctionSpec2):
    def setUp(self):
        super().setUp()
        self.data['DC_SOLUTION'] = "lambda x, y = 4, z = ('a', 'b'), *args, **kwargs: [x, y, *z, *args]"
        for attr in ['MULTI_SCT', 'SCT_CHECK', 'SCT_KW', 'SCT_POS', 'SCT_CHECK_ONE', 'SCT_CHECK_Y', 'SCT_CHECK_X', 'SCT_CHECK_ARGS', 'SCT_CHECK_KWARGS']:
            lam_sct = getattr(self, attr).replace("check_function_def('my_fun')", 'check_lambda_function(0)')
            setattr(self, attr, lam_sct)

if __name__ == "__main__":
    unittest.main()

