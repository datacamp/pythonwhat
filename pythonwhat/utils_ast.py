import ast

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
