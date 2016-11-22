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
        #'vararg': 'vararg part',
        #'kwarg':  ' kwarg part',
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
        'for_loop': 'for statement',
        'function_def': 'function definition',
        'if_exp': 'if expression',
        'if': 'if statement',
        'lambda_function': 'lambda function',
        'try_except': 'try statement',
        'while': '`while` loop',
        'with': '`with` statement'
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
          'check_arg',
          'has_equal_part']:
    scts[k] = getattr(check_funcs, k)

