from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test, EqualTest
from pythonwhat.Feedback import Feedback
from pythonwhat.utils import get_ord
from types import GeneratorType
from functools import partial
import copy

def part_to_child(stu_part, sol_part, append_message, state, node_name=None):
    # stu_part and sol_part will be accessible on all templates
    append_message['kwargs'].update({'stu_part': stu_part, 'sol_part': sol_part})

    # if the parts are dictionaries, use to deck out child state
    if all(isinstance(p, dict) for p in [stu_part, sol_part]):
        return state.to_child_state(student_subtree=stu_part['node'],
                                    solution_subtree=sol_part['node'],
                                    student_context=stu_part.get('target_vars'),
                                    solution_context=sol_part.get('target_vars'),
                                    student_parts=stu_part,
                                    solution_parts=sol_part,
                                    highlight = stu_part.get('highlight'),
                                    append_message = append_message,
                                    node_name=node_name)

    # otherwise, assume they are just nodes
    return state.to_child_state(student_subtree=stu_part,
                                solution_subtree=sol_part,
                                append_message = append_message)


def check_part(name, part_msg, state=None, missing_msg="Are you sure it's defined?", expand_msg=""):
    """Return child state with name part as its ast tree"""
    rep = Reporter.active_reporter

    if not part_msg: part_msg = name
    append_message = {'msg': expand_msg, 'kwargs': {'part': part_msg,}}

    has_part(name, missing_msg, state, append_message['kwargs'])
    stu_part = state.student_parts[name]
    sol_part = state.solution_parts[name]

    return part_to_child(stu_part, sol_part, append_message, state)

def check_part_index(name, index, part_msg,
                     missing_msg="FMT:Are you sure it is defined?",
                     state=None, expand_msg=""):
    """Return child state with indexed name part as its ast tree"""

    rep = Reporter.active_reporter

    # create message
    ordinal = "" if isinstance(index, str) else get_ord(index+1)
    fmt_kwargs = {'index': index, 'ordinal': ordinal}
    fmt_kwargs['part'] = part_msg.format(**fmt_kwargs)

    append_message = {'msg': expand_msg,
                      'kwargs': fmt_kwargs}

    # check there are enough parts for index
    has_part(name, missing_msg, state, append_message['kwargs'], index)

    # get part at index
    stu_part = state.student_parts[name][index]
    sol_part = state.solution_parts[name][index]

    # return child state from part
    return part_to_child(stu_part, sol_part, append_message, state)

MSG_MISSING = "FMT:The system wants to check the {typestr} you defined but hasn't found it."
MSG_PREPEND = "__JINJA__:Check your code in the{{' ' + child['part']+ ' of the' if child['part']}} {{typestr}}. "
def check_node(name, index=0, typestr='{ordinal} node', missing_msg=MSG_MISSING, expand_msg=MSG_PREPEND, state=None):
    rep = Reporter.active_reporter
    stu_out = getattr(state, 'student_'+name)
    sol_out = getattr(state, 'solution_'+name)

    # check if there are enough nodes for index
    fmt_kwargs = {'ordinal': get_ord(index+1) if isinstance(index, int) else "",
                  'index': index,
                  'name': name}
    fmt_kwargs['typestr'] = typestr.format(**fmt_kwargs)

    # test if node can be indexed succesfully
    try: stu_out[index]
    except (KeyError, IndexError):                  # TODO comment errors
        _msg = state.build_message(missing_msg, fmt_kwargs)
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    # get node at index
    stu_part = stu_out[index]
    sol_part = sol_out[index]

    append_message = {'msg': expand_msg,
                      'kwargs': fmt_kwargs
                      }

    return part_to_child(stu_part, sol_part, append_message, state, node_name=name)


# Part tests ------------------------------------------------------------------

def has_part(name, msg, state=None, fmt_kwargs=None, index=None):
    rep = Reporter.active_reporter
    d = {'sol_part': state.solution_parts,
         'stu_part': state.student_parts,
         **fmt_kwargs
         }

    try: 
        part = state.student_parts[name]
        if index is not None: part = part[index]
        if part is None: raise KeyError
    except (KeyError, IndexError):
        _msg = state.build_message(msg, d)
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    return state


def has_equal_part(name, msg, state):
    rep = Reporter.active_reporter
    d = {'stu_part': state.student_parts,
         'sol_part': state.solution_parts,
         'name': name}

    _msg = state.build_message(msg, d)
    rep.do_test(EqualTest(d['stu_part'][name], d['sol_part'][name], Feedback(_msg, state.highlight)))

    return state

