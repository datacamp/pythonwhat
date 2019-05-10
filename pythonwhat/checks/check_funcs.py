from pythonwhat.checks.check_logic import multi
from pythonwhat.checks.has_funcs import has_part
from protowhat.Feedback import InstructorError
from pythonwhat.tasks import setUpNewEnvInProcess, breakDownNewEnvInProcess
from pythonwhat.utils import get_ord
from pythonwhat.utils_ast import assert_ast
import ast
from jinja2 import Template


def render(template, kwargs):
    return Template(template).render(**kwargs)


def part_to_child(stu_part, sol_part, append_message, state, node_name=None):
    # stu_part and sol_part will be accessible on all templates
    append_message["kwargs"].update({"stu_part": stu_part, "sol_part": sol_part})

    # if the parts are dictionaries, use to deck out child state
    if all(isinstance(p, dict) for p in [stu_part, sol_part]):
        child_state = state.to_child(
            student_ast=stu_part["node"],
            solution_ast=sol_part["node"],
            student_context=stu_part.get("target_vars"),
            solution_context=sol_part.get("target_vars"),
            student_parts=stu_part,
            solution_parts=sol_part,
            highlight=stu_part.get("highlight"),
            append_message=append_message,
            node_name=node_name,
        )
    else:
        # otherwise, assume they are just nodes
        child_state = state.to_child(
            student_ast=stu_part,
            solution_ast=sol_part,
            append_message=append_message,
            node_name=node_name,
        )

    return child_state


def check_part(state, name, part_msg, missing_msg=None, expand_msg=None):
    """Return child state with name part as its ast tree"""

    if missing_msg is None:
        missing_msg = "Are you sure you defined the {{part}}? "
    if expand_msg is None:
        expand_msg = "Did you correctly specify the {{part}}? "

    if not part_msg:
        part_msg = name
    append_message = {"msg": expand_msg, "kwargs": {"part": part_msg}}

    has_part(state, name, missing_msg, append_message["kwargs"])

    stu_part = state.student_parts[name]
    sol_part = state.solution_parts[name]

    assert_ast(state, sol_part, append_message["kwargs"])

    return part_to_child(stu_part, sol_part, append_message, state)


def check_part_index(state, name, index, part_msg, missing_msg=None, expand_msg=None):
    """Return child state with indexed name part as its ast tree.

    ``index`` can be:

    - an integer, in which case the student/solution_parts are indexed by position.
    - a string, in which case the student/solution_parts are expected to be a dictionary.
    - a list of indices (which can be integer or string), in which case the student parts are indexed step by step.
    """

    if missing_msg is None:
        missing_msg = "Are you sure you defined the {{part}}? "
    if expand_msg is None:
        expand_msg = "Did you correctly specify the {{part}}? "

    # create message
    ordinal = get_ord(index + 1) if isinstance(index, int) else ""
    fmt_kwargs = {"index": index, "ordinal": ordinal}
    fmt_kwargs.update(part=render(part_msg, fmt_kwargs))

    append_message = {"msg": expand_msg, "kwargs": fmt_kwargs}

    # check there are enough parts for index
    has_part(state, name, missing_msg, fmt_kwargs, index)

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


def check_node(
    state, name, index=0, typestr="{{ordinal}} node", missing_msg=None, expand_msg=None
):

    if missing_msg is None:
        missing_msg = "The system wants to check the {{typestr}} but hasn't found it."
    if expand_msg is None:
        expand_msg = "Check the {{typestr}}. "

    stu_out = state.ast_dispatcher.find(name, state.student_ast)
    sol_out = state.ast_dispatcher.find(name, state.solution_ast)

    # check if there are enough nodes for index
    fmt_kwargs = {
        "ordinal": get_ord(index + 1) if isinstance(index, int) else "",
        "index": index,
        "name": name,
    }
    fmt_kwargs["typestr"] = render(typestr, fmt_kwargs)

    # test if node can be indexed succesfully
    try:
        stu_out[index]
    except (KeyError, IndexError):  # TODO comment errors
        _msg = state.build_message(missing_msg, fmt_kwargs)
        state.report(_msg)

    # get node at index
    stu_part = stu_out[index]
    sol_part = sol_out[index]

    append_message = {"msg": expand_msg, "kwargs": fmt_kwargs}

    return part_to_child(stu_part, sol_part, append_message, state, node_name=name)


