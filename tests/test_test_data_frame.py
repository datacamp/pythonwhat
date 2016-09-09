import unittest
import helper

class TestExercise1(unittest.TestCase):
    def setUp(self):
        self.data = {
          "DC_PEC": '''
import pandas as pd
          ''',
          "DC_SCT": '''
test_data_frame('df')
          ''',
          "DC_SOLUTION": '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
})
    '''
        }

    def test_Pass1(self):
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass2(self):
        self.data["DC_SCT"] = "test_data_frame('df', columns=['b','c'])"
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 5],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass3(self):
        self.data["DC_SCT"] = "test_data_frame('df', columns=['a','c'])"
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'r', 'z'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

    def test_Pass4(self):
        self.data["DC_SCT"] = "test_data_frame('df', columns=['a','b'])"
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, True, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


    def test_Fail1(self):
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 2],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Column <code>a</code> of your pandas DataFrame, <code>df</code>, is not correct.')

    def test_Fail2(self):
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'r'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Column <code>b</code> of your pandas DataFrame, <code>df</code>, is not correct.')

    def test_Fail3(self):
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, False]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Column <code>c</code> of your pandas DataFrame, <code>df</code>, is not correct.')

    def test_Fail4(self):
        self.data["DC_CODE"] = '''
not_df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'Are you sure you defined the pandas DataFrame: <code>df</code>?')

    def test_Fail5(self):
        self.data["DC_CODE"] = '''
df = {
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
}
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], '<code>df</code> is not a pandas DataFrame.')


    def test_Fail6(self):
        self.data["DC_SCT"] = "test_data_frame('df', incorrect_msg='test 1')"
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 2],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'test 1')

    def test_Fail7(self):
        self.data["DC_SCT"] = "test_data_frame('df', undefined_msg='test 2')"
        self.data["DC_CODE"] = '''
not_df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'test 2')

    def test_Fail8(self):
        self.data["DC_SCT"] = "test_data_frame('df', not_data_frame_msg='test 3')"
        self.data["DC_CODE"] = '''
df = {
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
}
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'test 3')

    def test_Fail9(self):
        self.data["DC_SCT"] = "test_data_frame('df', columns=['d'])"
        self.data["DC_SOLUTION"] = '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True],
    'd': [1.2, 1.3, 1.4]
})
        '''
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'There is no column <code>d</code> inside <code>df</code>.')

    def test_Fail10(self):
        self.data["DC_SCT"] = "test_data_frame('df', columns=['d'], undefined_cols_msg='test 4')"
        self.data["DC_SOLUTION"] = '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True],
    'd': [1.2, 1.3, 1.4]
})
        '''
        self.data["DC_CODE"] = '''
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z'],
    'c': [True, False, True]
})
        '''
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], 'test 4')

if __name__ == "__main__":
    unittest.main()
