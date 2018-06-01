import unittest
import helper
import pytest

class TestFChain(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''
[[ii+1 for ii in range(aa)] for aa in range(2)]

[[ii*2 for ii in range(bb)] for bb in range(1,3)]
'''
        }
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]

    def test_F(self):
        self.data["DC_SCT"]  =  '''
list_comp = F().check_list_comp(0).check_body().set_context(ii=2).has_equal_value('unequal')
Ex().check_list_comp(0).check_body().set_context(aa=2).multi(list_comp)
'''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_check_to_F(self):
        self.data["DC_SCT"] = '''
list_comp = check_list_comp(0).check_body().set_context(ii=2).has_equal_value('unequal')
Ex().check_list_comp(0).check_body().set_context(aa=2).multi(list_comp)
'''

    def test_check_to_F_nested(self):
        self.data["DC_SCT"] = '''
# funky, but we're testing nested check functions!
multi_test = multi(check_list_comp(0).check_body().set_context(aa=2).has_equal_value('badbody'))
Ex().multi(multi_test)
'''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_F_reused(self):
        self.data["DC_SCT"]  =  '''
list_comp = F().check_list_comp(0).check_body().set_context(ii=2).has_equal_value('unequal')

Ex().check_list_comp(0).check_body().set_context(aa=2).multi(list_comp)
Ex().check_list_comp(1).check_body().set_context(bb=4).multi(list_comp)
'''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_F_extends(self):
        self.data["DC_SCT"]  =  '''
list_comp = F().check_list_comp(0)
body_check = list_comp.check_body().set_context(aa=2).has_equal_value('unequal')

Ex().extend(body_check)\
        .check_list_comp(0).check_body().set_context(ii=2).has_equal_value('unequal')
'''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_F_assign_getattr(self):
        self.data["DC_SCT"]  =  '''
eq_test = F().check_list_comp(0).check_body().has_equal_value

Ex().multi(eq_test('unequal'))
'''

class TestSpecInterop(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''[aa+1 for aa in range(2)]'''
        }
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        self.FAIL_CODE = '''[aa for aa in range(2)]'''

    def test_spec1_in_multi_pass(self):
        self.data["DC_SCT"]  =  '''
te = test_expression_result(extra_env={'aa':2}, incorrect_msg='unequal')
Ex().multi(test_list_comp(body=te))                                                        # spec 1 inside multi
Ex().check_list_comp(0).check_body().multi(te)                                             # half of each spec
Ex().check_list_comp(0).check_body().set_context(aa=2).has_equal_value('unequal')          # full spec 2
test_list_comp(body=te)                                                                    # full spec 1
'''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_spec1_in_multi_fail(self):
        # TODO: this test fails because spec1 tests are run after spec2 tests,
        #       even if they come first in the SCT script, due to building the tree
        #       for spec1 tests but not spec2 (which are run immediately)
        self.data["DC_CODE"] = '''for aa in range(3): aa'''
        self.data["DC_SCT"] = '''
test_list_comp(body=test_expression_result(expr_code = 'aa', incorrect_msg='unequal'))
Ex().check_list_comp(0).check_body().multi(test_expression_result(incorrect_msg='unequal'))
Ex().check_list_comp(0).check_body().has_equal_value('unequal')

'''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_spec_run_order(self):
        self.data["DC_CODE"] = '''[aa for aa in range(2)]'''
        self.data["DC_SCT"]  =  '''
Ex().test_list_comp(body=test_expression_result(extra_env={'aa': 2}, incorrect_msg = 'spec1'))
Ex().check_list_comp(0).check_body().set_context(aa=2).has_equal_value('spec2')
'''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn('spec1', sct_payload['message'])

