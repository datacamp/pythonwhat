from pythonwhat.check_wrappers import scts
from pythonwhat.State import State
from pythonwhat.probe import Node
from functools import partial, reduce, wraps
import inspect
import copy

def multi_dec(f):
    """Decorator for multi to remove nodes for original test functions from root node"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        args = args[0] if len(args) == 1 and isinstance(args[0], (list, tuple)) else args
        for arg in args:
            if isinstance(arg, Node) and arg.parent.name is 'root':
                arg.parent.remove_child(arg)
                arg.update_child_calls()
        return f(*args, **kwargs)
    return wrapper


def state_dec(f):
    """Decorate check_* functions to return F chain if no state passed"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        ba = inspect.signature(f).bind(*args, **kwargs)
        ba.apply_defaults()

        state_arg = ba.arguments.get('state')
        if isinstance(state_arg, State):        # proper state, run function
            return f(*args, **kwargs)
        elif state_arg is None:                 # default state arg, make partial
            return F._from_func(partial(f, *args, **kwargs))
        else:                                   # passed improper state arg
            raise BaseException("Did you use the right number of arguments in your SCT?")
    
    return wrapper

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
            pf = partial(self._crnt_sct, *args, **kwargs)
            return self.__class__(self._stack + [pf])
    
    @classmethod
    def _from_func(cls, f):
        func_chain = cls()
        func_chain._stack.append(f)
        return func_chain

def Ex():
    return Chain(State.root_state)

# Prepare scts ----------------------
for k in ['multi', 'with_context']:
    scts[k] = multi_dec(scts[k])

spec_2_context = {k : state_dec(v) for k, v in scts.items()}
