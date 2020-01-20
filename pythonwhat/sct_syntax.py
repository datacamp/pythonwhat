from protowhat.sct_syntax import EagerChain, ExGen, LazyChainStart, state_dec_gen, LazyChain
from pythonwhat.checks.check_wrappers import scts
from pythonwhat.State import State
from pythonwhat.probe import Node, Probe, TEST_NAMES
from pythonwhat.utils import include_v1
from pythonwhat import test_funcs
from functools import wraps

# TODO: could define scts for check_wrappers at the module level
sct_dict = scts.copy()


def multi_dec(f):
    """Decorator for multi to remove nodes for original test functions from root node"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        args = (
            args[0] if len(args) == 1 and isinstance(args[0], (list, tuple)) else args
        )
        for arg in args:
            if isinstance(arg, Node) and arg.parent.name is "root":
                arg.parent.remove_child(arg)
                arg.update_child_calls()
        return f(*args, **kwargs)

    return wrapper


state_dec = state_dec_gen(sct_dict)

# todo: __all__?
assert ExGen
assert LazyChainStart


def Ex(state=None):
    return EagerChain(state=state or State.root_state, chainable_functions=sct_dict)


def F():
    return LazyChain(chainable_functions=sct_dict)


def get_chains():
    return {
        "Ex": ExGen(sct_dict, State.root_state),
        "F": LazyChainStart(sct_dict),
    }


if include_v1():
    # Prepare SCTs that may be chained attributes ----------------------
    # decorate functions that may try to run test_* function nodes as subtests
    # so they remove those nodes from the tree
    for k in ["multi", "with_context"]:
        sct_dict[k] = multi_dec(sct_dict[k])

    # allow test_* functions as chained attributes
    for k in TEST_NAMES:
        sct_dict[k] = Probe(tree=None, f=getattr(test_funcs, k), eval_on_call=True)

    # original logical test_* functions behave like multi
    # this is necessary to allow them to take check_* funcs as args
    # since probe behavior will try to call all SCTs passed (assuming they're also probes)
    for k in ["test_or", "test_correct"]:
        sct_dict[k] = multi_dec(getattr(test_funcs, k))

# Prepare check_funcs to be used alone (e.g. test = check_with().check_body())
v2_check_functions = {k: state_dec(v) for k, v in scts.items()}
