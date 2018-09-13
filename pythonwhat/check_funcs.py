from pythonwhat.tasks import getResultInProcess, getOutputInProcess, getErrorInProcess, ReprFail, setUpNewEnvInProcess, breakDownNewEnvInProcess
from pythonwhat.has_funcs import has_part
from pythonwhat.check_logic import multi
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test, EqualTest, TestFail
from pythonwhat.Feedback import Feedback, InstructorError
from pythonwhat.utils import get_ord
from pythonwhat.utils_ast import assert_ast
from functools import partial
import ast
from jinja2 import Template

def render(template, kwargs):
    return Template(template).render(**kwargs)

class StubState():
    def __init__(self, highlight, highlighting_disabled):
        self.highlight = highlight
        self.highlighting_disabled = highlighting_disabled

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
                                append_message=append_message,
                                node_name=node_name)

def check_part(name, part_msg,
               missing_msg=None,
               expand_msg=None,
               state=None):
    """Return child state with name part as its ast tree"""

    if missing_msg is None: missing_msg = "Are you sure you defined the {{part}}? "
    if expand_msg is None: expand_msg = "Did you correctly specify the {{part}}? "

    if not part_msg: part_msg = name
    append_message = {'msg': expand_msg, 'kwargs': { 'part': part_msg }}

    has_part(name, missing_msg, state, append_message['kwargs'])
    
    stu_part = state.student_parts[name]
    sol_part = state.solution_parts[name]

    assert_ast(state, sol_part, append_message['kwargs'])

    return part_to_child(stu_part, sol_part, append_message, state)

def check_part_index(name, index, part_msg,
                     missing_msg=None,
                     expand_msg=None,
                     state=None):
    """Return child state with indexed name part as its ast tree.

    ``index`` can be:

    - an integer, in which case the student/solution_parts are indexed by position.
    - a string, in which case the student/solution_parts are expected to be a dictionary.
    - a list of indices (which can be integer or string), in which case the student parts are indexed step by step.
    """

    if missing_msg is None: missing_msg = "Are you sure you defined the {{part}}? "
    if expand_msg is None: expand_msg = "Did you correctly specify the {{part}}? "

    # create message
    ordinal = get_ord(index+1) if isinstance(index, int) else ""
    fmt_kwargs = {
        'index': index,
        'ordinal': ordinal
    }
    fmt_kwargs.update(part = render(part_msg, fmt_kwargs))

    append_message = {
        'msg': expand_msg,
        'kwargs': fmt_kwargs
    }

    # check there are enough parts for index
    has_part(name, missing_msg, state, fmt_kwargs, index)

    # get part at index
    stu_part = state.student_parts[name]
    sol_part = state.solution_parts[name]

    if isinstance(index, list):
        for ind in index:
            stu_part = stu_part[ind]
            sol_part = sol_part[ind]
    else:
        stu_part = stu_part[index]
        sol_part = sol_part[index]

    assert_ast(state, sol_part, fmt_kwargs)

    # return child state from part
    return part_to_child(stu_part, sol_part, append_message, state)

def check_node(name,
               index=0,
               typestr='{{ordinal}} node',
               missing_msg=None,
               expand_msg=None,
               state=None):

    if missing_msg is None: missing_msg = "The system wants to check the {{typestr}} but hasn't found it."
    if expand_msg is None: expand_msg = "Check the {{typestr}}. "

    rep = Reporter.active_reporter
    stu_out = getattr(state, 'student_'+name)
    sol_out = getattr(state, 'solution_'+name)

    # check if there are enough nodes for index
    fmt_kwargs = {
        'ordinal': get_ord(index+1) if isinstance(index, int) else "",
        'index': index,
        'name': name
    }
    fmt_kwargs['typestr'] = render(typestr, fmt_kwargs)

    # test if node can be indexed succesfully
    try: stu_out[index]
    except (KeyError, IndexError):                  # TODO comment errors
        _msg = state.build_message(missing_msg, fmt_kwargs)
        rep.do_test(Test(Feedback(_msg, state)))

    # get node at index
    stu_part = stu_out[index]
    sol_part = sol_out[index]

    append_message = {
        'msg': expand_msg,
        'kwargs': fmt_kwargs
    }

    return part_to_child(stu_part, sol_part, append_message, state, node_name=name)
    
