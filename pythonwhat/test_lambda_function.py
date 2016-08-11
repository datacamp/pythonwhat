import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.Test import Test, BiggerTest, EqualTest, InstanceTest
from pythonwhat import utils
from pythonwhat.utils import get_ord, get_num
from pythonwhat.test_function_definition import test_args, test_body
from pythonwhat.tasks import getFunctionTreeResultInProcess, getFunctionTreeErrorInProcess

def test_lambda_function(index,
                         arg_names=True,
                         arg_defaults=True,
                         body=None,
                         results=None,
                         errors=None,
                         not_called_msg=None,
                         nb_args_msg=None,
                         arg_names_msg=None,
                         arg_defaults_msg=None,
                         wrong_result_msg=None,
                         no_error_msg=None,
                         expand_message=True):
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
        results (list(tuple)): a list of strings representing function calls to the lam function. The lam
            function will be replaced by the actual lambda function from the student and solution code. The result
            of calling the lambda function will be compared between student and solution.
        errors (list(tupe)): a list of strings representing function calls to the lam function. The lam
            function will be replaced by the actual lambda function from the student and solution code. It will be
            checked if an error is generated appropriately for the specified inputs.
        not_called_msg (str): message if the function is not defined.
        nb_args_msg (str): message if the number of arguments do not matched.
        arg_names_msg (str): message if the argument names do not match.
        arg_defaults_msg (str): message if the argument default values do not match.
        wrong_result_msg (str): message if one of the tested function calls' result did not match.
        no_error_msg (str): message if one of the tested function calls' result did not generate an error.
        expand_message (bool): only relevant if there is a body test. If True, feedback messages defined in the
            body test will be preceded by 'In your definition of ___, '. If False, `test_function_definition()`
            will generate no extra feedback if the body test fails. Defaults to True.
    """

    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_lambda_function")

    state.extract_lambda_functions()

    student_lambdas = state.student_lambda_functions
    solution_lambdas = state.solution_lambda_functions

    # raise error if not enough solution_lambdas
    try:
        solution_lambda = solution_lambdas[index - 1]
    except KeyError:
        raise NameError("There aren't %s lambda functions in the solution environment" % get_num(index))

    # check if enough student_lambdas
    c_not_called_msg = not_called_msg or \
        ("The system wants to check the %s lambda function you defined but hasn't found it." % get_ord(index))
    rep.do_test(BiggerTest(len(student_lambdas), index - 1, Feedback(c_not_called_msg)))
    if rep.failed_test:
        return

    student_lambda = student_lambdas[index - 1]

    args_student = student_lambda['args']
    args_solution = solution_lambda['args']
    student_fun = student_lambda['fun']
    solution_fun = solution_lambda['fun']

    fun_name = "the %s lambda function" % get_ord(index)
    test_args(rep=rep,
              arg_names=arg_names,
              arg_defaults=arg_defaults,
              args_student=args_student,
              args_solution=args_solution,
              fun_def=student_fun,
              nb_args_msg=nb_args_msg,
              arg_names_msg=arg_names_msg,
              arg_defaults_msg=arg_defaults_msg,
              name=fun_name)

    if rep.failed_test:
        return

    # sub-scts expect a module, so wrap the lambda body in a list!"
    test_body(rep=rep,
              state=state,
              body=body,
              subtree_student=ast.Module([student_lambda['body']]),
              subtree_solution=ast.Module([solution_lambda['body']]),
              args_student=args_student,
              args_solution=args_solution,
              name=fun_name,
              expand_message=expand_message)

    if rep.failed_test:
        return

    for el in results:
        parsed = ast.parse(el).body[0].value
        argstr = el.replace('lam', '')

        parsed.func = solution_fun
        eval_solution, str_solution = getFunctionTreeResultInProcess(process = state.solution_process, tree = parsed)
        if eval_solution is None:
            raise ValueError("Something went wrong in testing the result of %s for arguments %s" % (fun_name, argstr))


        parsed.func = student_fun
        eval_student, str_student = getFunctionTreeResultInProcess(process = state.student_process, tree = parsed)

        if eval_student is None:
            c_wrong_result_msg = wrong_result_msg or \
                ("Calling the %s with arguments `%s` should result in `%s`, instead got an error." %
                    (fun_name, argstr, str_solution))
            rep.do_test(Test(Feedback(c_wrong_result_msg, student_fun)))
            return

        c_wrong_result_msg = wrong_result_msg or \
            ("Calling %s with arguments `%s` should result in `%s`, instead got `%s`." %
                (fun_name, argstr, str_solution, str_student))
        rep.do_test(EqualTest(eval_solution, eval_student, Feedback(c_wrong_result_msg, student_fun)))
        if rep.failed_test:
            return

    for el in errors:
        parsed = ast.parse(el).body[0].value
        argstr = el.replace('lam', '')

        parsed.func = solution_fun
        error_solution = getFunctionTreeErrorInProcess(process = state.solution_process, tree = parsed)
        if error_solution is None:
            raise ValueError("Calling %s with arguments %s did not generate an error in the solution environment." % (fun_name, argstr))

        parsed.func = student_fun
        error_student = getFunctionTreeErrorInProcess(process = state.student_process, tree = parsed)

        if error_student is None:
            feedback_msg = no_error_msg or ("Calling %s with the arguments `%s` doesn't result in an error, but it should!" % (fun_name, argstr))
            rep.do_test(Test(Feedback(feedback_msg, student_fun)))


def print_attrs(node):
    def _print(node):
        print("============")
        print(node.__class__.__name__)
        if hasattr(node, 'lineno'):
            print('lineno:' + str(node.lineno))
        else:
            print("NO LINENO")
        if hasattr(node, 'col_offset'):
            print('col_offset:' + str(node.col_offset))
        else:
            print("NO COL_OFFSET")

        for child in ast.iter_child_nodes(node):
            _print(child)
    _print(node)
