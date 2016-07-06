import unittest
from pythonwhat import utils

class TestUtils(unittest.TestCase):

	def test_get_ord(self):
		self.assertEqual(utils.get_ord(1), "first")
		self.assertEqual(utils.get_ord(2), "second")
		self.assertEqual(utils.get_ord(3), "third")
		self.assertEqual(utils.get_ord(11), "11th")

	def test_get_times(self):
		self.assertEqual(utils.get_times(1), "once")
		self.assertEqual(utils.get_times(2), "twice")
		self.assertEqual(utils.get_times(3), "3 times")
		self.assertEqual(utils.get_times(11), "11 times")

if __name__ == "__main__":
    unittest.main()
