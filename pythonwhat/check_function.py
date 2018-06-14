from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import part_to_child, StubState
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
    return IndexedDict(bound_args.arguments)

MSG_PREPEND = "__JINJA__:Check the {{child['part']+ ' of the' if child['part']}} {{typestr}}. "
def check_function(name, index=0,
                   missing_msg = "FMT:Did you define the {typestr}?", 
                   params_not_matched_msg = "FMT:Something went wrong in figuring out how you specified the "
                                            "arguments for `{name}`; have another look at your code and its output.",
                   expand_msg  = MSG_PREPEND, 
                   signature=True,
                   typestr = "{ordinal} function call of `{name}()`",
                   state=None):
    """Check whether a particular function is called.

    This function is typically followed by ``check_args()`` to check whether the arguments were
    specified correctly.

    Args:
        name (str): the name of the function to be tested. When checking functions in packages, always
            use the 'full path' of the function.
        index (int): index of the function call to be checked. Defaults to 0.
        missing_msg (str): If specified, this overrides an automatically generated feedback message in case
            the student did not call the function correctly.
        params_not_matched_msg (str): If specified, this overrides an automatically generated feedback message
            in case the function parameters were not successfully matched.
        expand_msg (str): If specified, this overrides any messages that are prepended by previous SCT chains.
        signature (Signature): Normally, check_function() can figure out what the function signature is,
            but it might be necessary to use build_sig to manually build a signature and pass this along.
        typestr (formatted string): If specified, this overrides how the function call is automatically referred to.
        state (State): State object that is passed from the SCT Chain (don't specify this).

    :Examples:

        Student code and solution code::

            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])
            np.mean(arr)

        SCT::

            # Verify whether arr was correctly set in np.mean
            Ex().check_function('numpy.mean').check_args('a').has_equal_value()

            # Verify whether np.mean(arr) produced the same result
            Ex().check_function('numpy.mean').has_equal_value()

    """

    rep = Reporter.active_reporter
    stu_out = state.student_function_calls
    sol_out = state.solution_function_calls

    fmt_kwargs = {'ordinal': get_ord(index+1),
                  'index': index,
                  'name': name}
    fmt_kwargs['typestr'] = typestr.format(**fmt_kwargs)

    # Get Parts ----
    # Copy, otherwise signature binding overwrites sol_out[name][index]['args']
    sol_parts = {**sol_out[name][index]}

    try:
        # Copy, otherwise signature binding overwrites stu_out[name][index]['args']
        stu_parts = {**stu_out[name][index]}
    except (KeyError, IndexError):
        _msg = state.build_message(missing_msg, fmt_kwargs)
        rep.do_test(Test(Feedback(_msg, state)))

    # Signatures -----
    if signature:
        signature = None if isinstance(signature, bool) else signature
        get_sig = partial(getSignatureInProcess, name=name, signature=signature,
                                                manual_sigs = state.get_manual_sigs())

        try:
            sol_sig = get_sig(mapped_name=sol_parts['name'], process=state.solution_process)
            sol_parts['args'] = bind_args(sol_sig, sol_parts['args'])
        except:
            raise ValueError("Something went wrong in matching call index {index} of {name} to its signature. "
                             "You might have to manually specify or correct the signature."
                                    .format(index=index, name=name))

        try:
            stu_sig = get_sig(mapped_name=stu_parts['name'], process=state.student_process)
            stu_parts['args'] = bind_args(stu_sig, stu_parts['args'])
        except Exception:
            _msg = state.build_message(params_not_matched_msg, fmt_kwargs)
            rep.do_test(Test(Feedback(_msg, StubState(stu_parts['node'], state.highlighting_disabled))))

    # three types of parts: pos_args, keywords, args (e.g. these are bound to sig)
    append_message = {'msg': expand_msg, 'kwargs': fmt_kwargs}
    child = part_to_child(stu_parts, sol_parts, append_message, state, node_name='function_calls')
    return child