# TODO: shouldn't have to hardcode message
def has_equal_part_len(name, insufficient_msg, state=None):
    rep = Reporter.active_reporter
    d = dict(stu_len = len(state.student_parts[name]),
             sol_len = len(state.solution_parts[name]))

    if d['stu_len'] != d['sol_len']:
        _msg = state.build_message(insufficient_msg, d)
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    return state

# functions for running multiple sub-tests ------------------------------------

def extend(*args, state=None):
    """Run multiple subtests in sequence, each using the output state of the previous."""

    # when input is a single list of subtests
    args = args[0] if len(args) == 1 and hasattr(args[0], '__iter__') else args

    for test in args: state = test(state=state)  # run tests sequentially
    return state                                 # return final state for chaining

def multi(*args, state=None):
    """Run multiple subtests. Return original state (for chaining)."""
    if any(args):
        rep = Reporter.active_reporter

        # when input is a single list of subtests
        if len(args) == 1 and isinstance(args[0], (list, tuple, GeneratorType)):
            args = args[0]

        for test in args:
            # assume test is function needing a state argument
            # partial state so reporter can test
            closure = partial(test, state=state)
            rep.do_test(closure, "", state.highlight)

    # return original state, so can be chained
    return state

from pythonwhat.Test import TestFail

def test_not(*args, msg, state=None):
    """Pass if all of the subtests fail"""
    rep = Reporter.active_reporter

    try: multi(*args, state=state)
    except TestFail as e:
        return state
    
    _msg = state.build_message(msg)
    return rep.do_test(Test(_msg))

# utility functions -----------------------------------------------------------

def quiet(n = 0, state=None):
    """Turn off prepended messages. Defaults to turning all off."""
    cpy = copy.copy(state)
    hushed = [{**m, 'msg': ""} for m in cpy.messages]
    cpy.messages = hushed
    return cpy

def fail(msg="", state=None):
    """Fail test with message"""
    rep = Reporter.active_reporter
    _msg = state.build_message(msg)
    rep.do_test(Test(Feedback(_msg, state.highlight)))

    return state

import ast
def override(solution, state=None):
    """Change the focused solution code."""

    # the old ast may be a number of node types, but generally either a
    # (1) ast.Module, or for single expressions...
    # (2) whatever was grabbed using module.body[0]
    # (3) module.body[0].value, when module.body[0] is an Expr node
    old_ast = state.solution_tree
    new_ast = ast.parse(solution)
    if not isinstance(old_ast, ast.Module) and len(new_ast.body) == 1:
        expr = new_ast.body[0]
        candidates = [expr, expr.value] if isinstance(expr, ast.Expr) else [expr]
        for node in candidates:
            if isinstance(node, old_ast.__class__): 
                new_ast = node
                break

    kwargs  = state.messages[-1] if state.messages else {}
    child = state.to_child_state(
            solution_subtree = new_ast,
            student_subtree = state.student_tree,
            highlight = state.highlight,
            append_message = {'msg': "", 'kwargs': kwargs}
            )

    return child
    

# context functions -----------------------------------------------------------

from pythonwhat.tasks import setUpNewEnvInProcess, breakDownNewEnvInProcess
def with_context(*args, state=None):

    rep = Reporter.active_reporter

    # set up context in processes
    solution_res = setUpNewEnvInProcess(process = state.solution_process,
                                        context = state.solution_parts['with_items'])
    if isinstance(solution_res, Exception):
        raise Exception("error in the solution, running test_with(): %s" % str(solution_res))

    student_res = setUpNewEnvInProcess(process = state.student_process,
                                       context = state.student_parts['with_items'])
    if isinstance(student_res, AttributeError):
        rep.do_test(Test(Feedback("In your `with` statement, you're not using a correct context manager.", child.highlight)))

    if isinstance(student_res, (AssertionError, ValueError, TypeError)):
        rep.do_test(Test(Feedback("In your `with` statement, the number of values in your context manager "
                                  "doesn't correspond to the number of variables you're trying to assign it to.", child.highlight)))

    # run subtests
    try:
        multi(*args, state=state)
    finally:
        # exit context
        if breakDownNewEnvInProcess(process = state.solution_process):
            raise Exception("error in the solution, closing the `with` fails with: %s" % (close_solution_context))

        if breakDownNewEnvInProcess(process = state.student_process):

            rep.do_test(Test(Feedback("Your `with` statement can not be closed off correctly, you're " + \
                            "not using the context manager correctly.", state.highlight)),
                        fallback_ast = state.highlight)
    return state

