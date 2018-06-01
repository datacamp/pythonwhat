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
        self.data["DC_SCT"] = 'test_student_typed(r"# (A|a)ddition works to(o?)\sprint\(7")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_success_new(self):
        self.data["DC_SCT"] = 'Ex().has_code(r"# (A|a)ddition works to(o?)\sprint\(7")'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestStudentDidntTypeComment(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '',
            "DC_CODE": '# Just testing division\nprint(5 / 8)\nprint(7 + 10)',
            "DC_SOLUTION": ''
        }

    def test_fail(self):
        self.data["DC_SCT"] = 'test_student_typed(r"# (A|a)ddition works to(o?)\sprint\(7", not_typed_msg = "Wrong.")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Wrong.")

    def test_fail_new(self):
        self.data["DC_SCT"] = 'Ex().has_code(r"# (A|a)ddition works to(o?)\sprint\(7", not_typed_msg = "Wrong.")'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Wrong.")

class TestWikiExample(unittest.TestCase):

    def test_wikiexample1(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": 's = sum(range(10))\nprint(s)',
            "DC_SCT": 'Ex().has_code(r"sum(range(", pattern = False)',
            "DC_CODE": 's = sum(range(10))\nprint(s)'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_wikiexample2(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": 's = sum(range(10))\nprint(s)',
            "DC_SCT": 'Ex().has_code(r"sum\s*\(\s*range\s*\(")',
            "DC_CODE": 's = sum(range(10))\nprint(s)'
        }
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_wikiexample1(self):
        self.data = {
            "DC_PEC": '',
            "DC_SOLUTION": 's = sum(range(10))\nprint(s)',
            "DC_SCT": 'Ex().has_code(r"sum\s+\(\s*range\s*\(")',
            "DC_CODE": 's = sum(range(10))\nprint(s)'
        }
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()