# context functions -----------------------------------------------------------
# TODO: check if still useful
def with_context(state, *args, child=None):

    # set up context in processes
    solution_res = setUpNewEnvInProcess(
        process=state.solution_process, context=state.solution_parts["with_items"]
    )
    if isinstance(solution_res, Exception):
        raise InstructorError(
            "error in the solution, running test_with(): %s" % str(solution_res)
        )

    student_res = setUpNewEnvInProcess(
        process=state.student_process, context=state.student_parts["with_items"]
    )
    if isinstance(student_res, AttributeError):
        child.report(
            "In your `with` statement, you're not using a correct context manager."
        )

    if isinstance(student_res, (AssertionError, ValueError, TypeError)):
        child.report(
            "In your `with` statement, the number of values in your context manager "
            "doesn't correspond to the number of variables you're trying to assign it to."
        )

    # run subtests
    try:
        multi(state, *args)
    finally:
        # exit context
        close_solution_context = breakDownNewEnvInProcess(
            process=state.solution_process
        )
        if isinstance(close_solution_context, Exception):
            raise InstructorError(
                "error in the solution, closing the `with` fails with: %s"
                % close_solution_context
            )

        close_student_context = breakDownNewEnvInProcess(process=state.student_process)
        if isinstance(close_student_context, Exception):
            state.report(
                "Your `with` statement can not be closed off correctly, you're "
                "not using the context manager correctly."
            )
    return state


def check_args(state, name, missing_msg=None):
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
        missing_msg = "Did you specify the {{part}}?"

    if name in ["*args", "**kwargs"]:  # for check_function_def
        return check_part(state, name, name, missing_msg=missing_msg)
    else:
        if isinstance(name, list):  # dealing with args or kwargs
            if name[0] == "args":
                arg_str = "{} argument passed as a variable length argument".format(
                    get_ord(name[1] + 1)
                )
            else:
                arg_str = "argument `{}`".format(name[1])
        else:
            arg_str = (
                "{} argument".format(get_ord(name + 1))
                if isinstance(name, int)
                else "argument `{}`".format(name)
            )
        return check_part_index(state, "args", name, arg_str, missing_msg=missing_msg)


# CALL CHECK ==================================================================


def build_call(callstr, node):
    if isinstance(node, ast.FunctionDef):  # function name
        func_expr = ast.Name(id=node.name, ctx=ast.Load())
        argstr = "`%s`" % callstr.replace("f", node.name)
    elif isinstance(node, ast.Lambda):  # lambda body expr
        func_expr = node
        argstr = "it with the arguments `%s`" % callstr.replace("f", "")
    else:
        raise TypeError("Can't handle AST that is passed.")

    parsed = ast.parse(callstr).body[0].value
    parsed.func = func_expr
    ast.fix_missing_locations(parsed)
    return parsed, argstr


def check_call(state, callstr, argstr=None, expand_msg=None):
    """When checking a function definition of lambda function,
    prepare has_equal_x for checking the call of a user-defined function.

    Args:
        callstr (str): call string that specifies how the function should be called, e.g. `f(1, a = 2)`.
           ``check_call()`` will replace ``f`` with the function/lambda you're targeting.
        argstr (str): If specified, this overrides the way the function call is refered to in the expand message.
        expand_msg (str): If specified, this overrides any messages that are prepended by previous SCT chains.
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
        ["function_defs", "lambda_functions"],
        "check_call",
        ["check_function_def", "check_lambda_function"],
    )

    if expand_msg is None:
        expand_msg = "To verify it, we reran {{argstr}}. "

    stu_part, _argstr = build_call(callstr, state.student_parts["node"])
    sol_part, _ = build_call(callstr, state.solution_parts["node"])

    append_message = {"msg": expand_msg, "kwargs": {"argstr": argstr or _argstr}}
    child = part_to_child(stu_part, sol_part, append_message, state)

    return child
