import copy

def set_context_vals(env, context, context_vals = None):
    if context_vals:
        if len(context) == 1 != len(context_vals): context_vals = [context_vals]

        env.update({key: value for (key, value) in zip(context, context_vals)})
