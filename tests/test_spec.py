import unittest
import helper

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

    def test_fail(self):
        # obviously this would be a terrible sct...
        self.data["DC_SCT"] = """Ex().test_not(test_object('x'), msg="no")"""
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


#class TestSetContext(unittest.TestCase):
#    def setUp(self):
#        self.data = {
#                "DC_PEC": "",
#                "DC_SOLUTION": "[(i,j) for i,j in enumerate(range(10))]"
#                }

if __name__ == "__main__":
    unittest.main()
