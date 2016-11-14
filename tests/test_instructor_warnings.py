import unittest
import helper

class TestWarnings(unittest.TestCase):
    def test_converter_err(self):
        data = {
                "DC_SOLUTION": "d = dict()",
                "DC_SCT": """set_converter('builtins.dict', lambda: abc); test_object('d') """
                }
        data['DC_CODE'] = data['DC_SOLUTION']
        self.assertRaises(NameError, lambda: helper.run(data))

if __name__ == "__main__":
    unittest.main()
