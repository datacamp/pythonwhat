import unittest
import helper

class TestBuiltInSignatures(unittest.TestCase):

    # https://docs.python.org/3.x/library/functions.html
    #
    # Builtins that haven't been implemented/tested yet
    # filter(), format(), frozenset(), iter(), map(), max(), min(),
    # memoryview(), next(), property(), range(), slice(), super(), zip()

    def test_abs(self):
        helper.test_builtin(self, "abs", params="'x'", arguments="1")

    def test_all(self):
        helper.test_builtin(self, "all", params="'iterable'", arguments="[True, True]")

    def test_any(self):
        helper.test_builtin(self, "any", params="'iterable'", arguments="[True, False]")

    def test_ascii(self):
        helper.test_builtin(self, "ascii", params="'obj'", arguments="'test'")

    def test_bin(self):
        helper.test_builtin(self, "bin", params="'number'", arguments="123456")

    def test_bool(self):
        helper.test_builtin(self, "bool", params="'x'", arguments="1")

    def test_callable(self):
        helper.test_builtin(self, "callable", params="'obj'", arguments="round")

    def test_chr(self):
        helper.test_builtin(self, "chr", params="'i'", arguments="123")

    def test_classmethod(self):
        helper.test_builtin(self, "classmethod", params="'function'", arguments="str")

    def test_complex(self):
        helper.test_builtin(self, "complex", params="'real','imag'", arguments="1,2")

    def test_delattr(self):
        self.data = {
            "DC_PEC": '''
class Test():
    def __init__(self, a):
        self.a = a
    def set_a(self, value):
        self.a = value
x = Test(123)
            ''',
            "DC_SOLUTION": "x = delattr(x,'a')",
            "DC_CODE": "x = delattr(x,'a')",
            "DC_SCT": "test_function_v2('delattr', params=['obj','name'], do_eval=False)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_dir(self):
        helper.test_builtin(self, "dir", params="'object'", arguments="[1,2,3]")

    def test_divmod(self):
        helper.test_builtin(self, "divmod", params="'x','y'", arguments="7,3")

    def test_enumerate(self):
        helper.test_builtin(self, "enumerate", params="'iterable','start'", arguments="[1,2,3],1")

    def test_float(self):
        helper.test_builtin(self, "float", params="'x'", arguments="123")

    def test_getattr(self):
        self.data = {
            "DC_PEC": '''
class Test():
    def __init__(self, a):
        self.a = a
    def set_a(self, value):
        self.a = value
x = Test(123)
            ''',
            "DC_SOLUTION": "x = getattr(x,'a')",
            "DC_CODE": "x = getattr(x,'a')",
            "DC_SCT": "test_function_v2('getattr', params=['object','name'], do_eval=False)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_hasattr(self):
        self.data = {
            "DC_PEC": '''
class Test():
    def __init__(self, a):
        self.a = a
    def set_a(self, value):
        self.a = value
x = Test(123)
            ''',
            "DC_SOLUTION": "x = hasattr(x,'a')",
            "DC_CODE": "x = hasattr(x,'a')",
            "DC_SCT": "test_function_v2('hasattr', params=['obj','name'], do_eval=False)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_hash(self):
        helper.test_builtin(self, "hash", params="'obj'", arguments="123")

    def test_hex(self):
        helper.test_builtin(self, "hex", params="'number'", arguments="123")

    def test_id(self):
        helper.test_builtin(self, "id", params="'obj'", arguments="123")

    def test_int(self):
        helper.test_builtin(self, "int", params="'x','base'", arguments="'1001',2")

    def test_isinstance(self):
        helper.test_builtin(self, "isinstance", params="'obj','class_or_tuple'", arguments="[1,2,3],list")

    def test_issubclass(self):
        helper.test_builtin(self, "issubclass", params="'cls','class_or_tuple'", arguments="list,str")

    def test_len(self):
        helper.test_builtin(self, "len", params="'obj'", arguments="[1,2,3]")

    def test_list(self):
        helper.test_builtin(self, "list", params="", arguments="")
        helper.test_builtin(self, "list", params="'iterable'", arguments="[1,2,3,4]")

    def test_oct(self):
        helper.test_builtin(self, "oct", params="'number'", arguments="12345")

    def test_ord(self):
        helper.test_builtin(self, "ord", params="'c'", arguments="'a'")

    def test_pow(self):
        helper.test_builtin(self, "pow", params="'x','y'", arguments="3,3")
        helper.test_builtin(self, "pow", params="'x','y','z'", arguments="3,3,5")

    def test_print(self):
        helper.test_builtin(self, "print", params="'value'", arguments="123")

    def test_repr(self):
        helper.test_builtin(self, "repr", params="'obj'", arguments="[1,2,3]")

    def test_reversed(self):
        helper.test_builtin(self, "reversed", params = "'sequence'", arguments="[1,2,3]")

    def test_round(self):
        helper.test_builtin(self, "round", params = "'number','ndigits'", arguments="2.123123, 2")

    def test_set(self):
        helper.test_builtin(self, "set", params="", arguments="")
        helper.test_builtin(self, "set", params="'iterable'", arguments="[1,2,3,4]")

    def test_setattr(self):
        self.data = {
            "DC_PEC": '''
class Test():
    def __init__(self, a):
        self.a = a
    def set_a(self, value):
        self.a = value
x = Test(123)
            ''',
            "DC_SOLUTION": "setattr(x,'a',4)",
            "DC_CODE": "setattr(x,'a',4)",
            "DC_SCT": "test_function_v2('setattr', params=['obj','name','value'], do_eval=False)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_sorted(self):
        helper.test_builtin(self, "sorted", params = "'iterable'", arguments="[4,3,2,1]")

    def test_str(self):
        helper.test_builtin(self, "str", params = "'object'", arguments="123")

    def test_sum(self):
        helper.test_builtin(self, "sum", params = "'iterable','start'", arguments="[4,3,2,1],3")

    def test_tuple(self):
        helper.test_builtin(self, "tuple", params="", arguments="")
        helper.test_builtin(self, "tuple", params="'iterable'", arguments="[1,2,3,4]")

    def test_type(self):
        helper.test_builtin(self, "type", params = "'object'", arguments="[1,2,3,4]")

    def test_vars(self):
        self.data = {
            "DC_PEC": '''
class Test():
    def __init__(self, a):
        self.a = a
    def set_a(self, value):
        self.a = value
x = Test(123)
            ''',
            "DC_SOLUTION": "vars(x)",
            "DC_CODE": "vars(x)",
            "DC_SCT": "test_function_v2('vars', params=['object'], do_eval=False)"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestBuiltInMethodsInt(unittest.TestCase):
    pass

class TestBuiltInMethodsStr(unittest.TestCase):
    def test_center(self):
        self.data = {
            "DC_PEC": "x = 'test'",
            "DC_SOLUTION": "x.center(10, 's')",
            "DC_CODE": "x.center(10, 's')",
            "DC_SCT": "test_function_v2('x.center', params=['width','fillchar'])"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestBuiltInMethodsList(unittest.TestCase):
    def test_append(self):
        self.data = {
            "DC_PEC": "x = [1,2,3,4]",
            "DC_SOLUTION": "x.append(2)",
            "DC_CODE": "x.append(2)",
            "DC_SCT": "test_function_v2('x.append', params=['object'])"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_count(self):
        self.data = {
            "DC_PEC": "x = [1,2,3,4]",
            "DC_SOLUTION": "x.count(2)",
            "DC_CODE": "x.count(2)",
            "DC_SCT": "test_function_v2('x.count', params=['value'])"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestBuiltInMethodsDict(unittest.TestCase):
    pass

class TestBuiltInMethodsNumpy(unittest.TestCase):
    def test_array(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "x = np.array([1,2,3,4])",
            "DC_CODE": "x = np.array([1,2,3,4])",
            "DC_SCT": "test_function_v2('numpy.array', params=['object'])"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_array_spec2(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "x = np.array([1,2,3,4])",
            "DC_CODE": "x = np.array([1,2,3,4])",
            "DC_SCT": "Ex().check_function('numpy.array', 0).check_args('object')"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_random_seed(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "np.random.seed(123)",
            "DC_CODE": "np.random.seed(123)",
            "DC_SCT": "test_function_v2('numpy.random.seed', params=['seed'])"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_random_rand(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "np.random.rand(3,3,3)",
            "DC_CODE": "np.random.rand(3,3,3)",
            "DC_SCT": "test_function_v2('numpy.random.rand', params=['d0', 'd1', 'd2'])"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_random_randint(self):
        self.data = {
            "DC_PEC": "import numpy as np",
            "DC_SOLUTION": "np.random.randint(0, 5, size = (2,2))",
            "DC_CODE": "np.random.randint(0, 5, size = (2,2))",
            "DC_SCT": "test_function_v2('numpy.random.randint', params=['low', 'high', 'size'])"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestBuiltInMethodsOthers(unittest.TestCase):
    def test_radians(self):
        self.data = {
            "DC_PEC": "import math as m",
            "DC_SOLUTION": "x = m.radians(100)",
            "DC_CODE": "x = m.radians(100)",
            "DC_SCT": "test_function_v2('math.radians', params=['x'])"}
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

if __name__ == "__main__":
    unittest.main()
