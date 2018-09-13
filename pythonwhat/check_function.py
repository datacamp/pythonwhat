from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import part_to_child, StubState
from pythonwhat.tasks import getSignatureInProcess
from pythonwhat.utils import get_ord, get_times
from pythonwhat.Test import Test
from pythonwhat.Feedback import Feedback, InstructorError
from pythonwhat.parsing import IndexedDict
from functools import partial

def bind_args(signature, args_part):
    pos_args = []; kw_args = {}
    for k, arg in args_part.items():
        if isinstance(k, int): pos_args.append(arg)
        else: kw_args[k] = arg
    
    bound_args = signature.bind(*pos_args, **kw_args)
    return IndexedDict(bound_args.arguments)

def get_mapped_name(name, mappings):
    # get name by splitting on periods
    if "." in name:
        for orig, full_name in mappings.items():
            if name.startswith(full_name): return name.replace(full_name, orig)
    return name

MISSING_MSG = "Did you call `{{mapped_name}}()`{{' ' + times if index>0}}?"
SIG_ISSUE_MSG = "Have you specified the arguments for `{{mapped_name}}()` using the right syntax?"
PREPEND_MSG = "Check your {{ord + ' ' if index>0}}call of `{{mapped_name}}()`. "
def check_function(name, index=0,
                   missing_msg=None,
                   params_not_matched_msg=None,
                   expand_msg=None,
                   signature=True,
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

    append_missing = missing_msg is None
    append_params_not_matched = params_not_matched_msg is None
    if missing_msg is None:
        missing_msg = MISSING_MSG
    if expand_msg is None:
        expand_msg = PREPEND_MSG
    if params_not_matched_msg is None:
        params_not_matched_msg = SIG_ISSUE_MSG

    rep = Reporter.active_reporter
    stu_out = state.student_function_calls
    sol_out = state.solution_function_calls

    student_mappings = state.student_mappings

    fmt_kwargs = {'times': get_times(index+1),
                  'ord': get_ord(index+1),
                  'index': index,
                  'mapped_name': get_mapped_name(name, student_mappings)}

    # Get Parts ----
    # Copy, otherwise signature binding overwrites sol_out[name][index]['args']
    try:
        sol_parts = {**sol_out[name][index]}
    except KeyError:
        raise InstructorError("`check_function()` couldn't find a call of `%s()` in the solution code. Make sure you get the mapping right!" % name)
    except IndexError:
        raise InstructorError("`check_function()` couldn't find %s calls of `%s()` in your solution code." % (index+1, name))

    try:
        # Copy, otherwise signature binding overwrites stu_out[name][index]['args']
        stu_parts = {**stu_out[name][index]}
    except (KeyError, IndexError):
        _msg = state.build_message(missing_msg, fmt_kwargs, append=append_missing)
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
            raise InstructorError("`check_function()` couldn't match the %s call of `%s` to its signature. " % (get_ord(index + 1), name))

        try:
            stu_sig = get_sig(mapped_name=stu_parts['name'], process=state.student_process)
            stu_parts['args'] = bind_args(stu_sig, stu_parts['args'])
        except Exception:
            _msg = state.build_message(params_not_matched_msg, fmt_kwargs, append=append_params_not_matched)
            rep.do_test(Test(Feedback(_msg, StubState(stu_parts['node'], state.highlighting_disabled))))

    # three types of parts: pos_args, keywords, args (e.g. these are bound to sig)
    append_message = {'msg': expand_msg, 'kwargs': fmt_kwargs}
    child = part_to_child(stu_parts, sol_parts, append_message, state, node_name='function_calls')
    return child
