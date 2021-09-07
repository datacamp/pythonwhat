import ast

from protowhat.failure import debugger


def wrap_in_module(node):
    new_node = ast.Module(node, [])
    if isinstance(node, list):
        if len(node) > 0:
            new_node.first_token = node[0].first_token
            new_node.last_token = node[-1].last_token
        else:
            pass  # do nothing
    else:
        new_node.first_token = node.first_token
        new_node.last_token = node.first_token
    return new_node


def assert_ast(state, element, fmt_kwargs):
    err_msg = (
        "SCT fails on solution: "
        "You are zooming in on the {{part}}, but it is not an AST, so it can't be re-run."
        " If this error occurred because of ``check_args()``,"
        "you may have to refer to your argument differently, e.g. `['args', 0]` or `['kwargs', 'a']`. "
        "Read https://pythonwhat.readthedocs.io/en/latest/articles/checking_function_calls.html#signatures for more info."
    )
    # element can also be { 'node': AST }
    if isinstance(element, dict):
        element = element["node"]
    if isinstance(element, ast.AST):
        return
    if isinstance(element, list) and all([isinstance(el, ast.AST) for el in element]):
        return
    with debugger(state):
        state.report(err_msg, fmt_kwargs)
