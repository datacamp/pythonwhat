#import dill
#from .output import NoOutput, CaptureExecOutput, OutputManager
from . import utils
import os
import dill
import pythonwhat
import ast
import inspect

class TaskIsDefined(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell, original_ns_keys):
        return self.name in shell.user_ns

class TaskGetStream(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell, original_ns_keys):
        try:
            return dill.dumps(shell.user_ns[self.name])
        except:
            return None

class TaskGetClass(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell, original_ns_keys):
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

    def __call__(self, shell, original_ns_keys):
        return dill.loads(self.converter)(shell.user_ns[self.name])

class TaskEvalAst(object):
    def __init__(self, tree, name):
        self.tree = tree
        self.name = name

    def __call__(self, shell, original_ns_keys):
        try:
            shell.user_ns[self.name] = eval(compile(ast.Expression(self.tree), "<script>", "eval"), shell.user_ns)
            return True
        except:
            return None

class TaskGetSignature(object):
    def __init__(self, name, mapped_name, signature, manual_sigs):
        self.name = name
        self.mapped_name = mapped_name
        self.signature = signature
        self.manual_sigs = manual_sigs

    def __call__(self, shell, original_ns_keys):
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

    def __call__(self, shell, original_ns_keys):
        try:
            return inspect.signature(eval(self.obj_char, shell.user_ns))
        except:
            return None




def isDefined(name, process):
    return process.executeTask(TaskIsDefined(name))

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
    if not res:
        return None
    else:
        return getRepresentation("_evaluation_object_", process)

def getSignatureInProcess(name, mapped_name, signature, manual_sigs, process):
    return process.executeTask(TaskGetSignature(name, mapped_name, signature, manual_sigs))

def getSignatureInProcessFromObj(obj_char, process):
    return process.executeTask(TaskGetSignatureFromObj(obj_char))


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

