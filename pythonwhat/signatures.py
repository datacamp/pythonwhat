import inspect
from inspect import Parameter as param
import pythonwhat
from pythonwhat.tasks import getSignatureFromObjInProcess

def sig_from_params(*args):
    return(inspect.Signature(list(args)))

def sig_from_obj(obj_char):
  return getSignatureFromObjInProcess(obj_char,
    pythonwhat.State.State.root_state.solution_process)

def get_manual_sigs():
    manual_sigs = {
        # builtins
        'abs': [param('x', param.POSITIONAL_ONLY)],
        'all': [param('iterable', param.POSITIONAL_ONLY)],
        'any': [param('iterable', param.POSITIONAL_ONLY)],
        'ascii': [param('obj', param.POSITIONAL_ONLY)],
        'bin': [param('number', param.POSITIONAL_ONLY)],
        'bool': [param('x', param.POSITIONAL_OR_KEYWORD)],
        'chr': [param('i', param.POSITIONAL_ONLY)],
        'callable': [param('obj', param.POSITIONAL_ONLY)],
        'classmethod': [param('function', param.POSITIONAL_ONLY)],
        'complex': [param('imag', param.POSITIONAL_OR_KEYWORD, default=0),
                    param('real', param.POSITIONAL_OR_KEYWORD, default=0)],
        'delattr': [param('obj', param.POSITIONAL_ONLY),
                    param('name', param.POSITIONAL_ONLY)],
        'dir': [param('object', param.POSITIONAL_OR_KEYWORD, default=None)],
        'divmod': [param('x', param.POSITIONAL_ONLY),
                   param('y', param.POSITIONAL_ONLY)],
        'enumerate': [param('iterable', param.POSITIONAL_ONLY),
                     param('start', param.POSITIONAL_OR_KEYWORD, default=0)],
        'float': [param('x', param.POSITIONAL_OR_KEYWORD)],
        'getattr': [param('object', param.POSITIONAL_ONLY),
                    param('name', param.POSITIONAL_ONLY),
                    param('default', param.POSITIONAL_ONLY, default=None)],
        'hasattr': [param('obj', param.POSITIONAL_ONLY),
                    param('name', param.POSITIONAL_ONLY)],
        'hash': [param('obj', param.POSITIONAL_ONLY)],
        'hex': [param('number', param.POSITIONAL_ONLY)],
        'id': [param('obj', param.POSITIONAL_ONLY)],
        'int': [param('x', param.POSITIONAL_OR_KEYWORD),
                param('base', param.POSITIONAL_OR_KEYWORD, default=10)],
        'isinstance': [param('obj', param.POSITIONAL_ONLY),
                       param('class_or_tuple', param.POSITIONAL_ONLY)],
        'issubclass': [param('cls', param.POSITIONAL_ONLY),
                       param('class_or_tuple', param.POSITIONAL_ONLY)],
        'list': [param('iterable', param.POSITIONAL_ONLY, default=None)],
        'len': [param('obj', param.POSITIONAL_ONLY)],
        'oct': [param('number', param.POSITIONAL_ONLY)],
        'open': [param('file', param.POSITIONAL_OR_KEYWORD),
                 param('mode', param.POSITIONAL_OR_KEYWORD, default='r'),
                 param('buffering', param.POSITIONAL_OR_KEYWORD, default=1),
                 param('encoding', param.POSITIONAL_OR_KEYWORD, default=None),
                 param('errors', param.POSITIONAL_OR_KEYWORD, default=None),
                 param('newline', param.POSITIONAL_OR_KEYWORD, default=None),
                 param('closefd', param.POSITIONAL_OR_KEYWORD, default=None),
                 param('opener', param.POSITIONAL_OR_KEYWORD, default=None)],
        'ord': [param('c', param.POSITIONAL_ONLY)],
        'pow': [param('x', param.POSITIONAL_ONLY),
                param('y', param.POSITIONAL_ONLY),
                param('z', param.POSITIONAL_ONLY, default=None)],
        'print': [param('value', param.POSITIONAL_ONLY)],
        'repr': [param('obj', param.POSITIONAL_ONLY)],
        'reversed': [param('sequence', param.POSITIONAL_ONLY)],
        'round': [param('number', param.POSITIONAL_OR_KEYWORD),
                  param('ndigits', param.POSITIONAL_OR_KEYWORD, default=0)],
        'set': [param('iterable', param.POSITIONAL_ONLY, default=None)],

        # Difference v3.4 vs v3.5!!!
        'setattr': [param('obj', param.POSITIONAL_ONLY),
                    param('name', param.POSITIONAL_ONLY),
                    param('value', param.POSITIONAL_ONLY)],
        'sorted': [param('iterable', param.POSITIONAL_ONLY),
                   param('key', param.POSITIONAL_OR_KEYWORD, default=None),
                   param('reverse', param.POSITIONAL_OR_KEYWORD, default=False)],
        'str': [param('object', param.POSITIONAL_OR_KEYWORD)],
        'sum': [param('iterable', param.POSITIONAL_ONLY),
                param('start', param.POSITIONAL_ONLY, default=0)],
        'tuple': [param('iterable', param.POSITIONAL_ONLY, default=None)],
        'type': [param('object', param.POSITIONAL_ONLY)],
        'vars': [param('object', param.POSITIONAL_ONLY)],

        # int

        # str
        'str.center': [param('width', param.POSITIONAL_ONLY),
                       param('fillchar', param.POSITIONAL_ONLY, default=" ")],

        # list
        'list.append': [param('object', param.POSITIONAL_ONLY)],
        'list.count': [param('value', param.POSITIONAL_ONLY)],

        # dict

        # numpy
        'numpy.array': [param('object', param.POSITIONAL_OR_KEYWORD),
                        param('dtype', param.POSITIONAL_OR_KEYWORD, default=None),
                        param('copy', param.POSITIONAL_OR_KEYWORD, default=True),
                        param('order', param.POSITIONAL_OR_KEYWORD, default=None),
                        param('subok', param.POSITIONAL_OR_KEYWORD, default=False),
                        param('ndmin', param.POSITIONAL_OR_KEYWORD, default=0)],
        'numpy.random.seed': [param('seed', param.POSITIONAL_OR_KEYWORD, default=None)],
        'numpy.random.rand': [param('d0', param.POSITIONAL_ONLY, default=None),
                              param('d1', param.POSITIONAL_ONLY, default=None),
                              param('d2', param.POSITIONAL_ONLY, default=None),
                              param('d3', param.POSITIONAL_ONLY, default=None),
                              param('d4', param.POSITIONAL_ONLY, default=None),
                              param('d5', param.POSITIONAL_ONLY, default=None),
                              param('d6', param.POSITIONAL_ONLY, default=None)],
        'numpy.random.randint': [param('low', param.POSITIONAL_OR_KEYWORD),
                                 param('high', param.POSITIONAL_OR_KEYWORD, default=None),
                                 param('size', param.POSITIONAL_OR_KEYWORD, default=None),
                                 param('dtype', param.POSITIONAL_OR_KEYWORD, default='l')],

        # others
        'math.radians': [param('x', param.POSITIONAL_ONLY)]
    }
    return(manual_sigs)
