import ast

from pythonwhat.Test import Test, DefinedCollTest, EqualTest, BiggerTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.utils import get_ord, get_num
from pythonwhat.tasks import getResultInProcess, getSignatureInProcess, ReprFail
from .test_or import test_or

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
                  highlight=True,
                  state=None,
                  **kwargs):
    rep = Reporter.active_reporter

    index = index - 1

    eq_map = {"equal": EqualTest}
    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)
    eq_fun = eq_map[eq_condition]

    student_process, solution_process = state.student_process, state.solution_process

    solution_calls = state.solution_function_calls
    student_calls = state.student_function_calls
    student_mappings = state.student_mappings

    # for messaging purposes: replace with original alias or import again.
    stud_name = get_mapped_name(name, student_mappings)

    if not_called_msg is None:
        if index == 0:
            not_called_msg = "Have you called `%s()`?" % stud_name
        else:
            not_called_msg = ("The system wants to check the %s call of `%s()`, " +
                "but hasn't found it; have another look at your code.") % (get_ord(index + 1), stud_name)

    if name not in solution_calls or len(solution_calls[name]) <= index:
        raise NameError("%r not in solution environment (often enough)" % name)

    _msg = state.build_message(not_called_msg)
    rep.do_test(DefinedCollTest(name, student_calls, _msg))

    rep.do_test(BiggerTest(len(student_calls[name]), index, _msg))

    solution_call, args_solution, keyw_solution, sol_name = solution_calls[name][index]['_spec1']
    keyw_solution = {keyword.arg: keyword.value for keyword in keyw_solution}


    if args is None:
        args = list(range(len(args_solution)))

    if keywords is None:
        keywords = list(keyw_solution.keys())

    if len(args) > 0 or len(keywords) > 0:

        success = None

        # Get all options (some function calls may be blacklisted)
        call_indices = state.get_options(name, list(range(len(student_calls[name]))), index)

        feedback = None

        for call_ind in call_indices:
            student_call, args_student, keyw_student, stud_name = student_calls[name][call_ind]['_spec1']
            keyw_student = {keyword.arg: keyword.value for keyword in keyw_student}

            success = True
            dflt = "Have you specified all required arguments inside `%s()`?" % stud_name

            setdiff = list(set(keywords) - set(keyw_student.keys()))
            if (len(args) > 0 and (max(args) >= len(args_student))) or len(setdiff) > 0:
                if feedback is None:
                    if not args_not_specified_msg:
                        args_not_specified_msg = dflt
                    feedback = Feedback(args_not_specified_msg, student_call if highlight else None)
                success = False
                continue

            if do_eval is None:
                # don't have to go further: set used and break from the for loop
                state.set_used(name, call_ind, index)
                break

            feedback_msg = "Did you call `%s()` with the correct arguments?" % stud_name
            for arg in args:
                arg_student = args_student[arg]
                arg_solution = args_solution[arg]
                if incorrect_msg is None:
                    msg = feedback_msg + (" The %s argument seems to be incorrect." % get_ord(arg + 1))
                else:
                    msg = incorrect_msg

                test = build_test(arg_student, arg_solution,
                                  state,
                                  do_eval, eq_fun, msg, add_more=add_more,
                                  highlight=arg_student if highlight else None,
                                  **kwargs)
                test.test()

                if not test.result:
                    if feedback is None:
                        feedback = test.get_feedback()
                    success = False
                    break

            if success:
                for key in keywords:
                    key_student = keyw_student[key]
                    key_solution = keyw_solution[key]
                    if incorrect_msg is None:
                        msg = feedback_msg + (" Keyword `%s` seems to be incorrect." % key)
                        add_more = True
                    else:
                        msg = incorrect_msg
                        add_more = False

                    test = build_test(key_student, key_solution,
                                      state,
                                      do_eval, eq_fun, msg, add_more=add_more,
                                      highlight=key_student if highlight else None, **kwargs)
                    test.test()

                    if not test.result:
                        if feedback is None:
                            feedback = test.get_feedback()
                        success = False
                        break

            if success:
                # we have a winner that passes all argument and keyword checks
                state.set_used(name, call_ind, index)
                break

        if not success:
            if feedback is None:
                _msg = state.build_message("You haven't used enough appropriate calls of `%s()`" % stud_name)
                feedback = Feedback(_msg)
            rep.do_test(Test(feedback))

def test_print(index = 1,
               do_eval=True,
               eq_condition="equal",
               not_called_msg="Have you called `print()`?",
               params_not_matched_msg="Have you correctly called `print()`?",
               params_not_specified_msg="Have you correctly called `print()`?",
               incorrect_msg="Have you printed out the correct object?",
               highlight=True,
               state=None):
    test_function_v2("print",
                     index=index,
                     params=["value"],
                     signature=None,
                     eq_condition=eq_condition,
                     do_eval=do_eval,
                     not_called_msg=not_called_msg,
                     params_not_matched_msg=params_not_matched_msg,
                     params_not_specified_msg=params_not_specified_msg,
                     incorrect_msg=incorrect_msg,
                     highlight=highlight, state=state)
    """Test print() calls

    Utility function to test the print() function. For arguments, check test_function_v2()
    """

