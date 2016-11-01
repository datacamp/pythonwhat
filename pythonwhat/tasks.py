from pythonwhat import utils
import os
import dill
import pickle
import pythonwhat
import ast
import inspect
import copy
from pickle import PicklingError
from pythonwhat.utils_env import set_context_vals
from contextlib import contextmanager
from functools import partial, wraps

def process_task(f):
    """Decorator to (optionally) run function in a process."""
    sig = inspect.signature(f)
    @wraps(f)
    def wrapper(*args, **kwargs):
        # get bound arguments for call
        ba = sig.bind_partial(*args, **kwargs)
        # when process is specified, remove from args and use to execute
        process = ba.arguments.get('process')
        if process:
            ba.arguments['process'] = None
            # partial function since shell argument may have been left
            # unspecified, as it will be passed when the process executes
            pf = partial(wrapper, *ba.args, **ba.kwargs)
            return process.executeTask(pf)
        # otherwise, run original function
        return f(*ba.args, **ba.kwargs)
    return wrapper

def get_env(ns):
    if '__env__' in ns:
        return ns['__env__']
    else:
        return ns

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


## DEBUGGING

# import pythonwhat; pythonwhat.tasks.listElementsInProcess(state.student_process)
@process_task
def listElementsInProcess(process, shell):
    return list(get_env(shell.user_ns).keys())


# MC
@process_task
def getOptionFromProcess(process, name, shell):
    return shell.user_ns[name]


# Is a variable is defined in the process?
@process_task
def isDefinedInProcess(name, process, shell):
    return name in get_env(shell.user_ns)

# Is a variable is of a certain class in the process?
@process_task
def isInstanceInProcess(name, klass, process, shell):
    return isinstance(get_env(shell.user_ns)[name], klass)


# Get the keys() of a dictionary in the process
@process_task
def getKeysInProcess(name, process, shell):
        try:
            return list(get_env(shell.user_ns)[name].keys())
        except:
            return None

# Get the columns of a Pandas data frame in the process
@process_task
def getColumnsInProcess(name, process, shell):
        try:
            return list(get_env(shell.user_ns)[name].columns)
        except:
            return None

# Is a key defined in a collection in the process?
@process_task
def isDefinedCollInProcess(name, key, process, shell):
    return key in get_env(shell.user_ns)[name]

# Get the signature of a function inside the process

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


# Get the signature of a function based on an object inside the process
@process_task
def getSignatureInProcess(name, mapped_name, signature, manual_sigs, process, shell):
    try:
        return get_signature(name = name,
                                mapped_name = mapped_name,
                                signature = signature,
                                manual_sigs = manual_sigs,
                                env = get_env(shell.user_ns))
    except:
        return None

@process_task
def getSignatureFromObjInProcess(obj_char, process, shell):
    try:
        return inspect.signature(eval(obj_char, get_env(shell.user_ns)))
    except:
        return None



## Get the output of a tree (with setting envs, pre_code and/er expr_code)
@process_task
def getOutputInProcess(tree, process, extra_env, context, context_vals, 
                       pre_code, expr_code, keep_objs_in_env, 
                       shell):
    new_env = utils.copy_env(get_env(shell.user_ns), keep_objs_in_env)
    if extra_env is not None:
        new_env.update(copy.deepcopy(extra_env))
    set_context_vals(new_env, context, context_vals)
    try:
        with capture_output() as out:
            if pre_code is not None:
                exec(pre_code, new_env)
            if expr_code is not None:
                exec(expr_code, new_env)
            else:
                exec(compile(tree, "<script>", "exec"), new_env)
        return out[0].strip()
    except:
        return None

# Get output of function call in process
@process_task
def getFunctionCallOutputInProcess(fun_name, arguments, process, shell):
    try:
        with capture_output() as out:
            get_env(shell.user_ns)[fun_name](*arguments['args'], **arguments['kwargs'])
        return out[0].strip()
    except:
        return None

# Get error of function call in process
@process_task
def getFunctionCallErrorInProcess(fun_name, arguments, process, shell):
    try:
        get_env(shell.user_ns)[fun_name](*arguments['args'], **arguments['kwargs'])
    except Exception as e:
        return e
    else:
        return None

# Get error of an expression tree in process
@process_task
def getTreeErrorInProcess(tree, process, shell):
    try:
        eval(compile(ast.Expression(tree), "<script>", "eval"), get_env(shell.user_ns))
    except Exception as e:
        return e
    else:
        return None


# Stuff for test_with

from contextlib import ExitStack
def context_env_update(context_list, env):
    es = ExitStack()
    env_update = {}
    for context in context_list:
        cm = eval(
            compile(ast.Expression(context['node']), '<context_eval>', 'eval'),
            env)
        cm_init = es.enter_context(cm)
        context_keys = context['target_vars']
        if not context_keys:
            continue
        elif len(context_keys) == 1:
            k = list(context_keys.keys())[0]
            env_update[k] = cm_init
        else:
            assert len(context_keys) == len(cm_init)
            for (context_key, current_obj) in zip(context_keys, cm_init):
                env_update[context_key] = current_obj
    return env_update, es


@process_task
def setUpNewEnvInProcess(context, process, shell):
    shell.user_ns['__env__'] = utils.copy_env(shell.user_ns)
    try:
        context_env, es = context_env_update(context, shell.user_ns['__env__'])
        shell.user_ns['__env__'].update(context_env)
        shell.user_ns['__exit_stack__'] = es
        return True
    except Exception as e:
        return e

# break down environment
def context_objs_exit(es):
    try:
        es.close()
        return False
    except Exception as e:
        return e

