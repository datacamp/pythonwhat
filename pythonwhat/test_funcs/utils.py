import ast

from protowhat.Feedback import InstructorError
from pythonwhat.Feedback import Feedback
from pythonwhat.Test import EqualTest
from pythonwhat.checks.check_funcs import StubState
from pythonwhat.checks.has_funcs import evalCalls
from pythonwhat.tasks import ReprFail


def fix_format(arguments):
    if isinstance(arguments, str):
        arguments = (arguments,)
    if isinstance(arguments, tuple):
        arguments = list(arguments)

    if isinstance(arguments, list):
        arguments = {"args": arguments, "kwargs": {}}

    if (
        not isinstance(arguments, dict)
        or "args" not in arguments
        or "kwargs" not in arguments
    ):
        raise ValueError(
            "Wrong format of arguments in 'results', 'outputs' or 'errors'; either a list, or a dictionary with names args (a list) and kwargs (a dict)"
        )

    return arguments


def stringify(arguments):
    vararg = str(arguments["args"])[1:-1]
    kwarg = ", ".join(
        ["%s = %s" % (key, value) for key, value in arguments["kwargs"].items()]
    )
    if len(vararg) == 0:
        if len(kwarg) == 0:
            return "()"
        else:
            return "(" + kwarg + ")"
    else:
        if len(kwarg) == 0:
            return "(" + vararg + ")"
        else:
            return "(" + ", ".join([vararg, kwarg]) + ")"


# TODO: test string syntax with check_function_def
#       test argument syntax with check_lambda_function
def run_call(args, node, process, get_func, **kwargs):
    # Get function expression
    if isinstance(node, ast.FunctionDef):  # function name
        func_expr = ast.Name(id=node.name, ctx=ast.Load())
    elif isinstance(node, ast.Lambda):  # lambda body expr
        func_expr = node
    else:
        raise InstructorError("Only function definition or lambda may be called")

    ast.fix_missing_locations(func_expr)
    return get_func(process=process, tree=func_expr, call=args, **kwargs)


MSG_CALL_INCORRECT = "Calling {{argstr}} should {{action}} `{{str_sol}}`, instead got {{str_stu if str_stu == 'no printouts' else '`' + str_stu + '`'}}."
MSG_CALL_ERROR = "Calling {{argstr}} should {{action}} `{{str_sol}}`, instead it errored out: `{{str_stu}}`."
MSG_CALL_ERROR_INV = (
    "Calling {{argstr}} should {{action}} `{{str_sol}}`, instead got `{{str_stu}}`."
)


def call(
    state,
    args,
    test="value",
    incorrect_msg=None,
    error_msg=None,
    argstr=None,
    func=None,
    **kwargs
):
    """Use ``check_call()`` in combination with ``has_equal_x()`` instead.
    """

    if incorrect_msg is None:
        incorrect_msg = MSG_CALL_INCORRECT
    if error_msg is None:
        error_msg = MSG_CALL_ERROR_INV if test == "error" else MSG_CALL_ERROR

    assert test in ("value", "output", "error")

    get_func = evalCalls[test]

    # Run for Solution --------------------------------------------------------
    eval_sol, str_sol = run_call(
        args, state.solution_parts["node"], state.solution_process, get_func, **kwargs
    )

    if (test == "error") ^ isinstance(eval_sol, Exception):
        _msg = (
            state.build_message(
                "Calling {{argstr}} resulted in an error (or not an error if testing for one). Error message: {{type_err}} {{str_sol}}",
                dict(type_err=type(eval_sol), str_sol=str_sol, argstr=argstr),
            ),
        )
        raise InstructorError(_msg)

    if isinstance(eval_sol, ReprFail):
        _msg = state.build_message(
            "Can't get the result of calling {{argstr}}: {{eval_sol.info}}",
            dict(argstr=argstr, eval_sol=eval_sol),
        )
        raise InstructorError(_msg)

    # Run for Submission ------------------------------------------------------
    eval_stu, str_stu = run_call(
        args, state.student_parts["node"], state.student_process, get_func, **kwargs
    )
    action_strs = {
        "value": "return",
        "output": "print out",
        "error": "error out with the message",
    }
    fmt_kwargs = {
        "part": argstr,
        "argstr": argstr,
        "str_sol": str_sol,
        "str_stu": str_stu,
        "action": action_strs[test],
    }

    # either error test and no error, or vice-versa
    stu_node = state.student_parts["node"]
    stu_state = StubState(stu_node, state.highlighting_disabled)
    if (test == "error") ^ isinstance(eval_stu, Exception):
        _msg = state.build_message(error_msg, fmt_kwargs)
        state.report(Feedback(_msg, stu_state))

    # incorrect result
    _msg = state.build_message(incorrect_msg, fmt_kwargs)
    state.do_test(EqualTest(eval_sol, eval_stu, Feedback(_msg, stu_state), func))

    return state
