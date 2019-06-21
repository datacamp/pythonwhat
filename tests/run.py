import os
import sys
import pytest

os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
sys.setrecursionlimit(5000)
pytest.main()