def set_context(*args, state=None, **kwargs):
    """Update context values for student and solution environments.
    
    Note that excess args and unmatched kwargs will be unused in the student environment.
    If an argument is specified both by name and position args, ``set_context()`` will use the named arg.
    """
    stu_crnt = state.student_context.context
    sol_crnt = state.solution_context.context
    # set args specified by pos -----------------------------------------------
    # stop if too many pos args for solution
    if len(args) > len(sol_crnt): 
        raise IndexError("Too many positional args. There are {} context vals, but tried to set {}"
                            .format(len(sol_crnt), len(args)))
    # set pos args
    upd_sol = sol_crnt.update(dict(zip(stu_crnt.keys(), args)))
    upd_stu = stu_crnt.update(dict(zip(sol_crnt.keys(), args)))

    # set args specified by keyword -------------------------------------------
    if set(kwargs) - set(upd_sol):
        raise KeyError("Context val names are {}, but tried to set {}"
                            .format(upd_sol or "none", kwargs.keys()))
    out_sol = upd_sol.update(kwargs)
    # need to match keys in kwargs with corresponding keys in stu context
    # in case they used, e.g., different loop variable names
    match_keys = dict(zip(sol_crnt.keys(), stu_crnt.keys()))
    out_stu = upd_stu.update({match_keys[k]: v for k,v in kwargs.items() if k in match_keys})

    return state.to_child_state(student_context = out_stu, solution_context = out_sol)

def set_env(state = None, **kwargs):
    """Update/set environemnt variables for student and solution environments.

    When ``has_equal_x()`` is used after this, the variables specified through this function will
    be available in the student and solution process. Note that you will not see these variables
    in the student process of the state produced by this function: the values are saved on the state
    and are only added to the student and solution processes when ``has_equal_ast()`` is called.
    """

    stu_crnt = state.student_env.context
    sol_crnt = state.solution_env.context

    stu_new = stu_crnt.update(kwargs)
    sol_new = sol_crnt.update(kwargs)

    return state.to_child_state(student_env = stu_new, solution_env = sol_new)

def check_args(name, missing_msg='FMT:Are you sure it is defined?', state=None):
    """Check whether a function argument is specified.

    This function can follow ``check_function()`` in an SCT chain and verifies whether an argument is specified.
    If you want to go on and check whether the argument was correctly specified, you can can continue chaining with
    ``has_equal_value()`` (value-based check) or ``has_equal_ast()`` (AST-based check)

    This function can also follow ``check_function_def()`` or ``check_lambda_exp()`` to see if arguments have been
    specified.

    Args:
        name (str): the name of the argument for which you want to check it is specified. This can also be
            a number, in which case it refers to the positional arguments. Named argumetns take precedence.
        missing_msg (str): If specified, this overrides an automatically generated feedback message in case
            the student did specify the argument.
        state (State): State object that is passed from the SCT Chain (don't specify this).

    :Examples:

        Student and solution code::

            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])
            np.mean(arr)

        SCT::

            # Verify whether arr was correctly set in np.mean
            # has_equal_value() checks the value of arr, used to set argument a
            Ex().check_function('numpy.mean').check_args('a').has_equal_value()

            # Verify whether arr was correctly set in np.mean
            # has_equal_ast() checks the expression used to set argument a
            Ex().check_function('numpy.mean').check_args('a').has_equal_ast()

        Student and solution code::

            def my_power(x):
                print("calculating sqrt...")
                return(x * x)

        SCT::

            Ex().check_function_def('my_power').multi(
                check_args('x')  # Argument specified by name, will fail if student used y instead.
                check_args(0)    # Argument specified by position, still passes if student used y instead.
            )

    """
    if name in ['*args', '**kwargs']:
        return check_part(name, name, state=state, missing_msg = missing_msg)
    else: 
        arg_str = "%s argument"%get_ord(name+1) if isinstance(name, int) else "argument `%s`"%name
        return check_part_index('args', name, arg_str, state=state, missing_msg = missing_msg)


# CALL CHECK ==================================================================

from pythonwhat.tasks import getResultInProcess, getOutputInProcess, getErrorInProcess, ReprFail
import ast

evalCalls = {'value':  getResultInProcess,
             'output': getOutputInProcess,
             'error':  getErrorInProcess}

