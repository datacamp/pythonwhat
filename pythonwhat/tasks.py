#import dill
#from .output import NoOutput, CaptureExecOutput, OutputManager
from . import utils
import os
import dill
from pythonwhat.State import State

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

# class TaskEvalCode(object):
#     def __init__(self, code):
#         self.code = code

#     def __call__(self, shell, original_ns_keys):
#         #code = "x = " + code
#         #return dill.dumps(shell.user_ns['x'])

def isDefined(name, process):
    return process.executeTask(TaskIsDefined(name))

def getStream(name, process):
    return process.executeTask(TaskGetStream(name))

def getRepresentation(name, process):
    obj_class = process.executeTask(TaskGetClass(name))
    state = State.active_state
    converters = state.get_converters()
    if obj_class in converters:
        stream = process.executeTask(TaskConvert(name, dill.dumps(converters[obj_class])))
        if isinstance(stream, list) and 'backend-error' in str(stream):
            stream = None
    else:
        stream = getStream(name, process)

    return stream

    # else:
    #     return None
    # state.get_converters()[obj_type]
