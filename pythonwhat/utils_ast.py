import ast
from pythonwhat.Feedback import InstructorError

def wrap_in_module(node):
    new_node = ast.Module(node)
    if isinstance(node, list):
        if len(node) > 0:
            new_node.first_token = node[0].first_token
            new_node.last_token = node[-1].last_token
        else:
            pass # do nothing
    else:
        new_node.first_token = node.first_token
        new_node.last_token = node.first_token
    return new_node

def assert_ast(state, element, fmt_kwargs):
    patt = "You are zooming in on the {{part}}, but it is not an AST, so it can't be re-run."
    _err_msg = "SCT fails on solution: "
    _err_msg += state.build_message(patt, fmt_kwargs)
    # element can also be { 'node': AST }
    if isinstance(element, dict):
        element = element['node']
    if isinstance(element, ast.AST):
        return
    if isinstance(element, list) and all([isinstance(el, ast.AST) for el in element]):
        return
    raise InstructorError(_err_msg)