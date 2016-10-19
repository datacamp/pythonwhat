from pythonwhat import utils
import os
import dill
import pickle
import pythonwhat
import ast
import inspect
import copy
import inspect
from pythonwhat.utils_env import set_context_vals
from contextlib import contextmanager
from functools import partial, wraps

def process_task(f):
    """Decorator to return partial of task function if process arg not in call"""
    sig = inspect.signature(f)
    @wraps(f)
    def wrapper(*args, **kwargs):
        # get bound arguments for call
        bargs = sig.bind_partial(*args, **kwargs).arguments
        # when process is specified, use to execute
        process = bargs.get('process')
        if process:
            bargs['process'] = None
            pf = partial(wrapper, *bargs.values())
            return process.executeTask(pf)
        # otherwise, return partialed function, that a process may be passed to
        return f(**bargs)
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
class TaskGetClass(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        try:
            obj = get_env(shell.user_ns)[self.name]
            obj_type = type(obj)
            return obj_type.__module__ + "." + obj_type.__name__
        except:
            return None


class TaskConvert(object):
    def __init__(self, name, converter):
        self.name = name
        self.converter = converter

    def __call__(self, shell):
        return dill.loads(self.converter)(get_env(shell.user_ns)[self.name])

# class TaskGetObject(object):
#     def __init__(self, name):
#         self.name = name

#     def __call__(self, shell):
#         obj = get_env(shell.user_ns)[self.name]
#         #if dill.pickles(obj):
#         return obj
#        else:
#            return None

class TaskGetStreamPickle(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        try:
            return pickle.dumps(get_env(shell.user_ns)[self.name])
        except:
            return None


class TaskGetStreamDill(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        try:
            return dill.dumps(get_env(shell.user_ns)[self.name])
        except:
            return None


class ReprFail(object):
    def __init__(self, info):
        self.info = info

def getRepresentation(name, process):
    obj_class = process.executeTask(TaskGetClass(name))
    converters = pythonwhat.State.State.converters
    if obj_class in converters:
        repres = process.executeTask(TaskConvert(name, dill.dumps(converters[obj_class])))
        if (errored(repres)):
            repres = ReprFail("manual conversion failed")
    else:
        # first try to pickle
        try:
            stream = process.executeTask(TaskGetStreamPickle(name))
            fail = errored(stream) or stream is None
        except:
            fail = True

        if not fail:
            try:
                repres = pickle.loads(stream)
            except:
                fail = True

        # if it failed, try to dill
        if fail:
            try:
                stream = process.executeTask(TaskGetStreamDill(name))
                fail2 = errored(stream) or stream is None
            except:
                fail2 = True

            if fail2:
                repres = ReprFail("dilling inside process failed for %s - write manual converter" % obj_class)
            else :
                try:
                    repres = dill.loads(stream)
                except:
                    repres = ReprFail("undilling of bytestream failed - write manual converter")

    return repres

def errored(el):
    return(isinstance(el, list) and 'backend-error' in str(el))


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
    return process.executeTask(TaskGetOutput(**kwargs))


# Get the result of a tree (with setting envs, pre_code and/or expr_code)
class TaskGetResult(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        new_env = utils.copy_env(get_env(shell.user_ns), self.keep_objs_in_env)
        if self.extra_env is not None:
            new_env.update(copy.deepcopy(self.extra_env))
        set_context_vals(new_env, self.context, self.context_vals)
        try:
            if self.pre_code is not None:
                exec(self.pre_code, new_env)
            if self.expr_code is not None:
                get_env(shell.user_ns)[self.name] = eval(self.expr_code, new_env)
            else:
                get_env(shell.user_ns)[self.name] = eval(compile(ast.Expression(self.tree), "<script>", "eval"), new_env)
            return str(get_env(shell.user_ns)[self.name])
        except:
            return None

def getResultInProcess(process, **kwargs):
    kwargs['name'] = "_evaluation_object_"
    strrep = process.executeTask(TaskGetResult(**kwargs))
    if strrep is not None:
        value = getRepresentation(kwargs['name'], process)
    else:
        value = None
    return (value, strrep)


# Run code (with setting envs, pre_code and/er expr_code) to extract info from later on
class TaskRunTreeStoreEnv(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        new_env = utils.copy_env(get_env(shell.user_ns), self.keep_objs_in_env)
        if self.extra_env is not None:
            new_env.update(copy.deepcopy(self.extra_env))
        set_context_vals(new_env, self.context, self.context_vals)
        try:
            if self.pre_code is not None:
                exec(self.pre_code, new_env)
            exec(compile(self.tree, "<script>", "exec"), new_env)
            # get_env(shell.user_ns)[self.name] = new_env
        except:
            return None
        if self.name not in new_env :
            return "undefined"
        else :
            obj = new_env[self.name]
            get_env(shell.user_ns)[self.tempname] = obj
            return str(obj)

def getObjectAfterExpressionInProcess(process, **kwargs):
    tempname = "_evaluation_object_"
    kwargs['tempname'] = tempname
    strrep = process.executeTask(TaskRunTreeStoreEnv(**kwargs))
    if strrep is None or strrep is "undefined" :
        bytestream = None
    else :
        bytestream = getRepresentation(tempname, process)
    return (bytestream, strrep)


# Get result of function call in process
class TaskGetFunctionCallResult(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            get_env(shell.user_ns)[self.name] = get_env(shell.user_ns)[self.fun_name](*self.arguments['args'], **self.arguments['kwargs'])
            return str(get_env(shell.user_ns)[self.name])
        except:
            return None

def getFunctionCallResultInProcess(process, **kwargs):
    kwargs['name'] = "_evaluation_object_"
    strrep = process.executeTask(TaskGetFunctionCallResult(**kwargs))
    if strrep is not None:
        bytestream = getRepresentation("_evaluation_object_", process)
    else:
        bytestream = None
    return (bytestream, strrep)

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


# Get result of an expression tree in process
class TaskGetTreeResult(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            get_env(shell.user_ns)[self.name] = eval(compile(ast.Expression(self.tree), "<script>", "eval"), get_env(shell.user_ns))
            return str(get_env(shell.user_ns)[self.name])
        except:
            return None

def getTreeResultInProcess(process, **kwargs):
    kwargs['name'] = "_evaluation_object_"
    strrep = process.executeTask(TaskGetTreeResult(**kwargs))
    if strrep is not None:
        bytestream = getRepresentation("_evaluation_object_", process)
    else:
        bytestream = None
    return (bytestream, strrep)


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

def context_env_update(context_list, env):
    env_update = {}
    context_objs = []
    for context in context_list:
        context_obj = eval(
            compile(context['context_expr'], '<context_eval>', 'eval'),
            env)
        context_objs.append(context_obj)
        context_obj_init = context_obj.__enter__()
        context_keys = context['optional_vars']
        if context_keys is None:
            continue
        elif len(context_keys) == 1:
            env_update[context_keys[0]] = context_obj_init
        else:
            assert len(context_keys) == len(context_obj_init)
            for (context_key, current_obj) in zip(context_keys, context_obj_init):
                env_update[context_key] = current_obj
    return (env_update, context_objs)


@process_task
def setUpNewEnvInProcess(context, process, shell):
    shell.user_ns['__env__'] = utils.copy_env(shell.user_ns)
    try:
        context_env, context_objs = context_env_update(context, shell.user_ns['__env__'])
        shell.user_ns['__env__'].update(context_env)
        shell.user_ns['__context_obj__'] = context_objs
        return True
    except Exception as e:
        return e

# break down environment
def context_objs_exit(context_objs):
    got_error = False
    for context_obj in context_objs:
        try:
            context_obj.__exit__(*([None]*3))
        except Exception as e:
            got_error = e

    return got_error

@process_task
def breakDownNewEnvInProcess(process, shell):
    try:
        res = context_objs_exit(shell.user_ns['__context_obj__'])
        del shell.user_ns['__context_obj__']
        del shell.user_ns['__env__']
        return res
    except:
        return False
