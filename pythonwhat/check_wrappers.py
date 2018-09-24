from pythonwhat.check_funcs import check_part, check_part_index, check_node
from pythonwhat.has_funcs import has_equal_part
from pythonwhat import check_funcs, has_funcs, check_logic, check_object
from pythonwhat.check_function import check_function
from pythonwhat.check_has_context import has_context

from functools import partial
import inspect

__PART_WRAPPERS__ = {
    'iter': 'iterable part',
    'body': 'body',
    'key' : 'key part',
    'value': 'value part',
    'orelse': 'else part',
    'finalbody': 'finally part',
    'test': 'condition',
}

__PART_INDEX_WRAPPERS__ = {
    'ifs': '{{ordinal}} if',
    'bases': '{{ordinal}} base class',
    'handlers': '`{{index}}` `except` block',
    'context': '{{ordinal}} context',
}

__NODE_WRAPPERS__ = {
    'list_comp': '{{ordinal}} list comprehension',
    'generator_exp': '{{ordinal}} generator expression',
    'dict_comp': '{{ordinal}} dictionary comprehension',
    'for_loop': '{{ordinal}} for loop',
    'function_def': 'definition of `{{index}}()`',
    'class_def': 'class definition of `{{index}}`',
    'if_exp': '{{ordinal}} if expression',
    'if_else': '{{ordinal}} if statement',
    'lambda_function': '{{ordinal}} lambda function',
    'try_except': '{{ordinal}} try statement',
    'while': '{{ordinal}} `while` loop',
    'with': '{{ordinal}} `with` statement',
}

scts = {}

# make has_equal_part wrappers

scts['has_equal_name'] = partial(has_equal_part, 'name', msg='Make sure to use the correct {{name}}, was expecting {{sol_part[name]}}, instead got {{stu_part[name]}}.')
scts['is_default'] = partial(has_equal_part, 'is_default', msg="Make sure it {{ 'has' if sol_part.is_default else 'does not have'}} a default argument.")

# include rest of wrappers
for k, v in __PART_WRAPPERS__.items():
    scts['check_'+k] = partial(check_part, k, v)

for k, v in __PART_INDEX_WRAPPERS__.items(): 
    scts['check_'+k] = partial(check_part_index, k, part_msg=v)

for k, v in __NODE_WRAPPERS__.items():
    scts['check_'+k] = partial(check_node, k+'s', typestr=v)

for k in ['set_context', 'set_env', 'disable_highlighting', 'check_not', 'check_or', 'check_correct', 'fail', 'override', 'multi']:
    scts[k] = getattr(check_logic, k)

for k in ['with_context', 'check_args', 'check_call']:
    scts[k] = getattr(check_funcs, k)

for k in ['has_equal_value', 'has_equal_output', 'has_equal_error', 'has_equal_ast', 'has_equal_part_len',
          'has_equal_part', 'has_import', 'has_output', 'has_printout', 'has_code', 'has_no_error', 'has_chosen']:
    scts[k] = getattr(has_funcs, k)

# include check_object and friends ------
for k in ['check_object', 'is_instance', 'check_df', 'check_keys']:
    scts[k] = getattr(check_object, k)

scts['has_context'] = has_context
scts['check_function'] = check_function