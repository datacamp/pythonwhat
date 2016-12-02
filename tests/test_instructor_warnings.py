import unittest
import helper

class TestWarnings(unittest.TestCase):
    def test_converter_err(self):
        data = {
                "DC_SOLUTION": "d = dict()",
                "DC_SCT": """set_converter('builtins.dict', lambda: abc); test_object('d') """
                }
        data['DC_CODE'] = data['DC_SOLUTION']
        self.assertRaises(ValueError, lambda: helper.run(data))

    def test_check_syntax_double_getattr(self):
        data = {
                "DC_SOLUTION": "",
                "DC_CODE": "",
                "DC_SCT": """Ex().check_list_comp.check_body()"""
                }
        self.assertRaises(AttributeError, lambda: helper.run(data))

    def test_check_syntax_check_index_no_index(self):
        data = {
                "DC_SOLUTION": "[i for i in range(1)]",
                "DC_CODE": "[i for i in range(1)]",
                "DC_SCT": """Ex().check_list_comp()"""
                }
        self.assertRaises(TypeError, lambda: helper.run(data))

    def test_context_vals_wrong_place_in_chain(self):
        data = {"DC_SOLUTION": "[(i,j) for i,j in enumerate(range(10))]"}
        data["DC_CODE"] = data["DC_SOLUTION"]
        data["DC_SCT"] = """Ex().check_list_comp(0).set_context(i=1,j=2).check_iter()"""
        self.assertRaises(KeyError, lambda: helper.run(data))

if __name__ == "__main__":
    unittest.main()