@process_task
def breakDownNewEnvInProcess(process, shell):
    try:
        res = context_objs_exit(shell.user_ns['__exit_stack__'])
        del shell.user_ns['__exit_stack__']
        del shell.user_ns['__env__']
        return res
    except:
        return False

# Tasks that may need to serialize across processes ===========================

# Get the value linked to a key of a collection in the process
class TaskGetValue(object):
    def __init__(self, name, key, tempname):
        self.name = name
        self.key = key
        self.tempname = tempname

    def __call__(self, shell):
        try:
            get_env(shell.user_ns)[self.tempname] = get_env(shell.user_ns)[self.name][self.key]
            return True
        except:
            return None

def getValueInProcess(name, key, process):
    tempname = "_evaluation_object_"
    res = process.executeTask(TaskGetValue(name, key, tempname))
    if res:
        res = getRepresentation(tempname, process)
    return res

# Get a bytes or string representation of an object in the process
@process_task
def getClass(name, process, shell):
    try:
        obj = get_env(shell.user_ns)[name]
        obj_type = type(obj)
        return obj_type.__module__ + "." + obj_type.__name__
    except:
        return None

@process_task
def convert(name, converter, process, shell):
    return dill.loads(converter)(get_env(shell.user_ns)[name])

# class TaskGetObject(object):
#     def __init__(self, name):
#         self.name = name

#     def __call__(self, shell):
#         obj = get_env(shell.user_ns)[self.name]
#         #if dill.pickles(obj):
#         return obj
#        else:
#            return None

@process_task
def getStreamPickle(name, process, shell):
    try:
        return pickle.dumps(get_env(shell.user_ns)[name])
    except:
        return None

@process_task
def getStreamDill(name, process, shell):
    try:
        return dill.dumps(get_env(shell.user_ns)[name])
    except:
        return None


class ReprFail(object):
    def __init__(self, info):
        self.info = info

def getRepresentation(name, process):
    obj_class = getClass(name, process)
    converters = pythonwhat.State.State.converters
    if obj_class in converters:
        repres = convert(name, dill.dumps(converters[obj_class]), process)
        if (errored(repres)):
            repres = ReprFail("manual conversion failed")
        else: 
            return repres
    else:
        # first try to pickle
        try:
            stream = getStreamPickle(name, process)
            if not errored(stream): return pickle.loads(stream)
        except PicklingError: 
            pass

        # if it failed, try to dill
        try:
            stream = getStreamDill(name, process)
            if not errored(stream): return dill.loads(stream)
            return ReprFail("dilling inside process failed for %s - write manual converter" % obj_class)
        except PicklingError:
            return ReprFail("undilling of bytestream failed - write manual converter")

def errored(el):
    return el is None or (isinstance(el, list) and 'backend-error' in str(el))


# Make wrapper for getting an object representation from process --------------

def getResultFromProcess(res, tempname, process):
    """Get a value from process, return tuple of value, res if succesful"""
    if res not in [None, "undefined"]:
        value = getRepresentation(tempname, process)
        return (value, res)
    else: 
        return (None,  res)

# decorator to automatically get value after running process task function
def get_rep(f):
    sig = inspect.signature(f)
    @wraps(f)
    def wrapper(*args, **kwargs): 
        # get bound arguments for call
        ba = sig.bind_partial(*args, **kwargs)
        ba.apply_defaults()
        # get tempname, process arg values
        tempname = ba.arguments['tempname']
        process = ba.arguments['process']
        # run process task
        res = f(*args,**kwargs)
        # get result from task
        return getResultFromProcess(res, tempname, process)
    return wrapper

# General tasks to eval or exec code, with decorated counterparts -------------

# Eval an expression tree or node (with setting envs, pre_code and/or expr_code)
@process_task
def taskRunEval(tree,
                process, shell, 
                keep_objs_in_env = None, extra_env = None, context=None, context_vals=None, 
                pre_code = "", expr_code = "", name="", tempname='_evaluation_object_'):
    new_env = utils.copy_env(get_env(shell.user_ns), keep_objs_in_env)
    if extra_env is not None:
        new_env.update(copy.deepcopy(extra_env))
    set_context_vals(new_env, context, context_vals)
    try:
        # Execute pre_code if specified
        if pre_code: exec(pre_code, new_env)

        # If no name given, the object of interest is the output of eval
        # otherwise, we'll use name to get the object from the environment
        if not name:
            mode = 'eval'
            tree = ast.Expression(tree)
        else:
            mode = 'exec'

        # Expression code takes precedence over tree code
        if expr_code: code = expr_code
        else:         code = compile(tree, "<script>", mode)

        if mode == 'eval': 
            obj = eval(code, new_env)
        else:       
            exec(code, new_env)
            if name not in new_env:
                return "undefined"
            obj = new_env[name]

        # Set object as temp variable in original environment, so we can
        # later get its class, etc.., in order to extract it from process
        get_env(shell.user_ns)[tempname] = obj
        return str(obj)

    except:
        return None

getResultInProcess = get_rep(taskRunEval)

# Run a function call in process
# TODO: should this run the function on the original environment? what about side effects?
@process_task
def taskRunFunctionCall(fun_name, arguments, process, shell, tempname='_evaluation_object_'):
    try:
        get_env(shell.user_ns)[tempname] = get_env(shell.user_ns)[fun_name](*arguments['args'], **arguments['kwargs'])
        return str(get_env(shell.user_ns)[tempname])
    except:
        return None

getFunctionCallResultInProcess = get_rep(taskRunFunctionCall)
