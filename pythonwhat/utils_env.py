import copy

def set_context_vals(env, context, context_vals = None):
    if context_vals is not None and context_vals is not []:
        if len(context) > 1:
            env.update({key: value for (key, value) in zip(context, context_vals)})
        else:
            env.update({context[0]: (context_vals[0] if len(context_vals) == 1 else context_vals)})
