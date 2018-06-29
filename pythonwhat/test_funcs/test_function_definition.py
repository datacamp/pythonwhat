from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import check_node, check_part, check_part_index, multi, has_equal_part_len, has_equal_part, has_equal_value, call, fix_format, stringify

from functools import partial

MSG_MISSING = "FMT:You didn't define the following function: {typestr}."
MSG_PREPEND = "FMT:Check your definition of {typestr}. "

MSG_NUM_ARGS = "FMT:You should define {parent[typestr]} with {sol_len} arguments, instead got {stu_len}."

MSG_BAD_ARG_NAME = "FMT:The {parent[ordinal]} {parent[part]} should be called `{sol_part[name]}`, instead got `{stu_part[name]}`."
MSG_BAD_DEFAULT = "FMT:The {parent[part]} `{stu_part[name]}` should have no default."
MSG_INC_DEFAULT = "FMT:The {parent[part]} `{stu_part[name]}` does not have the correct default."

MSG_NO_VARARG = "FMT:Have you specified an argument to take a `*` argument and named it `{sol_part[*args][name]}`?"
MSG_NO_KWARGS = "FMT:Have you specified an argument to take a `**` argument and named it `{sol_part[**kwargs][name]}`?"
MSG_VARARG_NAME = "FMT:Have you specified an argument to take a `*` argument and named it `{sol_part[name]}`?"
MSG_KWARG_NAME = "FMT:Have you specified an argument to take a `**` argument and named it `{sol_part[name]}`?"

def test_function_definition(name,
                             arg_names=True,
                             arg_defaults=True,
                             body=None,
                             results=None,
                             outputs=None,
                             errors=None,
                             not_called_msg=None,
                             nb_args_msg=None,
                             other_args_msg=None,
                             arg_names_msg=None,
                             arg_defaults_msg=None,
                             wrong_result_msg=None,
                             wrong_output_msg=None,
                             no_error_msg=None,
                             wrong_error_msg=None,
                             expand_message=True,
                             state=None):
    """Test a function definition.

    This function helps you test a function definition. Generally four things can be tested:
        1) The argument names of the function (including if the correct defaults are used)
        2) The body of the functions (does it output correctly, are the correct functions used)
        3) The return value with a certain input
        4) The output value with a certain input
        5) Whether certain inputs generate an error and what type of error

    Custom feedback messages can be set for all these parts, default messages are generated
    automatically if none are set.

    Args:
        name (str): the name of the function definition to be tested.
        arg_names (bool): if True, the argument names will be tested, if False they won't be tested. Defaults
            to True.
        arg_defaults (bool): if True, the default values of the arguments will be tested, if False they won't
            be tested. Defaults to True.
        body: this arguments holds the part of the code that will be ran to check the body of the function
            definition. It should be passed as a lambda expression or a function. The functions that are
            ran should be other pythonwhat test functions, and they will be tested specifically on only the
            body of the for loop. Defaults to None.
        results (list(list)): a list of lists representing arguments that should be passed to the defined
            function. These arguments are passed to the function in the student environment and the solution
            environment, the results (what's returned) are compared.
        outputs (list(list)): a list of lists representing arguments that should be passed to the defined
            function. These arguments are passed to the function in the student environment and the solution
            environment, the outpus are compared.
        errors (list(list)): a list of lists representing arguments that should be passed to the defined
            function. These arguments are passed to the function in the student environment and the solution
            environment, the errors they generate are compared.
        not_called_msg (str): message if the function is not defined.
        nb_args_msg (str): message if the number of arguments do not matched.
        arg_names_msg (str): message if the argument names do not match.
        arg_defaults_msg (str): message if the argument default values do not match.
        wrong_result_msg (str): message if one of the tested function calls' result did not match.
        wrong_output_msg (str): message if one of the tested functions calls' output did not match.
        no_error_msg (str): message if one of the tested function calls' result did not generate an error.
        wrong_error_msg (str): message if the error that one of the tested function calls generated did not match.
        expand_message (bool): only relevant if there is a body test. If True, feedback messages defined in the
            body test will be preceded by 'In your definition of ___, '. If False, `test_function_definition()`
            will generate no extra feedback if the body test fails. Defaults to True.

    :Example:

        Student code::

            def shout( word, times = 3):
                shout_word = not_word + '???'
                print( shout_word )
                return word * times

        Solution code::

            def shout( word = 'help', times = 3 ):
                shout_word = word + '!!!'
                print( shout_word )
                return word * times

        SCT::

            test_function_definition('shout')                          # fail
            test_function_definition('shout', arg_defaults = False)    # pass
            test_function_definition('shout', arg_defaults = False,    # fail
                                            outputs = [('help')])    

            test_function_definition('shout', arg_defaults = False,    # pass
                                            results = [('help', 2)]) 

            test_function_definition('shout', args_defaults = False    # pass
                    body = test_function('print', args = []]))
    """
    rep = Reporter.active_reporter

    # what the function will be referred to as
    typestr = "`{}()`".format(name)
    get_func_child = partial(check_node, 'function_defs', name, typestr, not_called_msg or MSG_MISSING, state=state)
    child =  get_func_child(expand_msg = MSG_PREPEND if expand_message else "")

    # make a temporary child state, to reflect that there were two types of 
    # messages prepended in the original function
    quiet_child = get_func_child(expand_msg = "")
    prep_child2 = get_func_child(expand_msg = MSG_PREPEND)

    test_args(arg_names, arg_defaults, 
              nb_args_msg, arg_names_msg, arg_defaults_msg,
              prep_child2, quiet_child)

    multi(body, state=check_part('body', "", expand_msg=None if expand_message else "", state=child))

    # Test function calls -----------------------------------------------------

    #fun_name = ("`%s()`" % name)

    for el in (results or []):
        el = fix_format(el)
        call(el, 'value',
                incorrect_msg = wrong_result_msg,
                error_msg = wrong_result_msg,
                argstr = '`{}{}`'.format(name, stringify(el)),
                state = quiet_child)

    for el in (outputs or []):
        el = fix_format(el)
        call(el, 'output',
                incorrect_msg = wrong_output_msg,
                error_msg = wrong_output_msg,
                argstr = '`{}{}`'.format(name, stringify(el)),
                state = quiet_child)

    for el in (errors or []):
        el = fix_format(el)
        call(el, 'error',
                incorrect_msg = wrong_error_msg,
                error_msg = no_error_msg,
                argstr = '`{}{}`'.format(name, stringify(el)),
                state = quiet_child)


