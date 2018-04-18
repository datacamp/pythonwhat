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
        return state.to_child_state(stu_part['node'], sol_part['node'],
                                    stu_part.get('target_vars'), sol_part.get('target_vars'),
                                    stu_part, sol_part,
                                    highlight = stu_part.get('highlight'),
                                    append_message = append_message, node_name=node_name)

    # otherwise, assume they are just nodes
    return state.to_child_state(stu_part, sol_part, append_message = append_message)


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
def check_node(name, index, typestr, missing_msg=MSG_MISSING, expand_msg=MSG_PREPEND, state=None):
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
        rep.failed_test = False          # protect against old behavior
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
    # set up context in processes
    solution_res = setUpNewEnvInProcess(process = state.solution_process,
                                        context = state.solution_parts['with_items'])
    if isinstance(solution_res, Exception):
        raise Exception("error in the solution, running test_with(): %s" % str(solution_res))

    student_res = setUpNewEnvInProcess(process = state.student_process,
                                       context = state.student_parts['with_items'])
    if isinstance(student_res, AttributeError):
        rep.do_test(Test(Feedback("In your %s `with` statement, you're not using a correct context manager." % (get_ord(index)), child.highlight)))

    if isinstance(student_res, (AssertionError, ValueError, TypeError)):
        rep.do_test(Test(Feedback("In your %s `with` statement, the number of values in your context manager " + \
            "doesn't correspond to the number of variables you're trying to assign it to." % (get_ord(index)), child.highlight)))

    # run subtests
    try:
        multi(*args, state=state)
    finally:
        # exit context
        if breakDownNewEnvInProcess(process = state.solution_process):
            raise Exception("error in the solution, closing the %s with fails with: %s" %
                (get_ord(index), close_solution_context))

        if breakDownNewEnvInProcess(process = state.student_process):

            rep.do_test(Test(Feedback("Your %s `with` statement can not be closed off correctly, you're " + \
                            "not using the context manager correctly." % (get_ord(index)), state.highlight)),
                        fallback_ast = state.highlight)
    return state

def set_context(*args, state=None, **kwargs):
    """Update context values for student and solution environments.
    
    Note that excess args and unmatched kwargs will be unused in the student environment.
    If an argument is specified both by name and position args, will use named arg.
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

    return state.to_child_state(student_subtree = None, solution_subtree = None,
                                student_context = out_stu, solution_context = out_sol)


def check_args(name, missing_msg='FMT:Are you sure it is defined?', state=None):
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
    rep = Reporter.active_reporter
    test_type = ('value', 'output', 'error')

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

def has_expr(incorrect_msg="__JINJA__:Unexpected expression {{test}}: expected `{{sol_eval}}`, got `{{stu_eval}}`{{' with values ' + extra_env if extra_env}}.",
             error_msg="Running an expression in the student process caused an issue.",
             undefined_msg="FMT:Have you defined `{name}` without errors?",
             extra_env=None,
             context_vals=None,
             expr_code=None,
             pre_code=None,
             keep_objs_in_env=None,
             name=None,
             highlight=None,
             copy=True,
             func=None,
             state=None,
             test=None):
    """Run student and solution code, compare returned value, printed output, or errors.

    Args:
        incorrect_msg (str): feedback message if the output of the expression in the solution doesn't match
          the one of the student. This feedback message will be expanded if it is used in the context of
          another test function, like test_if_else.
        error_msg (str): feedback message if there was an error when running the student code.
          Note that when testing for an error, this message is displayed when none is raised.
        undefined_msg (str): feedback message if the name argument is defined, but a variable 
          with that name doesn't exist after running the student code.
        extra_env (dict): set variables to the extra environment. They will update the student
          and solution environment in the active state before the student/solution code in the active
          state is ran. This argument should contain a dictionary with the keys the names of
          the variables you want to set, and the values are the values of these variables.
        context_vals (list): set variables which are bound in a for loop to certain values. This argument is
          only useful if you use the function in a test_for_loop. It contains a list with the values
          of the bound variables.
        expr_code (str): if this variable is not None, the expression in the student/solution code will not
          be ran. Instead, the given piece of code will be ran in the student as well as the solution environment
          and the result will be compared.
        pre_code (str): the code in string form that should be executed before the expression is executed.
          This is the ideal place to set a random seed, for example.
        keep_obj_in_env (list()): a list of variable names that should be hold in the copied environment where
          the expression is evaluated. All primitive types are copied automatically, other objects have to
          be passed explicitely.
        name (str): the name of a variable, or expression, whose value will be tested after running the
          student and solution code. This could be thought of as post code.
        copy (bool): whether to try to deep copy objects in the environment, such as lists, that could
          accidentally be mutated. Disable to speed up SCTs. Disabling may lead to cryptic mutation issues.
        func: custom binary function of form f(stu_result, sol_result), for equality testing.
    """
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
                       keep_objs_in_env = keep_objs_in_env,
                       name=name,
                       copy=copy,
                       do_exec = True if test == 'output' else False)
    
    eval_sol, str_sol = get_func(tree = state.solution_tree,
                                 process = state.solution_process,
                                 context = state.solution_context)

    if (test == 'error') ^ isinstance(str_sol, Exception):
        raise ValueError("evaluating expression raised error in solution process (or not an error if testing for one). "
                         "Error: %s - %s"%(type(str_sol), str_sol))
    if isinstance(eval_sol, ReprFail):
        raise ValueError("Couldn't figure out the value of a default argument: " + eval_sol.info)

    eval_stu, str_stu = get_func(tree = state.student_tree,
                                 process = state.student_process,
                                 context = state.student_context)

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

has_equal_value =  partial(has_expr, test = 'value')
has_equal_output = partial(has_expr, test = 'output')
has_equal_error  = partial(has_expr, test = 'error')
