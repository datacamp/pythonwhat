import ast

from functools import partial
from pythonwhat.check_function import check_function
from pythonwhat.check_funcs import check_args, has_equal_value, has_equal_ast
from pythonwhat.test_funcs.test_output_contains import has_printout

def arg_test(name, do_eval, missing_msg, incorrect_msg, state):
    arg_state = check_args(name=name,
                            missing_msg=missing_msg,
                            state=state)

    append = incorrect_msg is None

    if isinstance(do_eval, bool):
        if do_eval:
            has_equal_value(incorrect_msg=incorrect_msg,
                            append=append,
                            copy=False,
                            state=arg_state)
        else:
            has_equal_ast(incorrect_msg=incorrect_msg,
                          append=append,
                          state=arg_state)

def test_function(name,
                  index=1,
                  args=None,
                  keywords=None,
                  eq_condition="equal",
                  do_eval=True,
                  not_called_msg=None,
                  args_not_specified_msg=None,
                  incorrect_msg=None,
                  add_more=False,
                  state=None,
                  **kwargs):
    index = index - 1

    # if root-level (not in compound statement) calls: use has_printout
    if name == 'print' and state.parent_state is None:
        return has_printout(index=index, not_printed_msg=incorrect_msg, state=state)

    fun_state = check_function(name=name, index=index,
                               missing_msg=not_called_msg,
                               signature=False, state=state)

    _, args_solution, keyw_solution, _ = state.solution_function_calls[name][index]['_spec1']
    keyw_solution = {keyword.arg: keyword.value for keyword in keyw_solution}

    # try binding the signature.
    # If it works, we override fun_state (as it's more robust)
    # If it doesn't work, we just continue with the old fun_state
    try:
        fun_state = check_function(name=name, index=index,
                                   missing_msg=not_called_msg,
                                   signature=True, state=state)
    except:
        pass

    if args is None:
        args = list(range(len(args_solution)))

    if keywords is None:
        keywords = list(keyw_solution.keys())

    arg_test_partial = partial(arg_test,
                               do_eval=do_eval, missing_msg=args_not_specified_msg,
                               incorrect_msg=incorrect_msg, state=fun_state)

    [ arg_test_partial(name=i) for i in range(len(args)) ]
    [ arg_test_partial(name=keyword) for keyword in keywords ]

    return state

def test_function_v2(name,
                     index=1,
                     params=[],
                     signature=True,
                     eq_condition="equal",
                     do_eval=True,
                     not_called_msg=None,
                     params_not_matched_msg=None,
                     params_not_specified_msg=None,
                     incorrect_msg=None,
                     add_more=False,
                     state=None,
                     **kwargs):

    index = index - 1

    if not isinstance(params, list):
        raise NameError("Inside test_function_v2, make sure to specify a LIST of params.")

    if isinstance(do_eval, bool) or do_eval is None:
        do_eval = [do_eval] * len(params)

    if len(params) != len(do_eval):
        raise NameError("Inside test_function_v2, make sure that do_eval has the same length as params.")

    # if params_not_specified_msg is a str or None, convert into list
    if isinstance(params_not_specified_msg, str) or params_not_specified_msg is None:
        params_not_specified_msg = [params_not_specified_msg] * len(params)

    if len(params) != len(params_not_specified_msg):
        raise NameError("Inside test_function_v2, make sure that params_not_specified_msg has the same length as params.")

    # if incorrect_msg is a str or None, convert into list
    if isinstance(incorrect_msg, str) or incorrect_msg is None:
        incorrect_msg = [incorrect_msg] * len(params)

    if len(params) != len(incorrect_msg):
        raise NameError("Inside test_function_v2, make sure that incorrect_msg has the same length as params.")

    # if root-level (not in compound statement) calls: use has_printout
    if name == 'print' and state.parent_state is None:
        return has_printout(index=index, not_printed_msg=incorrect_msg[0], state=state)

    if len(params) == 0:
        signature = False

    fun_state = check_function(name=name,
                               index=index,
                               missing_msg=not_called_msg,
                               params_not_matched_msg=params_not_matched_msg,
                               signature=signature,
                               state=state)

    for i in range(len(params)):
        arg_test(name=params[i], do_eval=do_eval[i],
                 missing_msg=params_not_specified_msg[i],
                 incorrect_msg=incorrect_msg[i],
                 state=fun_state)

    return state