from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import check_node, check_part_index
from pythonwhat.test_funcs.test_function import bind_args
from pythonwhat.tasks import getSignatureInProcess
from functools import partial

def check_function(name, index=0, 
                   missing_msg = "Did you define {typestr}?", 
                   expand_msg  = "In your definition of {sol_part[name]}, ", 
                   params_not_matched_msg = "Something went wrong in figuring out how you specified the "
                                            "arguments for `{sol_part[name]}`; have another look at your code and its output.",
                   state=None):
    rep = Reporter.active_reporter
    stu_out = state.student_function_calls
    sol_out = state.solution_function_calls

    import pdb; pdb.set_trace()
    # get function state
    func_list = check_node('function_calls', name, '{ordinal} function call to {name}', missing_msg, expand_msg, state)
    # grab specific function call
    # TODO NoneType not subscriptable, alter parsing so func part is dict
    child_func = check_part_index(None, index, "", func_list, state=func_list)
    stu_parts, sol_parts = child_func.student_parts, child_func.solution_parts
    # Signatures
    get_sig = partial(getSignatureInProcess, name=name, signature=signature,
                                             manual_sigs = state.get_manual_sigs())

    try:
        sol_sig = get_sig(mapped_name=sol_parts['name'], process=solution_process)
        sol_parts['args'], _ = bind_args(sol_sig, sol_parts['pos_args'], sol_parts['keywords'])
    except:
        raise ValueError("Something went wrong in matching call index {index} of {name} to its signature. "
                         "You might have to manually specify or correct the signature."
                                .format(index=index, name=name))

    # TODO if can't parse sig, send failed test msg
    try:
        stu_sig = get_sig(mapped_name=stu_parts['name'], process=child_func.student_process)
        stu_parts['args'], _ = bind_args(stu_sig, stu_parts['pos_args'], stu_parts['keywords'])
    except:
        _msg = state.build_message(params_not_matched_msg)
        rep.do_test(Test(Feedback(_msg, state.highlight)))

    # three types of parts: pos_args, keywords, args (e.g. these are bound to sig)
    return child_func
