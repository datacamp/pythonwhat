import unittest
import helper

class TestStudentTypedComment(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '# Just testing division\nprint(5 / 8)\n# Addition works too\nprint(7 + 10)',
            "DC_SOLUTION": ''
        }

    def test_success(self):
        self.data["DC_SCT"] = '''
test_student_typed("# (A|a)ddition works to(o?)\sprint\(7", not_typed_msg = "Make sure to add the instructed comment before `print(7+10)`.")
success_msg("You typed the correct comment.")
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "You typed the correct comment.")

class TestStudentDidntTypeComment(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '# Just testing division\nprint(5 / 8)\nprint(7 + 10)',
            "DC_SOLUTION": ''
        }

    def test_fail(self):
        self.data["DC_SCT"] = '''
test_student_typed("# (A|a)ddition works to(o?)\sprint\(7", not_typed_msg = "Make sure to add the instructed comment before `print(7+10)`.")
success_msg("You typed the correct comment.")
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Make sure to add the instructed comment before <code>print(7+10)</code>.")

class TestWikiExample(unittest.TestCase):

    def test_wikiexample1(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": 's = sum(range(10))\nprint(s)',
            "DC_SCT": 'test_student_typed("sum(range(", pattern = False)',
            "DC_CODE": 's = sum(range(10))\nprint(s)'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_wikiexample2(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": 's = sum(range(10))\nprint(s)',
            "DC_SCT": 'test_student_typed("sum\s*\(\s*range\s*\(")',
            "DC_CODE": 's = sum(range(10))\nprint(s)'
        }
        sct_payload = helper.run(self.data)
        print(sct_payload)
        self.assertTrue(sct_payload['correct'])

    def test_wikiexample1(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": 's = sum(range(10))\nprint(s)',
            "DC_SCT": 'test_student_typed("sum\s+\(\s*range\s*\(")',
            "DC_CODE": 's = sum(range(10))\nprint(s)'
        }
        sct_payload = helper.run(self.data)
        print(sct_payload)
        self.assertFalse(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()