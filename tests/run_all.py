import unittest
import os.path
import sys

if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover("."))
