import unittest
import os.path
import sys

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover("."))
