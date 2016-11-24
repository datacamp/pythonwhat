from pythonwhat.check_funcs import check_node
from pythonwhat.test_funcs.test_function import mapped_name
from pythonwhat.tasks import getSignatureInProcess
from functools import partial

def check_function(name, index=0, 
                   missing_msg = "Did you define {sol_part[name]}?", 
                   expand_msg  = "In your definition of {sol_part[name]}, ", 
                   state=None):
    rep = Reporter.active_reporter
    stu_out = state.student_function_calls
    sol_out = state.solution_function_calls

    # test if function exists
    stud_name = get_mapped_name(name, state.student_mappings)
    
    func_list = check_node('function_calls', name, 'function call', missing_msg, expand_msg, state)
    # get function state
    if index is None: 
        return func_list
    else:
        # TODO make has_part more robust
        # grab specific function call
        child_func = check_part(index, "FUNCTION MSG", func_list, "not enough func calls")
        stu_parts, sol_parts = child_func.student_parts, child_func.solution_parts
        # Signatures
        get_sig = partial(getSignatureInProcess, name=name, signature=signature,
                                                 manual_sigs = state.get_manual_sigs())

        # TODO if can't parse, raise warnings
        sol_sig = get_sig(mapped_name=sol_parts['name'], process=solution_process)
        sol_parts['args'], _ = bind_ards(sol_sig, sol_parts['pos_args'], sol_parts['keywords'])

        # TODO if can't parse sig, send failed test msg
        stu_sig = get_sig(mapped_name=stu_parts['name'], process=student_process)
        stu_parts['args'], _ = bind_ards(stu_sig, stu_parts['pos_args'], stu_parts['keywords'])

        # three types of parts: pos_args, keywords, args (e.g. these are bound to sig)
        return child_func
