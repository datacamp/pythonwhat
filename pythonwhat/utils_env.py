import copy
import ast

def assign_from_ast(node, expr):
    """
    Creates code to assign name (or tuple of names) node from expr

    This is useful for recreating destructuring assignment behavior, like
    a, *b = [1,2,3].
    """
    if isinstance(expr, str): expr = ast.Name(id=expr, ctx=ast.Load())
    mod = ast.Module([
        ast.Assign(targets=[node], value=expr)
        ])
    ast.fix_missing_locations(mod)
    return compile(mod, '<assignment_script>', 'exec')
    

def set_context_vals(env, context, context_vals = None):
    if context_vals:
        if len(context) == 1 != len(context_vals): context_vals = [context_vals]

        env.update({key: value for (key, value) in zip(context, context_vals)})
