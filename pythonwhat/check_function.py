from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import part_to_child
from pythonwhat.test_funcs.test_function import bind_args
from pythonwhat.tasks import getSignatureInProcess
from pythonwhat.utils import get_ord
from pythonwhat.Test import Test
from pythonwhat.Feedback import Feedback
from pythonwhat.parsing import IndexedDict
from functools import partial

def bind_args(signature, args_part):
    pos_args = []; kw_args = {}
    for k, arg in args_part.items():
        if isinstance(k, int): pos_args.append(arg)
        else: kw_args[k] = arg

    bound_args = signature.bind(*pos_args, **kw_args)

    return (IndexedDict(bound_args.arguments), signature)

MSG_PREPEND = "__JINJA__:Check your code in the {{child['part']+ ' of the' if child['part']}} {{typestr}}. "
def check_function(name, index, 
                   missing_msg = "FMT:Did you define {typestr}?", 
                   params_not_matched_msg = "FMT:Something went wrong in figuring out how you specified the "
                                            "arguments for `{name}`; have another look at your code and its output.",
                   expand_msg  = MSG_PREPEND, 
                   signature=True,
                   typestr = "{ordinal} function call",
                   state=None):
    rep = Reporter.active_reporter
    stu_out = state.student_function_calls
    sol_out = state.solution_function_calls

    fmt_kwargs = {'ordinal': get_ord(index+1),
                  'index': index,
                  'name': name}
    fmt_kwargs['typestr'] = typestr.format(**fmt_kwargs)

    # Get Parts ----
    try:
        stu_parts = stu_out[name][index]
    except (KeyError, IndexError):
        _msg = state.build_message(missing_msg, fmt_kwargs)
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    sol_parts = sol_out[name][index]

    # Signatures -----
    if signature:
        signature = None if isinstance(signature, bool) else signature
        get_sig = partial(getSignatureInProcess, name=name, signature=signature,
                                                manual_sigs = state.get_manual_sigs())

        try:
            sol_sig = get_sig(mapped_name=sol_parts['name'], process=state.solution_process)
            sol_parts['args'], _ = bind_args(sol_sig, sol_parts['args'])
        except:
            raise ValueError("Something went wrong in matching call index {index} of {name} to its signature. "
                            "You might have to manually specify or correct the signature."
                                    .format(index=index, name=name))

        try:
            stu_sig = get_sig(mapped_name=stu_parts['name'], process=state.student_process)
            stu_parts['args'], _ = bind_args(stu_sig, stu_parts['args'])
        except Exception as e:
            _msg = state.build_message(params_not_matched_msg, fmt_kwargs)
            rep.do_test(Test(Feedback(_msg, stu_parts['node'])))

    # three types of parts: pos_args, keywords, args (e.g. these are bound to sig)
    append_message = {'msg': expand_msg, 'kwargs': fmt_kwargs}
    child = part_to_child(stu_parts, sol_parts, append_message, state, node_name='function_calls')
    return child
