import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedCollTest, EqualTest, Test, InstanceTest
from pythonwhat.Feedback import Feedback
from pythonwhat import utils
from pythonwhat.utils import get_ord
from pythonwhat.tasks import getFunctionCallResultInProcess, getFunctionCallOutputInProcess, getFunctionCallErrorInProcess, ReprFail
from pythonwhat.check_funcs import check_node, check_part, check_part_index, multi, has_part, has_equal_part_len, has_equal_part, has_equal_value

from functools import partial

MSG_MISSING = "You didn't define the following function: {typestr}."
MSG_PREPEND = "Check your definition of {typestr}. "

MSG_NUM_ARGS = "You should define {parent[typestr]} with {sol_len} arguments, instead got {stu_len}."

MSG_PREPEND_ARG = "In your definition of {typestr}, " 
MSG_BAD_ARG_NAME = "the {parent[ordinal]} {parent[part]} should be called `{sol_part[name]}`, instead got `{stu_part[name]}`."
MSG_BAD_DEFAULT = "the {parent[part]} `{stu_part[name]}` should have no default."
MSG_INC_DEFAULT = "the {parent[part]} `{stu_part[name]}` does not have the correct default."

MSG_NO_VARARG = "have you specified an argument to take a `*` argument and named it `{sol_part[vararg][name]}`?"
MSG_NO_KWARGS = "have you specified an argument to take a `**` argument and named it `{sol_part[kwarg][name]}`?"
MSG_VARARG_NAME = "have you specified an argument to take a `*` argument and named it `{sol_part[name]}`?"
MSG_KWARG_NAME = "have you specified an argument to take a `**` argument and named it `{sol_part[name]}`?"


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
    rep.set_tag("fun", "test_function_definition")

    # what the function will be referred to as
    typestr = "`{}()`".format(name)
    get_func_child = partial(check_node, 'function_defs', name, typestr, not_called_msg or MSG_MISSING, state=state)
    child =  get_func_child(expand_msg = MSG_PREPEND if expand_message else "")

    # make a temporary child state, to reflect that there were two types of 
    # messages prepended in the original function
    quiet_child = get_func_child(expand_msg = "")
    prep_child2 = get_func_child(expand_msg = MSG_PREPEND_ARG)

    test_args(arg_names, arg_defaults, 
              nb_args_msg, arg_names_msg, arg_defaults_msg,
              prep_child2, quiet_child)

    multi(body, state=check_part('body', "", child))

    # TODO: refactor below ----------------------------------------------------
    #
    solution_defs = state.solution_function_defs
    student_defs = state.student_function_defs

    solution_def = solution_defs[name]
    student_def = student_defs[name]

    fun_def = student_def['node']
    fun_name = ("`%s()`" % name)


    if results is not None:
        for el in results:
            el = fix_format(el)
            call_str = name + stringify(el)

            eval_solution, str_solution = getFunctionCallResultInProcess(process = state.solution_process,
                                                                         fun_name = name,
                                                                         arguments = el)
            if str_solution is None:
                raise ValueError("Calling %s in the solution process resulted in an error" % call_str)
            if isinstance(eval_solution, ReprFail):
                raise ValueError("Something went wrong in figuring out the result of " + call_str + ": " + eval_solution.info)

            eval_student, str_student = getFunctionCallResultInProcess(process = state.student_process,
                                                                       fun_name = name,
                                                                       arguments = el)

            if str_student is None:
                c_wrong_result_msg = wrong_result_msg or \
                    ("Calling `%s` should result in `%s`, instead got an error." %
                        (call_str, str_solution))
                rep.do_test(Test(c_wrong_result_msg))
                return

            c_wrong_result_msg = wrong_result_msg or \
                ("Calling `%s` should result in `%s`, instead got `%s`." %
                    (call_str, str_solution, str_student))
            rep.do_test(EqualTest(eval_solution, eval_student, c_wrong_result_msg))

    if outputs is not None:
        for el in outputs:
            el = fix_format(el)
            call_str = name + stringify(el)
            output_solution = getFunctionCallOutputInProcess(process = state.solution_process,
                                                             fun_name = name,
                                                             arguments = el)

            if output_solution is None:
                raise ValueError("Calling %s in the solution process resulted in an error" % call_str)

            output_student = getFunctionCallOutputInProcess(process = state.student_process,
                                                            fun_name = name,
                                                            arguments = el)

            def format_output(out):
                if len(out) == 0:
                    return "no output"
                else:
                    return "`%s`" % out

            if output_student is None:
                c_wrong_output_msg = wrong_output_msg or \
                    ("Calling `%s` should output %s, instead got an error." %
                        (call_str, format_output(output_solution)))
                rep.do_test(Test(c_wrong_output_msg))
                return

            c_wrong_output_msg = wrong_output_msg or \
                ("Calling `%s` should output %s, instead got %s." %
                    (call_str, format_output(output_solution), format_output(output_student)))
            rep.do_test(EqualTest(output_solution, output_student, c_wrong_output_msg))

    if errors is not None:
        for el in errors:
            el = fix_format(el)
            call_str = name + stringify(el)
            error_solution = getFunctionCallErrorInProcess(process = state.solution_process,
                                                           fun_name = name,
                                                           arguments = el)

            if error_solution is None:
                raise ValueError("Calling %s did not generate an error in the solution environment." % call_str)

            error_student = getFunctionCallErrorInProcess(process = state.student_process,
                                                          fun_name = name,
                                                          arguments = el)

            if error_student is None:
                feedback_msg = no_error_msg or ("Calling `%s` doesn't result in an error, but it should!" % call_str)
                rep.do_test(Test(feedback_msg))
                return

            feedback_msg = wrong_error_msg or ("Calling `%s` should result in a `%s`, instead got a `%s`." % \
                (call_str, error_solution.__class__.__name__, error_student.__class__.__name__))
            rep.do_test(InstanceTest(error_student, error_solution.__class__, feedback_msg))


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

def test_args(arg_names, arg_defaults, 
              nb_args_msg, arg_names_msg, arg_defaults_msg, 
              child, quiet_child):
    if arg_names or arg_defaults:
        # test number of args
        has_equal_part_len('arg', nb_args_msg or MSG_NUM_ARGS, state=quiet_child)

        # iterate over each arg, testing name and default
        for ii in range(len(child.solution_parts['arg'])):
            # get argument state
            arg_state = check_part_index('arg', ii, 'argument', "NO MISSING MSG", state=child)
            # test exact name
            has_equal_part('name', arg_names_msg or MSG_BAD_ARG_NAME, arg_state)

            if arg_defaults:
                # test whether is default
                has_equal_part('is_default', arg_defaults_msg or MSG_BAD_DEFAULT, arg_state)
                # test default value, use if to prevent running a process no default
                if arg_state.solution_parts['is_default']:
                    has_equal_value(arg_defaults_msg or MSG_INC_DEFAULT, arg_state)

        # test *args and **kwargs
        if child.solution_parts['vararg']:
            vararg = check_part('vararg', "", missing_msg = MSG_NO_VARARG, state = child)
            has_equal_part('name', MSG_VARARG_NAME, vararg)
        
        if child.solution_parts['kwarg']:
            kwarg = check_part('kwarg', "", missing_msg = MSG_NO_KWARGS, state = child)
            has_equal_part('name', MSG_KWARG_NAME, kwarg)