call_warnings = {
        'value': 'in the solution process resulted in an error',
        'error': 'did not generate an error in the solution environment',
        'output': 'in the solution process resulted in an error'
        }

def fix_format(arguments):
    if isinstance(arguments, str):
        arguments = (arguments, )
    if isinstance(arguments, tuple):
        arguments = list(arguments)

    if isinstance(arguments, list):
        arguments = {'args': arguments, 'kwargs': {}}

    if not isinstance(arguments, dict) or 'args' not in arguments or 'kwargs' not in arguments:
        raise ValueError("Wrong format of arguments in 'results', 'outputs' or 'errors'; either a list, or a dictionary with names args (a list) and kwargs (a dict)")

    return(arguments)

# TODO: test string syntax with check_function_def
#       test argument syntax with check_lambda
#       implement for error and output
def run_call(args, node, process, get_func, **kwargs):
    # Get function expression
    if isinstance(node, ast.FunctionDef):                     # function name
        func_expr = ast.Name(id=node.name, ctx=ast.Load())
    elif isinstance(node, ast.Lambda):                        # lambda body expr
        func_expr = node
    else: raise TypeError("Only function definition or lambda may be called")

    # args is a call string or argument list/dict
    if isinstance(args, str):
        parsed = ast.parse(args).body[0].value
        parsed.func = func_expr
        ast.fix_missing_locations(parsed)
        return get_func(process = process, tree = parsed, **kwargs)
    else:
        # e.g. list -> {args: [...], kwargs: {}} 
        fmt_args = fix_format(args)           
        ast.fix_missing_locations(func_expr)
        return get_func(process = process, tree=func_expr, call = fmt_args, **kwargs)
        

MSG_CALL_INCORRECT = "FMT:Calling it should result in {str_sol}, instead got {str_stu}"
MSG_CALL_ERROR     = "FMT:Calling it should result in {str_sol}, instead got an error"
def call(args, 
         test='value', 
         incorrect_msg=MSG_CALL_INCORRECT, 
         error_msg=MSG_CALL_ERROR, 
         # TODO kept for backwards compatibility in test_function_definition/lambda
         argstr='',
         func=None,
         state=None, **kwargs):
    """Call function definition so you can compare value/output/error generated.

    This function is chained from ``check_function_def()``.

    Args:
        args: call string or argument list that specifies how the function definition should be called.
        test (str): Either 'value', 'output' or 'error', specifying if you want to compare the return value,
            the output generated or the error generated when calling the function.
        incorrect_msg (str): If specified, this overrides the automatic feedback message when the
            comparison (value, output or error) is not correct.
        error_msg (str): If specified, this overrides the automatic message that is generated when
            the call generated an error (when it shouldn't) or didn't generate one (when it should).
        argstr (str): argument for backwards compatibility.
        func (function): binary function that tells you how the comparison should be.
        state (State): state object that is chained from.

    :Example:

        Student and solution code::

            def my_power(x):
                print("calculating sqrt...")
                return(x * x)

        SCT::

            Ex().check_function_def('my_power').multi(
                call("my_power(3)", "value"),  # specified as string, compare return value
                call([3], "value"),            # specifies as list, compare return value
                call([3], "output")            # specified as list, compare output generated
            )

    """

    rep = Reporter.active_reporter

    assert test in ('value', 'output', 'error')

    get_func = evalCalls[test]

    # Run for Solution --------------------------------------------------------
    eval_sol, str_sol = run_call(args, state.solution_parts['node'], state.solution_process, get_func, **kwargs)

    if (test == 'error') ^ isinstance(str_sol, Exception):
        _msg = state.build_message("FMT:Calling for arguments {args} resulted in an error (or not an error if testing for one). Error message: {type_err} {str_sol}",
                                   dict(args=args, type_err=type(str_sol), str_sol=str_sol))
        raise ValueError(_msg)

    if isinstance(eval_sol, ReprFail):
        _msg = state.build_message("FMT:Can't get the result of calling it for arguments {args}: {eval_sol.info}",
                                   dict(args = args, eval_sol=eval_sol))
        raise ValueError(_msg)

    # Run for Submission ------------------------------------------------------
    eval_stu, str_stu = run_call(args, state.student_parts['node'], state.student_process, get_func, **kwargs)
    fmt_kwargs = {'part': argstr, 'argstr': argstr, 'str_sol': str_sol, 'str_stu': str_stu}

    # either error test and no error, or vice-versa
    stu_node = state.student_parts['node']
    if (test == 'error') ^ isinstance(str_stu, Exception):
        _msg = state.build_message(error_msg, fmt_kwargs)
        rep.do_test(Test(Feedback(_msg, stu_node)))

    # incorrect result
    _msg = state.build_message(incorrect_msg, fmt_kwargs)
    rep.do_test(EqualTest(eval_sol, eval_stu, Feedback(_msg, stu_node), func))

    return state

