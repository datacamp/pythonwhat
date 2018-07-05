import helper
import pytest
from pythonwhat.Test import TestFail as TF
from pythonwhat.local import setup_state

@pytest.mark.parametrize('stu, correct', [
    ('', False),
    ('import pandas', False),
    ('import pandas as x', False),
    ('import pandas as pd', True)
])
def test_basic(stu, correct):
    s = setup_state(stu_code = stu, sol_code = 'import pandas as pd')
    if correct:
        helper.passes(s.has_import('pandas'))
    else:
        with pytest.raises(TF):
            s.has_import('pandas')

@pytest.mark.parametrize('stu, same_as, correct', [
    ('', True, False),
    ('import pandas', True, False),
    ('import pandas as x', True, False),
    ('import pandas as pd', True, True),
    ('', False, False),
    ('import pandas', False, True),
    ('import pandas as x', False, True),
    ('import pandas as pd', False, True),
])
def test_same_as(stu, same_as, correct):
    s = setup_state(stu_code = stu, sol_code = 'import pandas as pd')
    if correct:
        helper.passes(s.has_import('pandas', same_as = same_as))
    else:
        with pytest.raises(TF):
            s.has_import('pandas', same_as = same_as)

@pytest.mark.parametrize('stu, correct', [
    ('', False),
    ('import numpy.random', False),
    ('import numpy.random as x', False),
    ('import numpy.random as rand', True)
])
def test_chaining(stu, correct):
    s = setup_state(stu_code = stu, sol_code = 'import numpy.random as rand')
    if correct:
        helper.passes(s.has_import('numpy.random'))
    else:
        with pytest.raises(TF):
            s.has_import('numpy.random')

def test_wrong_usage():
    s = setup_state(stu_code = '', sol_code = '')
    with pytest.raises(NameError):
        s.has_import('numpy')