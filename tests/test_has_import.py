import unittest
import helper

class TestImportingStepByStep(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "import pandas as pd",
            "DC_SCT": "test_import('pandas')"
        }

    def test_step_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Did you import <code>pandas</code>?")

    def test_step_2(self):
        self.data["DC_CODE"] = "import pandas as panda"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Did you set the correct alias for <code>pandas</code>?")

    def test_step_3(self):
        self.data["DC_CODE"] = "import pandas as pd"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    # if same_as = False, alias does not matter
    def test_step_x(self):
        self.data["DC_SCT"] = "test_import('pandas', same_as = False)"
        self.data["DC_CODE"] = "import pandas as panda"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestImportingStepByStep(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "import pandas as pd",
            "DC_SCT": "Ex().has_import('pandas')"
        }

    def test_step_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Did you import <code>pandas</code>?")

    def test_step_2(self):
        self.data["DC_CODE"] = "import pandas as panda"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Did you set the correct alias for <code>pandas</code>?")

    def test_step_3(self):
        self.data["DC_CODE"] = "import pandas as pd"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    # if same_as = False, alias does not matter
    def test_step_x(self):
        self.data["DC_SCT"] = "test_import('pandas', same_as = False)"
        self.data["DC_CODE"] = "import pandas as panda"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestImportingStepByStepCustom(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "import pandas as pd",
            "DC_SCT": "test_import('pandas', not_imported_msg = 'notimported', incorrect_as_msg = 'incorrectalias')"
        }

    def test_step_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "notimported")

    def test_step_2(self):
        self.data["DC_CODE"] = "import pandas as panda"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "incorrectalias")

if __name__ == "__main__":
    unittest.main()
