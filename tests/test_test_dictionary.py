import unittest
import helper

class TestDictionaryStepByStep(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = {'a': 123, 'b':456, 'c':789}",
            "DC_SCT": "test_dictionary('x')"
        }

    def test_dict_step1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Are you sure you defined", sct_payload['message'])

    def test_dict_step2(self):
        self.data["DC_CODE"] = "x = 123"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("<code>x</code> is not a dictionary", sct_payload['message'])

    def test_dict_step3(self):
        self.data["DC_CODE"] = "x = {'a':123, 'b':456, 'd':78}"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Have you specified a key <code>c</code> inside <code>x</code>?", sct_payload['message'])

    def test_dict_step4(self):
        self.data["DC_CODE"] = "x = {'a':123, 'b':456, 'c':78}"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Have you specified the correct value for the key <code>c</code> inside <code>x</code>?", sct_payload['message'])

    def test_dict_step5(self):
        self.data["DC_CODE"] = "x = {'a':123, 'b':456, 'c':789}"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestDictionaryStepByStepCustom(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = {'a': 123, 'b':456, 'c':789}",
            "DC_SCT": '''
test_dictionary('x',
                keys=['a', 'b'],
                undefined_msg='undefined',
                not_dictionary_msg='notdictionary',
                key_missing_msg='keymissing',
                incorrect_value_msg='incorrectvalue')
            '''
        }

    def test_dict_step1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'undefined')

    def test_dict_step2(self):
        self.data["DC_CODE"] = "x = 123"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'notdictionary')

    def test_dict_step3(self):
        self.data["DC_CODE"] = "x = {'a':123, 'c':56}"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'keymissing')

    def test_dict_step4(self):
        self.data["DC_CODE"] = "x = {'a':123, 'b':56}"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'incorrectvalue')

    def test_dict_step5(self):
        self.data["DC_CODE"] = "x = {'a':123, 'b':456, 'd':78}"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestDictionaryNonStringKeys(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "x = {'a': 123, 2:456}",
            "DC_SCT": "test_dictionary('x')"
        }

    def test_dict_step1(self):
        self.data["DC_CODE"] = "x = {'a': 123, 3:456}"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Have you specified a key <code>2</code> inside <code>x</code>?", sct_payload['message'])

    def test_dict_step2(self):
        self.data["DC_CODE"] = "x = {'a': 123, 2:45}"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Have you specified the correct value for the key <code>2</code> inside <code>x</code>?", sct_payload['message'])


class TestDictionaryIrregularities(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_CODE": "x = {'a': 123, 'b':456}",
            "DC_SCT": "test_dictionary('x', keys=['a','b'])"
        }

    def test_not_defined(self):
        self.data["DC_SOLUTION"] = ""
        self.assertRaises(NameError, helper.run, self.data)

    def test_not_dict(self):
        self.data["DC_SOLUTION"] = "x = 123"
        self.assertRaises(ValueError, helper.run, self.data)

    def test_not_key(self):
        self.data["DC_SOLUTION"] = "x = {'a': 123}"
        self.assertRaises(NameError, helper.run, self.data)

if __name__ == "__main__":
    unittest.main()
