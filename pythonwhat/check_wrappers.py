from pythonwhat.check_funcs import check_part, check_part_index, check_node
from pythonwhat import check_funcs
from functools import partial
import inspect

__PART_WRAPPERS__ = {
        'iter': 'iterable part',
        'body': 'body',
        'key' : 'key part',
        'value': 'value part',
        'orelse': 'else part',
        'test': 'condition' 
        }

__PART_INDEX_WRAPPERS__ = {
        'ifs': '{ordinal} if',
        'handlers': '{index} `except` block',
        'context': 'context'
        }

__NODE_WRAPPERS__ = {
        'list_comp': '{ordinal} list comprehension',
        'generator_exp': '{ordinal} generator expression',
        'dict_comp': '{ordinal} dictionary comprehension',
        'for_loop': '{ordinal} for statement',
        'function_def': 'definition of `{index}()`',
        'if_exp': '{ordinal} if expression',
        'if': '{ordinal} if statement',
        'lambda_function': '{ordinal} lambda function',
        'try_except': '{ordinal} try statement',
        'while': '{ordinal} `while` loop',
        'with': '{ordinal} `with` statement'
        }

scts = {}

for k, v in __PART_WRAPPERS__.items():
    scts['check_'+k] = partial(check_part, k, v)

for k, v in __PART_INDEX_WRAPPERS__.items(): 
    scts['check_'+k] = partial(check_part_index, k, part_msg=v)


for k, v in __NODE_WRAPPERS__.items():
    scts['check_'+k] = partial(check_node, k+'s', typestr=v)

for k in ['set_context', 
          'has_equal_value', 'has_equal_output', 'has_equal_error', 'call',
          'extend', 'multi',
          'with_context',
          'check_args',
          'has_equal_part']:
    scts[k] = getattr(check_funcs, k)

