from pythonwhat.check_wrappers import scts
from pythonwhat.State import State
from functools import partial
import copy

class Chain:
    def __init__(self, state):
        self._state = state
        self._crnt_sct = None

    def __getattr__(self, attr):
        if attr not in scts: raise AttributeError("No SCT named %s"%attr)
        else:
            # make a copy to return, 
            # in case someone does: a = chain.a; b = chain.b
            chain = copy.copy(self)
            chain._crnt_sct = scts[attr]
            return chain

    def __call__(self, *args, **kwargs):
        self._state = self._crnt_sct(state=self._state, *args, **kwargs)
        assert isinstance(self._state, State)
        return self
