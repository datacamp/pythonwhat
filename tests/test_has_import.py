import pytest
import tests.helper as helper
from pythonwhat.test_exercise import setup_state


@pytest.mark.parametrize(
    "stu, correct",
    [
        ("", False),
        ("import numpy", False),
        ("import pandas", True),
        ("import pandas as x", True),
        ("import pandas as pd", True),
    ],
)
def test_basic(stu, correct):
    s = setup_state(stu_code=stu, sol_code="import pandas as pd")
    with helper.verify_sct(correct):
        s.has_import("pandas")


@pytest.mark.parametrize(
    "stu, same_as, correct",
    [
        ("", True, False),
        ("import numpy", True, False),
        ("import pandas", True, False),
        ("import pandas as x", True, False),
        ("import pandas as pd", True, True),
        ("", False, False),
        ("import numpy", False, False),
        ("import pandas", False, True),
        ("import pandas as x", False, True),
        ("import pandas as pd", False, True),
    ],
)
def test_same_as(stu, same_as, correct):
    s = setup_state(stu_code=stu, sol_code="import pandas as pd")
    with helper.verify_sct(correct):
        s.has_import("pandas", same_as=same_as)


@pytest.mark.parametrize(
    "stu, correct",
    [
        ("", False),
        ("import numpy.random", True),
        ("import numpy.random as x", True),
        ("import numpy.random as rand", True),
        ("from numpy import random as x", True),
        ("from numpy import random as rand", True),
    ],
)
def test_chaining(stu, correct):
    s = setup_state(stu_code=stu, sol_code="import numpy.random as rand")
    with helper.verify_sct(correct):
        s.has_import("numpy.random")
