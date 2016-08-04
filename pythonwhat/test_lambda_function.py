import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.Test import Test, BiggerTest, EqualTest, InstanceTest
from pythonwhat import utils
from pythonwhat.utils import get_ord, get_num
from pythonwhat.test_function_definition import test_args, test_body

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
                         wrong_error_msg=None,
                         expand_message=True):
    
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


    solution_env = state.solution_env
    student_env = state.student_env

    for call in results:
        parsed = ast.parse(call).body[0].value
        argstr = call.replace('lam', '')
        try:
            # replace fun call with solution lambda function
            parsed.func = solution_fun
            solution_result = eval(compile(ast.Expression(parsed), "<solution>", "eval"))
        except:
            raise ValueError("Something went wrong in testing the result for %s%s" % (solution_str, call))

        try:
            # replace fun call with student lambda function
            parsed.func = student_fun
            student_result = eval(compile(ast.Expression(parsed), '<student>', 'eval'))
        except:
            c_wrong_result_msg = wrong_result_msg or \
                ("Calling the %s with arguments `%s` should result in `%s`, instead got an error." %
                    (fun_name, argstr, solution_result))
            rep.do_test(Test(c_wrong_result_msg))
            return

        c_wrong_result_msg = wrong_result_msg or \
            ("Calling %s with arguments `%s` should result in `%s`, instead got `%s`." %
                (fun_name, argstr, solution_result, student_result))
        rep.do_test(EqualTest(solution_result, student_result, c_wrong_result_msg))
        if rep.failed_test:
            return

    for call in errors:
        parsed = ast.parse(call).body[0].value
        argstr = call.replace('lam', '')
        try:
            # replace fun call with solution lambda function
            parsed.func = solution_fun
            solution_result = eval(compile(ast.Expression(parsed), "<solution>", "eval"))
        except Exception as sol_exc:
            solution_result = sol_exc
        if not isinstance(solution_result, Exception):
            raise ValueError("Calling %s with arguments %s did not generate an error in the solution environment." % (fun_name, argstr))

        try:
            # replace fun call with student lambda function
            parsed.func = student_fun
            student_result = eval(compile(ast.Expression(parsed), '<student>', 'eval'))
        except Exception as stud_exc:
            student_result = stud_exc
        feedback_msg = no_error_msg or ("Calling %s with the arguments `%s` doesn't result in an error, but it should!" % (fun_name, argstr))
        rep.do_test(InstanceTest(student_result, Exception, feedback_msg))
        if rep.failed_test:
            return
        feedback_msg = wrong_error_msg or ("Calling %s with the arguments `%s` should result in a `%s`, instead got a `%s`." % \
            (fun_name, argstr, solution_result.__class__.__name__, student_result.__class__.__name__))
        rep.do_test(InstanceTest(student_result, solution_result.__class__, feedback_msg))
        if rep.failed_test:
            return



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