def test_function_v2(name,
                     index=1,
                     params=[],
                     signature=None,
                     eq_condition="equal",
                     do_eval=True,
                     not_called_msg=None,
                     params_not_matched_msg=None,
                     params_not_specified_msg=None,
                     incorrect_msg=None,
                     add_more=False,
                     highlight=True,
                     state=None,
                     **kwargs):
    """Test if function calls match (v2).

    This function compares a function call in the student's code with the corresponding one in the solution
    code. It will cause the reporter to fail if the corresponding calls do not match. The fail message
    that is returned will depend on the sort of fail.

    Args:
        name (str): the name of the function to be tested.
        index (int): index of the function call to be checked. Defaults to 1.
        params (list(str)): the parameter names of the function call that you want to check.
        signature (Signature): Normally, test_function() can figure out what the function signature is,
            but it might be necessary to use build_sig to manually build a signature and pass this along.
        eq_condition (str): how parameters are compared. Currently, only "equal" is supported,
            meaning that the arguments in student and solution process should have exactly the same value.
        do_eval (list(bool)): Boolean or list of booleans (parameter-specific) that specify whether or
            not arguments should be evaluated.
            True: arguments are evaluated and compared.
            False: arguments are not evaluated but 'string-matched'.
            None: arguments are not evaluated; it is only checked if they are specified.
        not_called_msg (str): custom feedback message if the function is not called.
        params_not_matched_message (str): custom feedback message if the function parameters were not successfully matched.
        params_not_specified_msg (str): string or list of strings (parameter-specific). Custom feedback message if not all
            parameters listed in params are specified by the student.
        incorrect_msg (list(str)): string or list of strings (parameter-specific). Custom feedback messages if the arguments
            don't correspond between student and solution code.
        kwargs: named arguments which are the same as those used by ``has_equal_value``.
    """

    rep = Reporter.active_reporter

    index = index - 1
    eq_map = {"equal": EqualTest}

    # ARG CHECKS --------------------------------------------------------------
    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)
    eq_fun = eq_map[eq_condition]

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

    # STATE STUFF -------------------------------------------------------------
    student_process, solution_process = state.student_process, state.solution_process

    solution_calls = state.solution_function_calls
    student_calls = state.student_function_calls
    student_mappings = state.student_mappings
    solution_mappings = state.solution_mappings

    stud_name = get_mapped_name(name, student_mappings)
    #sol_name = get_mapped_name(name, solution_mappings)

    if not_called_msg is None:
        if index == 0:
            not_called_msg = "Have you called `%s()`?" % stud_name
        else:
            not_called_msg = ("The system wants to check the %s call of `%s()`, " +
                "but hasn't found it; have another look at your code.") % (get_ord(index + 1), stud_name)

    if name not in solution_calls or len(solution_calls[name]) <= index:
        raise NameError("%r not in solution environment (often enough)" % name)
    # TODO: test if function name in dict of calls
    _msg = state.build_message(not_called_msg)
    rep.do_test(DefinedCollTest(name, student_calls, _msg))

    # TODO: test if number of specific function calls is less than index
    rep.do_test(BiggerTest(len(student_calls[name]), index, _msg))  # TODO

    # TODO pull into own function
    if len(params) > 0:

        # Parse Signature -----------------------------------------------------
        try:
            sol_call, arguments, keywords, sol_name = solution_calls[name][index]['_spec1']
            sol_sig = getSignatureInProcess(name=name, mapped_name=sol_name,
                                            signature=signature,
                                            manual_sigs = state.get_manual_sigs(),
                                            process=solution_process)
            solution_args, _ = bind_args(signature = sol_sig, arguments=arguments, keyws=keywords)
        except:
            raise ValueError(("Something went wrong in matching the %s call of %s to its signature." + \
                " You might have to manually specify or correct the function signature.") % (get_ord(index + 1), sol_name))

        # Check if params are in signature
        if set(params) - set(solution_args.keys()):
            raise ValueError("When testing %s(), the solution call doesn't specify the listed parameters." % name)

        # Get all options (some function calls may be blacklisted)
        call_indices = state.get_options(name, list(range(len(student_calls[name]))), index)

        feedback = None

        # Test all calls ------------------------------------------------------
        from functools import partial
        sub_tests = [partial(test_call, name, call_ind, signature, params, do_eval, solution_args, 
                             eq_fun, add_more, index,
                             params_not_specified_msg, params_not_matched_msg, incorrect_msg, 
                             keywords, state=state, highlight = highlight, **kwargs)
                     for call_ind in call_indices]
        test_or(*sub_tests, state=state)

        # TODO: AFAIK this was never called (and it isn't in the unit tests)
        #if feedback is None:
        #    feedback = Feedback("You haven't used enough appropriate calls of `%s()`." % stud_name)
        #rep.do_test(Test(feedback))    # TODO: sub_call


