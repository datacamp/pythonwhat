from protowhat.sct_syntax import EagerChain, ExGen, LazyChainStart, state_dec_gen, LazyChain
from pythonwhat.checks.check_wrappers import scts
from pythonwhat.State import State

# TODO: could define scts for check_wrappers at the module level
sct_dict = scts.copy()

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


# Prepare check_funcs to be used alone (e.g. test = check_with().check_body())
v2_check_functions = {k: state_dec(v) for k, v in scts.items()}