class TestMulti(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": '''[aa+1 for aa in range(2)]'''
        }
        self.data["DC_CODE"] = self.data["DC_SOLUTION"]
        self.FAIL_CODE = '''[aa for aa in range(2)]'''

    def test_nested_multi(self):
        self.data["DC_SCT"]  =  '''
test_body = F().check_body().set_context(aa=2).has_equal_value('wrong')
Ex().check_list_comp(0).multi(F().multi(test_body))
'''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_multi_splits_node_and_check(self):
        self.data["DC_SCT"]  =  '''
test_body = F().check_list_comp(0).check_body().set_context(aa=2).has_equal_value('wrong')
Ex().check_list_comp(0).multi(F().check_body().set_context(aa=2).has_equal_value('wrong'))
'''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_multi_generator(self):
        self.data["DC_SCT"] = """
Ex().check_list_comp(0).check_body()\
        .multi(set_context(aa=i).has_equal_value('wrong') for i in range(2))
"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

@pytest.mark.debug
class TestTestNot(unittest.TestCase):
    def setUp(self):
        self.data = {
                "DC_SOLUTION": "x = 1",
                "DC_CODE": "x = 1"
                }

    def test_pass(self):
        self.data["DC_SCT"] = """Ex().test_not(check_list_comp(0), msg="no")"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_pass2(self):
        self.data["DC_SCT"] = """Ex().test_not(test_student_typed("y"), msg = "don't type 'y'")"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_fail(self):
        # obviously this would be a terrible sct...
        self.data["DC_SCT"] = """Ex().test_not(test_object('x'), msg="no")"""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_fail2(self):
        # obviously this would be a terrible sct...
        self.data["DC_SCT"] = """Ex().test_not(test_student_typed("x"), msg="x is defined")"""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

class TestTestFail(unittest.TestCase):
    def setUp(self):
        self.data = {
                "DC_SOLUTION": "", "DC_CODE": ""
                }

    def test_fail(self):
        self.data["DC_SCT"] = """Ex().fail()"""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

class TestHasEqualAst(unittest.TestCase):
    def setUp(self):
        self.data = {
                "DC_SOLUTION": """dict(a = "a").keys()""",
                "DC_CODE":     """dict(a = 'a')    .keys()"""}

    def failing_submission(self):
        self.data["DC_CODE"] = "dict(A = 'a').keys(somearg = 2)"""
        sct_payload = helper.run(self.data, run_code=False)
        self.assertFalse(sct_payload['correct'])

    def test_simple_pass(self):
        self.data["DC_SCT"] = "Ex().has_equal_ast()"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_simple_fail(self):
        self.data["DC_SCT"] = "Ex().has_equal_ast()"
        self.failing_submission()

    def test_function_pass(self):
        self.data["DC_SCT"] = "Ex().check_function('dict', 0, signature=False).has_equal_ast()"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_function_fail(self):
        self.data["DC_SCT"] = "Ex().check_function('dict', 0, signature=False).has_equal_ast()"
        self.failing_submission()

    def test_function_code_pass(self):
        self.data["DC_SCT"] = """Ex().has_equal_ast(code = 'dict(a = "a").keys()')"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_function_code_fail(self):
        self.data["DC_SCT"] = """Ex().has_equal_ast(code = 'dict(a = "a").keys()')"""
        self.failing_submission()

    def test_exact_false_pass(self):
        self.data["DC_CODE"] = """dict(a = 'a').keys()\nprint('extra')"""
        self.data["DC_SCT"] = "Ex().has_equal_ast(exact=False)"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_exact_false_fail(self):
        self.data["DC_SCT"] = "Ex().has_equal_ast(exact=False)"
        self.failing_submission()

    def test_part_of_method_pass(self):
        self.data["DC_SCT"] = """Ex().has_equal_ast(code = 'dict(a = "a")', exact=False)"""
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_part_of_method_fail(self):
        self.data["DC_SCT"] = """Ex().has_equal_ast(code = 'dict(a = "a")', exact=False)"""
        self.failing_submission()

class TestOverride(unittest.TestCase):
    """
    This class is used to test overriding w/ correct and incorrect code. Tests are 
    run for entire nodes (e.g. an if block) and their parts (e.g. body of if block)
    """

    def do_exercise(self, code, base_check, parts, override=None, part_name = None, part_index = "", passes=True):
        """High level function used to generate tests"""
        if part_name:
            if not override: override = parts[part_name]
            sct = base_check + '.check_{}({}).override("""{}""").has_equal_ast()'\
                        .format(part_name, part_index, override)
        else:
            # whole code (e.g. if expression, or for loop)
            if not override: override = code.format(**parts)
            sct = base_check + '.override("""{}""").has_equal_ast()'.format(override)
        
        data = {
                "DC_SOLUTION": code.format(**parts),
                "DC_CODE": code.format(**parts),
                "DC_SCT": sct
            }
        sct_payload = helper.run(data)
        self.assertTrue(sct_payload['correct']) if passes else self.assertFalse(sct_payload['correct'])

    # used to generate tests
    EXPRESSIONS = {
            'if_exp': "{body} if {test} else {orelse}",
            'list_comp': "[{body} for i in {iter}]",
            'dict_comp': "{{ {key}: {value}  for i in {iter} }}",
            'for_loop': "for i in {iter}: {body}",
            'while': "while {test}: {body}",
            'try_except': "try: {body}\nexcept: pass\nelse: {orelse}",
            'lambda_function': "lambda a={args}: {body}",
            'function_def': ["'sum'", "def sum(a={args}): {body}"],
            'function': ["'sum', 0", "sum({args})"]
            }

    PARTS = {'body': "1", "test": "False", 'orelse': "2", 'iter': "range(3)", 
             'key': "3", 'value': "4", 'args': "(1,2,3)"}

import re
def gen_exercise(*args, **kwargs):
    return lambda self: TestOverride.do_exercise(self, *args, **kwargs)

for k, code in TestOverride.EXPRESSIONS.items():
    # base SCT, w/ special indexing if function checks
    if isinstance(code, list): indx, code = code
    else: indx = '0'
    base_check = "Ex().check_{}({})".format(k, indx)
    # pass overall test ----
    pf = gen_exercise(code, base_check, TestOverride.PARTS)
    setattr(TestOverride, 'test_{}_pass'.format(k), pf)
    # fail overall test ----
    pf = gen_exercise(code, base_check, TestOverride.PARTS, override="'WRONG ANSWER'", passes=False)
    setattr(TestOverride, 'test_{}_fail'.format(k), pf)
    # test individual pieces --------------------------------------------------
    for part in re.findall("\{([^{]*?)\}", code):    # find all str.format vars, e.g. {body}
        part_index = "" if part != 'args' else 0
        # pass individual piece ----
        test_name = 'test_{}_{}_pass'.format(k, part)
        pf = gen_exercise(code, base_check, TestOverride.PARTS, part_name=part, part_index=part_index)
        setattr(TestOverride, test_name, pf) 
        # fail individual piece ----
        test_name = 'test_{}_{}_fail'.format(k, part)
        bad_code = code.format(**{part: "[]", **TestOverride.PARTS})
        pf = gen_exercise(code, base_check, TestOverride.PARTS, part_name=part, part_index=part_index, override=bad_code, passes=False)
        setattr(TestOverride, test_name, pf) 


# Test SCT Ex syntax (copied from sqlwhat)  -----------------------------------

import pytest
from pythonwhat.check_syntax import Ex, F, state_dec

@pytest.fixture
def addx():
    return lambda x, state=None: state + x

@pytest.fixture
def f():
    return F._from_func(lambda state=None: state + 'b')

@pytest.fixture
def f2():
    return F._from_func(lambda state=None: state + 'c')

def test_f_from_func(f):
    assert f('a') == 'ab'

def test_f_sct_copy_kw(addx):
    assert F()._sct_copy(addx)(x = 'x')('state') == 'statex'

def test_f_sct_copy_pos(addx):
    assert F()._sct_copy(addx)('x')('state') == 'statex'

def test_ex_sct_copy_kw(addx):
    assert Ex('state')._sct_copy(addx)(x = 'x')._state == 'statex'

def test_ex_sct_copy_pos(addx):
    assert Ex('state')._sct_copy(addx)('x')._state == 'statex'

def test_f_2_funcs(f, addx):
    g = f._sct_copy(addx)
    
    assert g(x = 'x')('a') == 'abx'

def test_f_add_unary_func(f):
    g = f >> (lambda state=None: state + 'c')
    assert g('a') == 'abc'

def test_f_add_f(f, f2):
    g = f >> f2
    assert g('a') == 'abc'

def test_f_from_state_dec(addx):
    dec_addx = state_dec(addx)
    f = dec_addx(x = 'x')
    isinstance(f, F)
    assert f('state') == 'statex'

@pytest.fixture
def ex():
    return Ex('state')._sct_copy(lambda x, state=None: state + x)('x')

def test_ex_add_f(ex, f):
    (ex >> f)._state = 'statexb'

def test_ex_add_unary(ex):
    (ex >> (lambda state=None: state + 'b'))._state == 'statexb'

def test_ex_add_ex_err(ex):
    with pytest.raises(BaseException): ex >> ex

def test_f_add_ex_err(f, ex):
    with pytest.raises(BaseException): f >> ex


if __name__ == "__main__":
    unittest.main()