def test_call(name, call_ind, signature, params, do_eval, solution_args, 
              eq_fun, add_more, index,
              params_not_specified_msg, params_not_matched_msg, incorrect_msg, 
              keywords,  # pulled from solution process
              state, highlight, **kwargs):
    #stud_name = get_mapped_name(name, state.student_mappings)

    rep = Reporter.active_reporter
    # Parse Signature for Submission. TODO: more info
    try:
        student_call, arguments, keywords, stud_name = state.student_function_calls[name][call_ind]['_spec1']
        student_sig = getSignatureInProcess(name = name, mapped_name = stud_name,
                                            signature=signature,
                                            manual_sigs = state.get_manual_sigs(),
                                            process=state.student_process)
        student_args, student_params = bind_args(signature = student_sig, arguments=arguments, keyws=keywords)
    except:
        # -prep feedback-
        if not params_not_matched_msg:
            params_not_matched_msg = ("Something went wrong in figuring out how you specified the " + \
                "arguments for `%s()`; have another look at your code and its output.") % stud_name
        _msg = state.build_message(params_not_matched_msg)
        feedback = Feedback(_msg, student_call if highlight else None)
        # run subtest
        rep.do_test(Test(feedback))    # TODO: sub_call

    # Fail if student didn't use all params ---------------------------
    setdiff = list(set(params) - set(student_args.keys()))
    if setdiff:
        # -prep feedback-
        first_missing = setdiff[0]  # TODO: sets are not ordered! equiv to set.pop()?
        param_ind = params.index(first_missing)
        if params_not_specified_msg[param_ind] is None:
            msg = "Have you specified all required arguments inside `%s()`?" % stud_name
            # only if value can be supplied as keyword argument, give more info:
            if student_params[first_missing].kind in [1, 3, 4]:
                msg += " You didn't specify `%s`." % first_missing
        else:
            msg = params_not_specified_msg[param_ind]
        _msg = state.build_message(msg)
        feedback = Feedback(_msg, student_call if highlight else None)
        # run subtest
        rep.do_test(Test(feedback))    # TODO: sub_call
    
    # TEST EACH PARAM
    for ind, param in enumerate(params):
        if do_eval[ind] is None: continue
        arg_student = student_args[param]
        arg_solution = solution_args[param]
        param_kind = student_params[param].kind
        test_arg(param, do_eval[ind],
                 arg_student, arg_solution, param_kind, stud_name,
                 eq_fun, add_more,
                 incorrect_msg[ind], state=state, highlight = arg_student if highlight else None,
                 **kwargs)

    # If all is still good, we have a winner!
    state.set_used(name, call_ind, index)

def test_arg(param, do_eval, 
             arg_student, arg_solution, param_kind, stud_name,
             eq_fun, add_more,
             incorrect_msg, state=None, highlight = None, **kwargs):
    rep = Reporter.active_reporter

    if incorrect_msg is None:
        msg = "Did you call `%s()` with the correct arguments?" % stud_name
        # only if value can be supplied as keyword argument, give more info:
        if param_kind in [1, 3, 4]:
                msg += " The argument you specified for `%s` seems to be incorrect." % param
    else:
        msg = incorrect_msg

    test = build_test(arg_student, arg_solution,
                        state,
                        do_eval, eq_fun, msg, add_more = add_more, highlight=highlight,
                        **kwargs)
    # TODO
    rep.do_test(test)


def get_mapped_name(name, mappings):
    # get name by splitting on periods
    if "." in name:
        for orig, full_name in mappings.items():
            if name.startswith(full_name): return name.replace(full_name, orig)
    return name

def bind_args(signature, arguments, keyws):
    keyws = {keyword.arg: keyword.value for keyword in keyws}
    bound_args = signature.bind(*arguments, **keyws)
    return(bound_args.arguments, signature.parameters)

def build_test(stud, sol, state, do_eval, eq_fun, feedback_msg, add_more, highlight = False, **kwargs):
    got_error = False
    if do_eval:

        eval_solution, str_solution = getResultInProcess(tree = sol, process = state.solution_process, **kwargs)
        if isinstance(str_solution, Exception):
            raise ValueError("Running an argument in the solution environment raised an error")
        if isinstance(eval_solution, ReprFail):
            raise ValueError("Couldn't figure out the argument: " + eval_solution.info)

        eval_student, str_student = getResultInProcess(tree = stud, process = state.student_process, **kwargs)
        if isinstance(str_student, Exception):
            got_error = True

        # The (eval_student, ) part is important, because when eval_student is a tuple, we don't want
        # to expand them all over the %'s during formatting, we just want the tuple to be represented
        # in the place of the %r. Same for eval_solution.
        if add_more:
            if got_error:
                feedback_msg += " Expected `%s`, but got %s." % (str_solution, "an error")
            else:
                feedback_msg += " Expected `%s`, but got `%s`." % (str_solution, str_student)
    else:
        # We don't want the 'expected...' message here. It's a pain in the ass to deparse the ASTs to
        # give something meaningful.
        eval_student = ast.dump(stud)
        eval_solution = ast.dump(sol)

    _msg = state.build_message(feedback_msg)
    return(Test(Feedback(_msg, stud if highlight else None)) if got_error else
        eq_fun(eval_student, eval_solution, Feedback(_msg, stud if highlight else None)))