def test_args(arg_names, arg_defaults, 
              nb_args_msg, arg_names_msg, arg_defaults_msg, 
              child, quiet_child):
    if arg_names or arg_defaults:
        # test number of args
        has_equal_part_len('_spec1_args', nb_args_msg or MSG_NUM_ARGS, state=quiet_child)

        # iterate over each arg, testing name and default
        for ii in range(len(child.solution_parts['_spec1_args'])):
            # get argument state
            arg_state = check_part_index('_spec1_args', ii, 'argument', "NO MISSING MSG", expand_msg="", state=child)
            # test exact name
            has_equal_part('name', arg_names_msg or MSG_BAD_ARG_NAME, arg_state)

            if arg_defaults:
                # test whether is default
                has_equal_part('is_default', arg_defaults_msg or MSG_BAD_DEFAULT, arg_state)
                # test default value, use if to prevent running a process no default
                if arg_state.solution_parts['is_default']:
                    has_equal_value(incorrect_msg = arg_defaults_msg or MSG_INC_DEFAULT, error_msg="error message", append=True, state=arg_state)

        # test *args and **kwargs
        if child.solution_parts['*args']:
            vararg = check_part('*args', "", missing_msg=MSG_NO_VARARG, expand_msg="", state=child)
            has_equal_part('name', MSG_VARARG_NAME, state=vararg)
        
        if child.solution_parts['**kwargs']:
            kwarg = check_part('**kwargs', "", missing_msg=MSG_NO_KWARGS, expand_msg="", state=child)
            has_equal_part('name', MSG_KWARG_NAME, state=kwarg)

