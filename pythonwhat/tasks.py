#import dill
#from .output import NoOutput, CaptureExecOutput, OutputManager
from . import utils
import os
import dill
import pythonwhat
import ast
import inspect
import copy
from pythonwhat.utils_env import set_context_vals
from contextlib import contextmanager
import random, string

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

### TASKS

class TaskIsDefined(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        return self.name in shell.user_ns

class TaskIsInstance(object):
    def __init__(self, name, klass):
        self.name = name
        self.klass = klass

    def __call__(self, shell):
        return isinstance(shell.user_ns[self.name], self.klass)

class TaskGetKeys(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        try:
            return list(shell.user_ns[self.name].keys())
        except:
            return None

class TaskGetColumns(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        try:
            return list(shell.user_ns[self.name].columns)
        except:
            return None

class TaskHasKey(object):
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __call__(self, shell):
        return self.key in shell.user_ns[self.name]


class TaskGetValue(object):
    def __init__(self, name, key, tempname):
        self.name = name
        self.key = key
        self.tempname = tempname

    def __call__(self, shell):
        try:
            shell.user_ns[self.tempname] = shell.user_ns[self.name][self.key]
            return True
        except:
            return None

class TaskGetStream(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        try:
            return dill.dumps(shell.user_ns[self.name])
        except:
            return None

class TaskGetClass(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        obj = shell.user_ns[self.name]

        if hasattr(obj, '__module__'):
            typestr = obj.__module__ + "."
        else:
            typestr = ""
        return typestr + obj.__class__.__name__

class TaskConvert(object):
    def __init__(self, name, converter):
        self.name = name
        self.converter = converter

    def __call__(self, shell):
        return dill.loads(self.converter)(shell.user_ns[self.name])

class TaskEvalAst(object):
    def __init__(self, tree, name):
        self.tree = tree
        self.name = name

    def __call__(self, shell):
        try:
            shell.user_ns[self.name] = eval(compile(ast.Expression(self.tree), "<script>", "eval"), shell.user_ns)
            return True
        except:
            return None

class TaskGetSignature(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            return get_signature(name = self.name,
                                 mapped_name = self.mapped_name,
                                 signature = self.signature,
                                 manual_sigs = self.manual_sigs,
                                 env = shell.user_ns)
        except:
            return None

class TaskGetSignatureFromObj(object):
    def __init__(self, obj_char):
        self.obj_char = obj_char

    def __call__(self, shell):
        try:
            return inspect.signature(eval(self.obj_char, shell.user_ns))
        except:
            return None

class TaskGetOutput(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        new_env = utils.copy_env(shell.user_ns, self.keep_objs_in_env)
        if self.extra_env is not None:
            new_env.update(copy.deepcopy(self.extra_env))
        set_context_vals(new_env, self.context, self.context_vals)
        try:
            with capture_output() as out:
                if self.pre_code is not None:
                    exec(self.pre_code, new_env)
                exec(compile(self.tree, "<script>", "exec"), new_env)
            return out[0].strip()
        except:
            return None

class TaskGetResult(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        new_env = utils.copy_env(shell.user_ns, self.keep_objs_in_env)
        if self.extra_env is not None:
            new_env.update(copy.deepcopy(self.extra_env))
        set_context_vals(new_env, self.context, self.context_vals)
        try:
            if self.pre_code is not None:
                exec(self.pre_code, new_env)
            if self.expr_code is not None:
                shell.user_ns[self.name] = exec(self.expr_code, new_env)
            else:
                shell.user_ns[self.name] = eval(compile(ast.Expression(self.tree), "<script>", "eval"), new_env)
            return str(shell.user_ns[self.name])
        except:
            return None

class TaskRunTreeStoreEnv(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        new_env = utils.copy_env(shell.user_ns, self.keep_objs_in_env)
        if self.extra_env is not None:
            new_env.update(copy.deepcopy(self.extra_env))
        set_context_vals(new_env, self.context, self.context_vals)
        try:
            if self.pre_code is not None:
                exec(self.pre_code, new_env)
            exec(compile(self.tree, "<script>", "exec"), new_env)
            # shell.user_ns[self.name] = new_env
        except:
            return None
        if self.name not in new_env :
            return "undefined"
        else :
            obj = new_env[self.name]
            shell.user_ns[self.tempname] = obj
            return str(obj)

class TaskGetFunctionCallResult(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            shell.user_ns[self.name] = shell.user_ns[self.fun_name](*self.arguments)
            return str(shell.user_ns[self.name])
        except:
            return None

class TaskGetFunctionCallOutput(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            with capture_output() as out:
                shell.user_ns[self.fun_name](*self.arguments)
            return out[0].strip()
        except:
            return None

class TaskGetFunctionCallError(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            shell.user_ns[self.fun_name](*self.arguments)
        except Exception as e:
            return e
        else:
            return None



### Wrapper functions

def isDefinedInProcess(name, process):
    return process.executeTask(TaskIsDefined(name))

def isInstanceInProcess(name, klass, process):
    return process.executeTask(TaskIsInstance(name, klass))

def getKeysInProcess(name, process):
    return process.executeTask(TaskGetKeys(name))

def getColumnsInProcess(name, process):
    return process.executeTask(TaskGetColumns(name))


def hasKeyInProcess(name, key, process):
    return process.executeTask(TaskHasKey(name, key))

def getValueInProcess(name, key, process):
    tempname = "_evaluation_object_"
    res = process.executeTask(TaskGetValue(name, key, tempname))
    if res:
        res = getRepresentation(tempname, process)
    return res


def getStream(name, process):
    return process.executeTask(TaskGetStream(name))

def getRepresentation(name, process):
    obj_class = process.executeTask(TaskGetClass(name))
    state = pythonwhat.State.State.active_state
    converters = state.get_converters()
    if obj_class in converters:
        stream = process.executeTask(TaskConvert(name, dill.dumps(converters[obj_class])))
        if isinstance(stream, list) and 'backend-error' in str(stream):
            stream = None
    else:
        stream = getStream(name, process)

    return stream

def evalInProcess(tree, process):
    # res = process.executeTask(TaskEvalCode(code, "_evaluation_object_"))
    res = process.executeTask(TaskEvalAst(tree, "_evaluation_object_"))
    if res:
        res = getRepresentation("_evaluation_object_", process)
    return res

def getSignatureInProcess(process, **kwargs):
    return process.executeTask(TaskGetSignature(**kwargs))

def getSignatureInProcessFromObj(obj_char, process):
    return process.executeTask(TaskGetSignatureFromObj(obj_char))

def getOutputInProcess(process, **kwargs):
    return process.executeTask(TaskGetOutput(**kwargs))

def getResultInProcess(process, **kwargs):
    kwargs['name'] = randomword(10)
    strrep = process.executeTask(TaskGetResult(**kwargs))
    if strrep is not None:
        bytestream = getRepresentation(kwargs['name'], process)
    else:
        bytestream = None
    return (bytestream, strrep)

def getObjectAfterExpressionInProcess(process, **kwargs):
    tempname = "_evaluation_object_"
    strrep = process.executeTask(TaskRunTreeStoreEnv(**kwargs, tempname = tempname))
    if strrep is None or strrep is "undefined" :
        bytestream = None
    else :
        bytestream = getRepresentation(tempname, process)
    return (bytestream, strrep)

def getFunctionCallResultInProcess(process, **kwargs):
    kwargs['name'] = "_evaluation_object_"
    strrep = process.executeTask(TaskGetFunctionCallResult(**kwargs))
    if strrep is not None:
        bytestream = getRepresentation("_evaluation_object_", process)
    else:
        bytestream = None
    return (bytestream, strrep)

def getFunctionCallOutputInProcess(process, **kwargs):
    return process.executeTask(TaskGetFunctionCallOutput(**kwargs))

def getFunctionCallErrorInProcess(process, **kwargs):
    return process.executeTask(TaskGetFunctionCallError(**kwargs))


## HELPERS

def get_signature(name, mapped_name, signature, manual_sigs, env):

    if isinstance(signature, str):
        if signature in manual_sigs:
            signature = inspect.Signature(manual_sigs[signature])
        else:
            raise ValueError('signature error - specified signature not found')

    if signature is None:
        # establish function
        try:
            fun = eval(mapped_name, env)
        except:
            raise ValueError("%s() was not found." % mapped_name)

        # first go through manual sigs
        # try to get signature
        try:
            if name in manual_sigs:
                signature = inspect.Signature(manual_sigs[name])
            else:
                # it might be a method, and we have to find the general method name
                if "." in mapped_name:
                    els = name.split(".")
                    try:
                        els[0] = type(eval(els[0], env)).__name__
                        generic_name = ".".join(els[:])
                    except:
                        raise ValueError('signature error - cannot convert call')
                    if generic_name in manual_sigs:
                        signature = inspect.Signature(manual_sigs[generic_name])
                    else:
                        raise ValueError('signature error - %s not in builtins' % generic_name)
                else:
                    raise ValueError('manual signature not found')
        except:
            try:
                signature = inspect.signature(fun)
            except:
                raise ValueError('signature error - cannot determine signature')

    return signature


@contextmanager
def capture_output():
    import sys
    from io import StringIO
    oldout, olderr = sys.stdout, sys.stderr
    out = [StringIO(), StringIO()]
    sys.stdout, sys.stderr = out
    yield out
    sys.stdout, sys.stderr = oldout, olderr
    out[0] = out[0].getvalue()
    out[1] = out[1].getvalue()
