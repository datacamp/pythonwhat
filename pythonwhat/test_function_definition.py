import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedTest, EqualTest, Test
from pythonwhat.Feedback import Feedback
from pythonwhat import utils

from contextlib import contextmanager

ordinal = lambda n: "%d%s" % (
    n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])

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

def test_function_definition(name,
                             arg_names=True,
                             arg_defaults=True,
                             body=None,
                             results=None,
                             outputs=None,
                             not_called_msg=None,
                             nb_args_msg=None,
                             arg_names_msg=None,
                             arg_defaults_msg=None,
                             wrong_result_msg=None,
                             wrong_output_msg=None,
                             expand_message=True):
    """Test a function definition.

    This function helps you test a function definition. Generally four things can be tested:
        1) The argument names of the function (including if the correct defaults are used)
        2) The body of the functions (does it output correctly, are the correct functions used)
        3) The return value with a certain input
        4) The output value with a certain input
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
        results (list(tuple)): a list of tuples representing arguments that should be passed to the defined
            function. These arguments are passed to the function in the student environment and the solution
            environment, the results (what's returned) are compared.
        outputs (list(tuple)): a list of tuples representing arguments that should be passed to the defined
            function. These arguments are passed to the function in the student environment and the solution
            environment, the outpus are compared.
        not_called_msg (str): message if the function is not defined.
        nb_args_msg (str): message if the number of arguments do not matched.
        arg_names_msg (str): message if the argument names do not match.
        arg_defaults_msg (str): message if the argument default values do not match.
        wrong_result_msg (str): message if one of the tested function call's result did not match.
        wrong_output_msg (str): message if one of the tested functions call's output did not match.
        expand_message (bool): only relevant if there is a body test. If True, feedback messages defined in the
            body test will be preceded by 'In your definition of ___, '. If False, `test_function_definition()`
            will generate no extra feedback if the body test fails. Defaults to True.

    Examples:
        Student code

        | ``def shout( word, times = 3):``
        |     ``shout_word = not_word + '???'``
        |     ``print( shout_word )``
        |     ``return word * times``

        Solution code

        | ``def shout( word = 'help', times = 3 ):``
        |     ``shout_word = word + '!!!'``
        |     ``print( shout_word )``
        |     ``return word * times``

        SCT

        | ``test_function_definition('shout')``: fail.
        | ``test_function_definition('shout', arg_defaults = False)``: pass.
        | ``test_function_definition('shout', arg_defaults = False,``
        |     ``outputs = [('help')])``: fail.
        | ``test_function_definition('shout', arg_defaults = False,``
        |     ``results = [('help', 2)])``: pass.
        | ``test_function_definition('shout', args_defaults = False``
        |     ``body = lambda: test_function('print', args = []]))``: pass.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_function_definition")

    state.extract_function_defs()
    solution_defs = state.solution_function_defs
    student_defs = state.student_function_defs

    try:
        solution_def = solution_defs[name]
    except KeyError:
        raise NameError("%s not in solution environment" % name)

    c_not_called_msg = not_called_msg or \
        ("You didn't define the following function: `%s()`." %
            name)
    rep.do_test(DefinedTest(name, student_defs, c_not_called_msg))
    if rep.failed_test:
        return
    student_def = student_defs[name]

    args_solution = solution_def['args']
    args_student = student_def['args']
    if arg_names or arg_defaults:

        nb_args_solution = len(args_solution)
        nb_args_student = len(args_student)
        c_nb_args_msg = nb_args_msg or \
            ("You should define `%s()` with %d arguments, instead got %d." %
                (name, nb_args_solution, nb_args_student))
        rep.do_test(EqualTest(nb_args_solution, nb_args_student, c_nb_args_msg))
        if rep.failed_test:
            return

        for i in range(nb_args_solution):
            arg_name_solution, arg_default_solution = args_solution[i]
            arg_name_student, arg_default_student = args_student[i]
            if arg_names:
                c_arg_names_msg = arg_names_msg or \
                    ("In your definition of `%s()`, the %s argument should be called `%s`, instead got `%s`." %
                        (name, ordinal(i+1), arg_name_solution, arg_name_student))
                rep.do_test(
                    EqualTest(arg_name_solution, arg_name_student, c_arg_names_msg))
                if rep.failed_test:
                    return
            if arg_defaults:
                c_arg_defaults_msg = arg_defaults_msg or \
                    ("In your definition of `%s()`, the %s argument should have `%s` as default, instead got `%s`." %
                        (name, ordinal(i+1), arg_default_solution, arg_default_student))
                rep.do_test(
                    EqualTest(arg_default_solution, arg_default_student, c_arg_defaults_msg))
                if rep.failed_test:
                    return
    if rep.failed_test:
        return

    if body is not None:
        subtree_solution = solution_def['body']
        subtree_student = student_def['body']
        failed_before = rep.failed_test
        child = state.to_child_state(subtree_student, subtree_solution)
        child.context_solution = [arg[0] for arg in args_solution]
        child.context_student = [arg[0] for arg in args_student]
        body()
        child.to_parent_state()
        if expand_message and (failed_before is not rep.failed_test):
            rep.feedback.message = ("In your definition of `%s()`, " % name) + \
                utils.first_lower(rep.feedback.message)
    if rep.failed_test:
        return

    solution_env = state.solution_env
    student_env = state.student_env
    if results is not None:
        solution_func = solution_env[name]
        student_func = student_env[name]
        for call in results:
            if isinstance(call, str):
                call = (call,)
            solution_result = solution_func(*call)
            try:
                student_result = student_func(*call)
            except:
                c_wrong_result_msg = wrong_result_msg or \
                    ("Calling `%s%s` should result in `%s`, instead got an error." %
                        (name, arguments_as_string(call), solution_result))
                rep.do_test(Test(c_wrong_result_msg))
                return
            c_wrong_result_msg = wrong_result_msg or \
                ("Calling `%s%s` should result in `%s`, instead got `%s`." %
                    (name, arguments_as_string(call), solution_result, student_result))
            rep.do_test(EqualTest(solution_result, student_result, c_wrong_result_msg))
            if rep.failed_test:
                return
    if rep.failed_test:
        return

    if outputs is not None:
        solution_func = solution_env[name]
        student_func = student_env[name]
        for call in outputs:
            if isinstance(call, str):
                call = (call,)
            with capture_output() as out:
                solution_func(*call)
            solution_output = out[0].strip()
            try:
                with capture_output() as out:
                    student_func(*call)
                student_output = out[0].strip()
            except:
                c_wrong_output_msg = wrong_output_msg or \
                    ("Calling `%s%s` should output in `%s`, instead got an error." %
                        (name, arguments_as_string(call), solution_output))
                rep.do_test(Test(c_wrong_output_msg))
                return
            c_wrong_output_msg = wrong_output_msg or \
                ("Calling `%s%s` should output `%s`, instead got `%s`." %
                    (name, arguments_as_string(call), solution_output, student_output))
            rep.do_test(EqualTest(solution_output, student_output, c_wrong_output_msg))
            if rep.failed_test:
                return


def arguments_as_string(args):
    if len(args) == 0:
        return '()'
    elif len(args) > 1:
        return str(args)
    elif isinstance(args[0], str):
        return "('"+args[0]+"')"
    else:
        return '('+str(args)+')'