# Expression tests ------------------------------------------------------------
from pythonwhat.tasks import ReprFail, UndefinedValue
from pythonwhat import utils

def has_equal_ast(incorrect_msg="FMT: Your code does not seem to match the solution.", code=None, exact=True, state=None):
    """Test whether abstract syntax trees match between the student and solution code.

    ``has_equal_ast()`` can be used in two ways:

    * As a robust version of ``has_code()``. By setting ``code``, you can look for the AST representation of ``code`` in the student's submission.
    * As an expression-based check when using more advanced SCT chain, e.g. to compare the equality of expressions to set function arguments.

    Args:
        incorrect_msg: message displayed when ASTs mismatch.
        code: optional code to use instead of the solution AST
        exact: whether the representations must match exactly. If false, the solution AST
               only needs to be contained within the student AST (similar to using test student typed).

    :Example:

        Student and Solution Code::

            dict(a = 'value').keys()

        SCT::

            # all pass
            Ex().has_equal_ast()
            Ex().has_equal_ast(code = "dict(a = 'value').keys()")
            Ex().has_equal_ast(code = "dict(a = 'value')", exact = False)

        Student and Solution Code::

            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])
            np.mean(arr)

        SCT::

            # Check underlying value of arugment a of np.mean:
            Ex().check_function('numpy.mean').check_args('a').has_equal_ast()

            # Only check AST equality of expression used to specify argument a:
            Ex().check_function('numpy.mean').check_args('a').has_equal_ast()

    """
    rep = Reporter.active_reporter

    def parse_tree(n):
        # get contents of module.body if only 1 element
        crnt = n.body[0] if isinstance(n, ast.Module) and len(n.body) == 1 else n

        # remove Expr if it exists
        return ast.dump(crnt.value if isinstance(crnt, ast.Expr) else crnt)
        
    stu_rep = parse_tree(state.student_tree)
    sol_rep = parse_tree(state.solution_tree if not code else ast.parse(code))

    _msg = state.build_message(incorrect_msg)

    if exact:
        rep.do_test(EqualTest(stu_rep, sol_rep, Feedback(_msg, state.highlight)))
    elif not sol_rep in stu_rep:
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    return state

DEFAULT_INCORRECT_MSG="__JINJA__:Unexpected expression {{test}}: expected `{{sol_eval}}`, got `{{stu_eval}}`{{' with values ' + extra_env if extra_env}}."
DEFAULT_ERROR_MSG="Running an expression in the student process caused an issue."
DEFAULT_UNDEFINED_MSG="FMT:Have you defined `{name}` without errors?"
def has_expr(incorrect_msg=DEFAULT_INCORRECT_MSG,
             error_msg=DEFAULT_ERROR_MSG,
             undefined_msg=DEFAULT_UNDEFINED_MSG,
             extra_env=None,
             context_vals=None,
             pre_code=None,
             expr_code=None,
             name=None,
             highlight=None,
             copy=True,
             func=None,
             state=None,
             test=None):

    rep = Reporter.active_reporter

    # run function to highlight a block of code
    if callable(highlight):
        try:    highlight = highlight(state=state).student_tree
        except: pass
    highlight = highlight or state.highlight

    get_func = partial(evalCalls[test], 
                       extra_env = extra_env,
                       context_vals = context_vals,
                       pre_code = pre_code,
                       expr_code = expr_code,
                       name = name,
                       copy=copy,
                       do_exec = True if test == 'output' else False)
    
    eval_sol, str_sol = get_func(tree = state.solution_tree,
                                 process = state.solution_process,
                                 context = state.solution_context,
                                 env = state.solution_env)

    if (test == 'error') ^ isinstance(str_sol, Exception):
        raise ValueError("Evaluating expression raised error in solution process (or not an error if testing for one). "
                         "Error: {} - {}".format(type(str_sol), str_sol))
    if isinstance(eval_sol, ReprFail):
        raise ValueError("Couldn't figure out the value of a default argument: " + eval_sol.info)

    eval_stu, str_stu = get_func(tree = state.student_tree,
                                 process = state.student_process,
                                 context = state.student_context,
                                 env = state.student_env)

    # kwargs ---
    fmt_kwargs = {'stu_part': state.student_parts, 'sol_part': state.solution_parts, 
                  'name': name, 'test': test,
                  'extra_env': str(extra_env) if extra_env else "", 'context_vals': context_vals}
    fmt_kwargs['stu_eval'] = utils.shorten_str(str(eval_stu))
    fmt_kwargs['sol_eval'] = utils.shorten_str(str(eval_sol))

    # tests ---
    # error in process
    if (test == 'error') ^ isinstance(str_stu, Exception):
        _msg = state.build_message(error_msg, fmt_kwargs)
        feedback = Feedback(_msg, highlight)
        rep.do_test(Test(feedback))

    # name is undefined after running expression
    if isinstance(str_stu, UndefinedValue):
        _msg = state.build_message(undefined_msg, fmt_kwargs)
        rep.do_test(Test(Feedback(_msg, highlight)))

    # test equality of results
    _msg = state.build_message(incorrect_msg, fmt_kwargs)
    rep.do_test(EqualTest(eval_stu, eval_sol, Feedback(_msg, highlight), func))

    return state