# context functions -----------------------------------------------------------

def with_context(*args, state=None):

    rep = Reporter.active_reporter

    # set up context in processes
    solution_res = setUpNewEnvInProcess(process = state.solution_process,
                                        context = state.solution_parts['with_items'])
    if isinstance(solution_res, Exception):
        raise InstructorError("error in the solution, running test_with(): %s" % str(solution_res))

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
            raise InstructorError("error in the solution, closing the `with` fails with: %s" % (close_solution_context))

        if breakDownNewEnvInProcess(process = state.student_process):

            rep.do_test(Test(Feedback("Your `with` statement can not be closed off correctly, you're " + \
                            "not using the context manager correctly.", state)))
    return state

def check_args(name, missing_msg=None, state=None):
    """Check whether a function argument is specified.

    This function can follow ``check_function()`` in an SCT chain and verifies whether an argument is specified.
    If you want to go on and check whether the argument was correctly specified, you can can continue chaining with
    ``has_equal_value()`` (value-based check) or ``has_equal_ast()`` (AST-based check)

    This function can also follow ``check_function_def()`` or ``check_lambda_function()`` to see if arguments have been
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
                check_args('x') # will fail if student used y as arg
                check_args(0)   # will still pass if student used y as arg
            )

    """
    if missing_msg is None:
        missing_msg = 'Did you specify the {{part}}?'

    if name in ['*args', '**kwargs']: # for check_function_def
        return check_part(name, name, state=state, missing_msg = missing_msg)
    else:
        if isinstance(name, list): # dealing with args or kwargs
            if name[0] == 'args':
                arg_str = "%s argument passed as a variable length argument"%get_ord(name[1]+1)
            else:
                arg_str = "argument `%s`"%name[1]
        else:
            arg_str = "%s argument" % get_ord(name+1) if isinstance(name, int) else "argument `%s`" % name
        return check_part_index('args', name, arg_str, missing_msg = missing_msg, state=state)


# CALL CHECK ==================================================================

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

def stringify(arguments):
    vararg = str(arguments['args'])[1:-1]
    kwarg = ', '.join(['%s = %s' % (key, value) for key, value in arguments['kwargs'].items()])
    if len(vararg) == 0:
        if len(kwarg) == 0:
            return "()"
        else:
            return "(" + kwarg + ")"
    else :
        if len(kwarg) == 0:
            return "(" + vararg + ")"
        else :
            return "(" + ", ".join([vararg, kwarg]) + ")"

# TODO: test string syntax with check_function_def
#       test argument syntax with check_lambda_function
def run_call(args, node, process, get_func, **kwargs):
    # Get function expression
    if isinstance(node, ast.FunctionDef):                     # function name
        func_expr = ast.Name(id=node.name, ctx=ast.Load())
    elif isinstance(node, ast.Lambda):                        # lambda body expr
        func_expr = node
    else: raise InstructorError("Only function definition or lambda may be called")

    ast.fix_missing_locations(func_expr)
    return get_func(process = process, tree=func_expr, call = args, **kwargs)

