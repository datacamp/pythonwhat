from pythonwhat.check_funcs import check_part, check_part_index, check_node
from pythonwhat import check_funcs
from pythonwhat.State import State
from pythonwhat.probe import Node
from functools import partial, wraps
import inspect

__PART_WRAPPERS__ = {
        'iter': 'iterable part',
        'body': 'body',
        'key' : 'key part',
        'value': 'value part',
        'orelse': 'else part',
        'vararg': '(changeme) vararg part',
        'kwarg':  '(changeme) kwarg part',
        'test': 'condition' 
        }

__PART_INDEX_WRAPPERS__ = {
        'ifs': 'if',
        'handlers': 'exception handler',
        'context': 'context'
        }

__NODE_WRAPPERS__ = {
        'list_comp': 'list comprehension',
        'generator_exp': 'generator expression',
        'dict_comp': 'dictionary comprehension',
        'for_call': 'for statement',
        'function_def': 'function definition',
        'if_exp_call': 'if expression',
        'if_call': 'if statement',
        'lambda_function': 'lambda function',
        'try_except': 'try statement',
        'while_call': 'while statement',
        'with': 'with statement'
        }

def state_dec(f):
    """Decorate check_* functions to return partial if no state passed"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        ba = inspect.signature(f).bind(*args, **kwargs)
        ba.apply_defaults()

        state_arg = ba.arguments.get('state')
        if isinstance(state_arg, State):        # proper state, run function
            return f(*args, **kwargs)
        elif state_arg is None:                 # default state arg, make partial
            return partial(f, *args, **kwargs)
        else:                                   # passed improper state arg
            raise BaseException("Did you use the right number of arguments in your SCT?")
    
    return wrapper

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

scts = {}

for k, v in __PART_WRAPPERS__.items():
    scts['check_'+k] = state_dec(partial(check_part, k, v))

for k, v in __PART_INDEX_WRAPPERS__.items(): 
    scts['check_'+k] = state_dec(partial(check_part_index, k, part_msg=v))


for k, v in __NODE_WRAPPERS__.items():
    scts['check_'+k] = state_dec(partial(check_node, k+'s', typestr=v))

for k in ['set_context', 'has_equal_value', 'extend']:
    scts[k] = state_dec(getattr(check_funcs, k))


scts['multi'] = multi_dec(state_dec(check_funcs.multi))
scts['with_context'] = multi_dec(state_dec(check_funcs.with_context))
