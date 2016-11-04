from pythonwhat.check_wrappers import scts
from pythonwhat.State import State
from functools import partial, reduce, wraps
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

class F(Chain):
    def __init__(self, stack = None):
        self._crnt_sct = None
        self._stack = [] if stack is None else stack

    def __call__(self, *args, **kwargs):
        if not self._crnt_sct:
            state = kwargs.get('state') or args[0]
            return reduce(lambda s, f: f(state=s), self._stack, state)
        else:
            pf = self._crnt_sct(*args, **kwargs)
            return self.__class__(self._stack + [pf])

def Ex():
    return Chain(State.root_state)