MSG_CALL_INCORRECT = "Calling {{argstr}} should {{action}} `{{str_sol}}`, instead got {{str_stu if str_stu == 'no printouts' else '`' + str_stu + '`'}}."
MSG_CALL_ERROR     = "Calling {{argstr}} should {{action}} `{{str_sol}}`, instead it errored out: `{{str_stu}}`."
MSG_CALL_ERROR_INV = "Calling {{argstr}} should {{action}} `{{str_sol}}`, instead got `{{str_stu}}`."
def call(args,
         test='value',
         incorrect_msg=None,
         error_msg=None,
         argstr=None,
         func=None,
         state=None, **kwargs):
    """Use ``check_call()`` in combination with ``has_equal_x()`` instead.
    """

    if incorrect_msg is None:
        incorrect_msg = MSG_CALL_INCORRECT
    if error_msg is None:
        error_msg = MSG_CALL_ERROR_INV if test == 'error' else MSG_CALL_ERROR

    rep = Reporter.active_reporter

    assert test in ('value', 'output', 'error')

    get_func = evalCalls[test]

    # Run for Solution --------------------------------------------------------
    eval_sol, str_sol = run_call(args, state.solution_parts['node'], state.solution_process, get_func, **kwargs)

    if (test == 'error') ^ isinstance(eval_sol, Exception):
        _msg = state.build_message("Calling {{argstr}} resulted in an error (or not an error if testing for one). Error message: {{type_err}} {{str_sol}}",
                                   dict(type_err=type(eval_sol), str_sol=str_sol, argstr=argstr)),
        raise InstructorError(_msg)

    if isinstance(eval_sol, ReprFail):
        _msg = state.build_message("Can't get the result of calling {{argstr}}: {{eval_sol.info}}",
                                   dict(argstr = argstr, eval_sol=eval_sol))
        raise InstructorError(_msg)

    # Run for Submission ------------------------------------------------------
    eval_stu, str_stu = run_call(args, state.student_parts['node'], state.student_process, get_func, **kwargs)
    action_strs = {'value': 'return', 'output': 'print out', 'error': 'error out with the message'}
    fmt_kwargs = {'part': argstr, 'argstr': argstr, 'str_sol': str_sol, 'str_stu': str_stu, 'action': action_strs[test]}

    # either error test and no error, or vice-versa
    stu_node = state.student_parts['node']
    stu_state = StubState(stu_node, state.highlighting_disabled)
    if (test == 'error') ^ isinstance(eval_stu, Exception):
        _msg = state.build_message(error_msg, fmt_kwargs)
        rep.do_test(Test(Feedback(_msg, stu_state)))

    # incorrect result
    _msg = state.build_message(incorrect_msg, fmt_kwargs)
    rep.do_test(EqualTest(eval_sol, eval_stu, Feedback(_msg, stu_state), func))

    return state

def build_call(callstr, node):
    if isinstance(node, ast.FunctionDef): # function name
        func_expr = ast.Name(id=node.name, ctx=ast.Load())
        argstr = "`%s`" % callstr.replace('f', node.name)
    elif isinstance(node, ast.Lambda): # lambda body expr
        func_expr = node
        argstr = 'it with the arguments `%s`' % callstr.replace('f', '')
    else:
        raise TypeError("Can't handle AST that is passed.")

    parsed = ast.parse(callstr).body[0].value
    parsed.func = func_expr
    ast.fix_missing_locations(parsed)
    return parsed, argstr

def check_call(callstr, argstr = None, expand_msg=None, state=None):
    """When checking a function definition of lambda function,
    prepare has_equal_x for checking the call of a user-defined function.

    Args:
        callstr (str): call string that specifies how the function should be called, e.g. `f(1, a = 2)`.
           ``check_call()`` will replace ``f`` with the function/lambda you're targeting.
        argstr (str): If specified, this overrides the way the function call is refered to in the expand message.
        expand_msg (str): If specified, this overrides the expand message.
        state (State): state object that is chained from.

    :Example:

        Student and solution code::

            def my_power(x):
                print("calculating sqrt...")
                return(x * x)

        SCT::

            Ex().check_function_def('my_power').multi(
                check_call("f(3)").has_equal_value()
                check_call("f(3)").has_equal_output()
            )
    """

    state.assert_is(
        ['function_defs', 'lambda_functions'],
        'check_call',
        ['check_function_def', 'check_lambda_function']
    )

    if expand_msg is None:
        expand_msg = "To verify it, we reran {{argstr}}. "

    stu_part, _argstr = build_call(callstr, state.student_parts['node'])
    sol_part, _ = build_call(callstr, state.solution_parts['node'])

    append_message = { 'msg': expand_msg, 'kwargs': {'argstr': argstr or _argstr }}
    child = part_to_child(stu_part, sol_part, append_message, state)

    return child