args_string = """

    Args:
        incorrect_msg (str): feedback message if the {0} of the expression in the solution
          doesn't match the one of the student. This feedback message will be expanded if it is used
          in the context of another check function, like ``check_if_else``.
        error_msg (str): feedback message if there was an error when running the targeted student code.
          Note that when testing for an error, this message is displayed when none is raised.
        undefined_msg (str): feedback message if the ``name`` argument is defined, but a variable
          with that name doesn't exist after running the targeted student code.
        extra_env (dict): set variables to the extra environment. They will update the student and solution environment in
          the active state before the student/solution code in the active state is ran. This argument should contain a
          dictionary with the keys the names of the variables you want to set, and the values are the values of these variables.
          You can also use ``set_env()`` for this.
        context_vals (list): set variables which are bound in a ``for`` loop to certain values.
          This argument is only useful when checking a for loop (or list comprehensions).
          It contains a list with the values of the bound variables.
          You can also use ``set_context()`` for this.
        pre_code (str): the code in string form that should be executed before the expression is executed.
          This is the ideal place to set a random seed, for example.
        expr_code (str): if this argument is set, the expression in the student/solution code will not
          be ran. Instead, the given piece of code will be ran in the student as well as the solution environment
          and the result will be compared.
        name (str): If this is specified, the {1} of running this expression after running the focused expression
          is returned, instead of the {1} of the focussed expression in itself. This is typically used to inspect the
          {1} of an object after executing the body of e.g. a ``for`` loop.
        copy (bool): whether to try to deep copy objects in the environment, such as lists, that could
          accidentally be mutated. Disable to speed up SCTs. Disabling may lead to cryptic mutation issues.
        func: custom binary function of form f(stu_result, sol_result), for equality testing.
    """

has_equal_value =  partial(has_expr, test = 'value')
has_equal_value.__doc__ = """Run targeted student and solution code, and compare returned value.

    When called on an SCT chain, ``has_equal_value()`` will execute the student and solution
    code that is 'zoomed in on' and compare the returned values.
    """ + args_string.format("returned value", "value") + """
    :Example:

        Student code and solution code::

            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])
            np.mean(arr)

        SCT::

            # Verify equality of arr:
            Ex().check_object('arr').has_equal_value()

            # Verify whether arr was correctly set in np.mean
            Ex().check_function('numpy.mean').check_args('a').has_equal_value()

            # Verify whether np.mean(arr) produced the same result
            Ex().check_function('numpy.mean').has_equal_value()

    """


has_equal_output = partial(has_expr, test = 'output')
has_equal_output.__doc__ = """Run targeted student and solution code, and compare output.

    When called on an SCT chain, ``has_equal_output()`` will execute the student and solution
    code that is 'zoomed in on' and compare the output.
    """ + args_string.format("output", "output")

has_equal_error  = partial(has_expr, test = 'error')
has_equal_error.__doc__ = """Run targeted student and solution code, and compare generated errors.

    When called on an SCT chain, ``has_equal_error()`` will execute the student and solution
    code that is 'zoomed in on' and compare the errors that they generate.
    """ + args_string.format("error", "error")
