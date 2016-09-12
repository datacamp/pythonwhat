import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedCollTest, EqualTest, Test, InstanceTest
from pythonwhat.Feedback import Feedback
from pythonwhat import utils
from pythonwhat.utils import get_ord
from pythonwhat.tasks import getTreeResultInProcess, getFunctionCallResultInProcess, getFunctionCallOutputInProcess, getFunctionCallErrorInProcess, ReprFail


def test_function_definition(name,
                             arg_names=True,
                             arg_defaults=True,
                             body=None,
                             results=None,
                             outputs=None,
                             errors=None,
                             not_called_msg=None,
                             nb_args_msg=None,
                             arg_names_msg=None,
                             arg_defaults_msg=None,
                             wrong_result_msg=None,
                             wrong_output_msg=None,
                             no_error_msg=None,
                             wrong_error_msg=None,
                             expand_message=True):
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
        raise NameError("%s not in solution code" % name)

    c_not_called_msg = not_called_msg or \
        ("You didn't define the following function: `%s()`." %
            name)
    rep.do_test(DefinedCollTest(name, student_defs, c_not_called_msg))
    if rep.failed_test:
        return
    student_def = student_defs[name]

    args_student=student_def['args']['args']
    args_solution=solution_def['args']['args']
    fun_def = student_def['fundef']
    fun_name = ("`%s()`" % name)

    test_args(rep=rep,
              arg_names=arg_names,
              arg_defaults=arg_defaults,
              args_student=args_student,
              args_solution=args_solution,
              fun_def=fun_def,
              nb_args_msg=nb_args_msg,
              arg_names_msg=arg_names_msg,
              arg_defaults_msg=arg_defaults_msg,
              student_process=state.student_process,
              solution_process=state.solution_process,
              name=fun_name)
    if rep.failed_test:
        return

    test_body(rep=rep,
              state=state,
              body=body,
              subtree_student=student_def['body'],
              subtree_solution=solution_def['body'],
              args_student=args_student,
              args_solution=args_solution,
              name=fun_name,
              expand_message=expand_message)

    if rep.failed_test:
        return

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
            if rep.failed_test:
                return

    if rep.failed_test:
        return

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

            if output_student is None:
                c_wrong_output_msg = wrong_output_msg or \
                    ("Calling `%s` should output `%s`, instead got an error." %
                        (call_str, output_solution))
                rep.do_test(Test(c_wrong_output_msg))
                return

            c_wrong_output_msg = wrong_output_msg or \
                ("Calling `%s` should output `%s`, instead got `%s`." %
                    (call_str, output_solution, output_student))
            rep.do_test(EqualTest(output_solution, output_student, c_wrong_output_msg))
            if rep.failed_test:
                return

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
            if rep.failed_test:
                return


def stringify(args):
    if len(args) == 0:
        return '()'
    else :
        return "(" + str(args)[1:-1] + ")"


def fix_format(arguments):
    if isinstance(arguments, str):
        arguments = (arguments, )
    if isinstance(arguments, tuple):
        arguments = list(arguments)
    return(arguments)

def test_args(rep, arg_names, arg_defaults, args_student, args_solution,
              fun_def, nb_args_msg, arg_names_msg, arg_defaults_msg,
              student_process, solution_process, name):

    #import pdb; pdb.set_trace();

    if arg_names or arg_defaults:
        nb_args_solution = len(args_solution)
        nb_args_student = len(args_student)
        c_nb_args_msg = nb_args_msg or \
            ("You should define %s with %d arguments, instead got %d." %
                (name, nb_args_solution, nb_args_student))

        rep.do_test(EqualTest(nb_args_solution, nb_args_student, Feedback(c_nb_args_msg, fun_def)))
        if rep.failed_test:
            return

        for i in range(nb_args_solution):
            arg_name_solution, arg_default_solution = args_solution[i]
            arg_name_student, arg_default_student = args_student[i]
            if arg_names:
                c_arg_names_msg = arg_names_msg or \
                    ("In your definition of %s, the %s argument should be called `%s`, instead got `%s`." %
                        (name, get_ord(i+1), arg_name_solution, arg_name_student))
                rep.do_test(
                    EqualTest(arg_name_solution, arg_name_student, Feedback(c_arg_names_msg, fun_def)))
                if rep.failed_test:
                    return

            if arg_defaults:

                if arg_defaults_msg is None:
                    if arg_default_solution is None:
                        c_arg_defaults_msg = "In your definition of %s, the %s argument should have no default." % (name, get_ord(i+1))
                    else :
                        c_arg_defaults_msg = "In your definition of %s, the %s argument does not have the correct default." % (name, get_ord(i+1))
                else :
                    c_arg_defaults_msg = arg_defaults_msg

                if arg_default_solution is None:
                    if arg_default_student is not None:
                        rep.do_test(Test(Feedback(c_arg_defaults_msg, arg_default_student)))
                        return
                else:
                    if arg_default_student is None:
                        rep.do_test(Test(Feedback(c_arg_defaults_msg, fun_def)))
                        return
                    else:
                        eval_solution, str_solution = getTreeResultInProcess(tree = arg_default_solution, process = solution_process)
                        if str_solution is None:
                            raise ValueError("Evaluating a default argument in the solution environment raised an error")
                        if isinstance(eval_solution, ReprFail):
                            raise ValueError("Couldn't figure out the value of a default argument: " + eval_solution.info)

                        eval_student, str_student = getTreeResultInProcess(tree = arg_default_student, process = student_process)
                        if str_student is None:
                            rep.do_test(Test(Feedback(c_arg_defaults_msg, arg_default_student)))
                        else :
                            rep.do_test(EqualTest(eval_student, eval_solution, Feedback(c_arg_defaults_msg, arg_default_student)))

                if rep.failed_test:
                    return

def test_body(rep, state, body,
              subtree_student, subtree_solution,
              args_student, args_solution,
              name, expand_message):
    if body is not None:
        if rep.failed_test:
            return
        child = state.to_child_state(subtree_student, subtree_solution)
        child.solution_context = [arg[0] for arg in args_solution]
        child.student_context = [arg[0] for arg in args_student]
        body()
        child.to_parent_state()
        if rep.failed_test:
            if expand_message:
                rep.feedback.message = ("In your definition of %s, " % name) + \
                    utils.first_lower(rep.feedback.message)
            if not rep.feedback.line_info:
                rep.feedback = Feedback(rep.feedback.message, subtree_student)
