from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import multi

from .test_or import test_or

def test_correct(check, diagnose, state=None):
    """Allows feedback from a diagnostic SCT, only if a check SCT fails. 
    
    """

    def diagnose_and_check(state=None):
        # use multi twice, since diagnose and check may be lists of tests
        multi(diagnose, state=state)
        multi(check, state=state)

    test_or(diagnose_and_check, check, state=state)
