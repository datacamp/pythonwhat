from pythonwhat import utils
import os
import dill
import pythonwhat
import ast
import inspect
import copy
from pythonwhat.utils_env import set_context_vals
from contextlib import contextmanager


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
class TaskListElements(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        return list(get_env(shell.user_ns).keys())

def listElementsInProcess(process):
    return process.executeTask(TaskListElements())


# MC
class TaskGetOption(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        return shell.user_ns[self.name]

def getOptionFromProcess(process, name):
    return process.executeTask(TaskGetOption(name))


# Is a variable is defined in the process?
class TaskIsDefined(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        return self.name in get_env(shell.user_ns)

def isDefinedInProcess(name, process):
    return process.executeTask(TaskIsDefined(name))

# Is a variable is of a certain class in the process?
class TaskIsInstance(object):
    def __init__(self, name, klass):
        self.name = name
        self.klass = klass

    def __call__(self, shell):
        return isinstance(get_env(shell.user_ns)[self.name], self.klass)

def isInstanceInProcess(name, klass, process):
    return process.executeTask(TaskIsInstance(name, klass))


# Get the keys() of a dictionary in the process
class TaskGetKeys(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        try:
            return list(get_env(shell.user_ns)[self.name].keys())
        except:
            return None

def getKeysInProcess(name, process):
    return process.executeTask(TaskGetKeys(name))


# Get the columns of a Pandas data frame in the process
class TaskGetColumns(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        try:
            return list(get_env(shell.user_ns)[self.name].columns)
        except:
            return None

def getColumnsInProcess(name, process):
    return process.executeTask(TaskGetColumns(name))


# Is a key defined in a collection in the process?
class TaskDefinedColl(object):
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __call__(self, shell):
        return self.key in get_env(shell.user_ns)[self.name]

def isDefinedCollInProcess(name, key, process):
    return process.executeTask(TaskDefinedColl(name, key))


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

class TaskGetObject(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell):
        return get_env(shell.user_ns)[self.name]

class TaskGetStream(object):
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
    state = pythonwhat.State.State.active_state
    converters = state.get_converters()
    if obj_class in converters:
        repres = process.executeTask(TaskConvert(name, dill.dumps(converters[obj_class])))
        if isinstance(repres, list) and 'backend-error' in str(repres):
            repres = ReprFail("manual conversion failed")
    else:
        try:
            repres = process.executeTask(TaskGetObject(name))
            if isinstance(repres, list) and 'backend-error' in str(repres):
                fail = True
            else:
                fail = False
        except:
            fail = True
        if fail:
            stream = process.executeTask(TaskGetStream(name))
            if stream is None:
                repres = ReprFail("dilling inside process failed - write manual converter")
            else :
                try:
                    repres = dill.loads(stream)
                except:
                    repres = ReprFail("undilling of bytestream failed - write manual converter")
    return repres



# Get the signature of a function inside the process
class TaskGetSignature(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            return get_signature(name = self.name,
                                 mapped_name = self.mapped_name,
                                 signature = self.signature,
                                 manual_sigs = self.manual_sigs,
                                 env = get_env(shell.user_ns))
        except:
            return None


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
class TaskGetSignatureFromObj(object):
    def __init__(self, obj_char):
        self.obj_char = obj_char

    def __call__(self, shell):
        try:
            return inspect.signature(eval(self.obj_char, get_env(shell.user_ns)))
        except:
            return None

def getSignatureInProcess(process, **kwargs):
    return process.executeTask(TaskGetSignature(**kwargs))

def getSignatureFromObjInProcess(obj_char, process):
    return process.executeTask(TaskGetSignatureFromObj(obj_char))



# Get the output of a tree (with setting envs, pre_code and/er expr_code)
class TaskGetOutput(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        new_env = utils.copy_env(get_env(shell.user_ns), self.keep_objs_in_env)
        if self.extra_env is not None:
            new_env.update(copy.deepcopy(self.extra_env))
        set_context_vals(new_env, self.context, self.context_vals)
        try:
            with capture_output() as out:
                if self.pre_code is not None:
                    exec(self.pre_code, new_env)
                if self.expr_code is not None:
                    exec(self.expr_code, new_env)
                else:
                    exec(compile(self.tree, "<script>", "exec"), new_env)
            return out[0].strip()
        except:
            return None

def getOutputInProcess(process, **kwargs):
    return process.executeTask(TaskGetOutput(**kwargs))


# Get the result of a tree (with setting envs, pre_code and/er expr_code)
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
                get_env(shell.user_ns)[self.name] = exec(self.expr_code, new_env)
            else:
                get_env(shell.user_ns)[self.name] = eval(compile(ast.Expression(self.tree), "<script>", "eval"), new_env)
            return str(get_env(shell.user_ns)[self.name])
        except:
            return None

def getResultInProcess(process, **kwargs):
    kwargs['name'] = "_evaluation_object_"
    strrep = process.executeTask(TaskGetResult(**kwargs))
    if strrep is not None:
        bytestream = getRepresentation(kwargs['name'], process)
    else:
        bytestream = None
    return (bytestream, strrep)


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
            get_env(shell.user_ns)[self.name] = get_env(shell.user_ns)[self.fun_name](*self.arguments)
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
class TaskGetFunctionCallOutput(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            with capture_output() as out:
                get_env(shell.user_ns)[self.fun_name](*self.arguments)
            return out[0].strip()
        except:
            return None

def getFunctionCallOutputInProcess(process, **kwargs):
    return process.executeTask(TaskGetFunctionCallOutput(**kwargs))

# Get error of function call in process
class TaskGetFunctionCallError(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            get_env(shell.user_ns)[self.fun_name](*self.arguments)
        except Exception as e:
            return e
        else:
            return None

def getFunctionCallErrorInProcess(process, **kwargs):
    return process.executeTask(TaskGetFunctionCallError(**kwargs))



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
class TaskGetTreeError(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            eval(compile(ast.Expression(self.tree), "<script>", "eval"), get_env(shell.user_ns))
        except Exception as e:
            return e
        else:
            return None

def getTreeErrorInProcess(process, **kwargs):
    return process.executeTask(TaskGetTreeError(**kwargs))


# Stuff for test_with
class TaskSetUpNewEnv(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        shell.user_ns['__env__'] = utils.copy_env(shell.user_ns)
        try:
            context_env, context_objs = context_env_update(self.context, shell.user_ns['__env__'])
            shell.user_ns['__env__'].update(context_env)
            shell.user_ns['__context_obj__'] = context_objs
            return True
        except Exception as e:
            return e

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


def setUpNewEnvInProcess(process, **kwargs):
    return process.executeTask(TaskSetUpNewEnv(**kwargs))

class TaskBreakDownNewEnv(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, shell):
        try:
            res = context_objs_exit(shell.user_ns['__context_obj__'])
            del shell.user_ns['__context_obj__']
            del shell.user_ns['__env__']
            return res
        except:
            return False


def context_objs_exit(context_objs):
    got_error = False
    for context_obj in context_objs:
        try:
            context_obj.__exit__(*([None]*3))
        except Exception as e:
            got_error = e

    return got_error

def breakDownNewEnvInProcess(process, **kwargs):
    return process.executeTask(TaskBreakDownNewEnv(**kwargs))
