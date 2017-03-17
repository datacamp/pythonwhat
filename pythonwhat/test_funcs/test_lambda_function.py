from pythonwhat.Reporter import Reporter
from .test_function_definition import test_args
from pythonwhat.utils import get_ord
from pythonwhat.check_funcs import check_node, multi, check_part, call
from functools import partial

MSG_MISSING = "FMT:The system wants to check {typestr} you defined but hasn't found it."
MSG_PREPEND = "FMT:Check your definition of {typestr}. "
MSG_PREPEND_ARG = "FMT:In your definition of {typestr}, "

MSG_RES_ERROR = "FMT:Calling it with arguments `{argstr}` should result in `{str_sol}`, instead got an error."
MSG_RES_INCORRECT = "FMT:Calling it with arguments `{argstr}` should result in `{str_sol}`, instead got `{str_stu}`."
MSG_ERR_WRONG = "FMT:Calling it with arguments `{argstr}` doesn't result in an error, but it should."
def test_lambda_function(index,
                         arg_names=True,
                         arg_defaults=True,
                         body=None,
                         results=[],
                         errors=[],
                         not_called_msg=None,
                         nb_args_msg=None,
                         arg_names_msg=None,
                         arg_defaults_msg=None,
                         wrong_result_msg=None,
                         no_error_msg=None,
                         expand_message=True,
                         state=None):
    """Test a lambda function definition.

    This function helps you test a lambda function definition. Generally four things can be tested:
        1) The argument names of the function (including if the correct defaults are used)
        2) The body of the functions (does it output correctly, are the correct functions used)
        3) The return value with a certain input
        4) Whether certain inputs generate an error

    Custom feedback messages can be set for all these parts, default messages are generated
    automatically if none are set.

    Args:
        index (int): the number of the lambda function you want to test.
        arg_names (bool): if True, the argument names will be tested, if False they won't be tested. Defaults
            to True.
        arg_defaults (bool): if True, the default values of the arguments will be tested, if False they won't
            be tested. Defaults to True.
        body: this arguments holds the part of the code that will be ran to check the body of the function
            definition. It should be passed as a lambda expression or a function. The functions that are
            ran should be other pythonwhat test functions, and they will be tested specifically on only the
            body of the for loop. Defaults to None.
        results (list(str)): a list of strings representing function calls to the lam function. The lam
            function will be replaced by the actual lambda function from the student and solution code. The result
            of calling the lambda function will be compared between student and solution.
        errors (list(str)): a list of strings representing function calls to the lam function. The lam
            function will be replaced by the actual lambda function from the student and solution code. It will be
            checked if an error is generated appropriately for the specified inputs.
        not_called_msg (str): message if the function is not defined.
        nb_args_msg (str): message if the number of arguments do not matched.
        arg_names_msg (str): message if the argument names do not match.
        arg_defaults_msg (str): message if the argument default values do not match.
        wrong_result_msg (str): message if one of the tested function calls' result did not match.
        no_error_msg (str): message if one of the tested function calls' result did not generate an error.
        expand_message (bool): only relevant if there is a body test. If True, feedback messages defined in the
            body test will be preceded by 'In your definition of ___, '. If False, :code:`test_function_definition()`
            will generate no extra feedback if the body test fails. Defaults to True.
    """

    rep = Reporter.active_reporter

    # what the lambda will be referred to as
    typestr = "the {} lambda function".format(get_ord(index))
    get_func_child = partial(check_node, 'lambda_functions', index-1, typestr, not_called_msg or MSG_MISSING, state=state)
    child = get_func_child(expand_msg = MSG_PREPEND if expand_message else "")

    # make a temporary child states, to reflect that there were two types of 
    # messages prepended in the original function
    quiet_child = get_func_child(expand_msg = "")
    prep_child2 = get_func_child(expand_msg =  MSG_PREPEND_ARG if expand_message else "")

    test_args(arg_names, arg_defaults, 
              nb_args_msg, arg_names_msg, arg_defaults_msg, 
              prep_child2, quiet_child)

    multi(body, state=check_part('body', "", child))

    # Test function calls -----------------------------------------------------

    student_fun  = state.student_lambda_functions[index-1]['node']
    solution_fun = state.solution_lambda_functions[index-1]['node']

    for el in results:
        argstr = el.replace('lam', '')
        call(el, 
             incorrect_msg = wrong_result_msg or MSG_RES_INCORRECT, 
             error_msg = wrong_result_msg or MSG_RES_ERROR,
             argstr = argstr,
             state = child)

    for el in errors:
        argstr = el.replace('lam', '')
        call(el, 'error',
             incorrect_msg = no_error_msg or MSG_ERR_WRONG, 
             error_msg = no_error_msg or MSG_ERR_WRONG,
             argstr = argstr,
             state = child)
