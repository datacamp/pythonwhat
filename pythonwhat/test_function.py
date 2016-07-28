import ast

from pythonwhat.Test import Test, DefinedTest, EqualTest, EquivalentTest, BiggerTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Fb import Feedback
from pythonwhat.utils import get_ord, get_num
import inspect
from inspect import Parameter as param

def test_function(name,
                  index=1,
                  args=None,
                  keywords=None,
                  eq_condition="equal",
                  do_eval=True,
                  not_called_msg=None,
                  args_not_specified_msg=None,
                  incorrect_msg=None):
    """Test if function calls match.

    This function compares a function call in the student's code with the corresponding one in the solution
    code. It will cause the reporter to fail if the corresponding calls do not match. The fail message
    that is returned will depend on the sort of fail.

    Args:
        name (str): the name of the function to be tested.
        index (int): index of the function call to be checked. Defaults to 1.
        args (list(int)): the indices of the positional arguments that have to be checked. If it is set to
          None, all positional arguments which are in the solution will be checked.
        keywords (list(str)): the indices of the keyword arguments that have to be checked. If it is set to
          None, all keyword arguments which are in the solution will be checked.
        eq_condition (str): The condition which is checked on the eval of the group. Can be "equal" --
          meaning that the operators have to evaluate to exactly the same value, or "equivalent" -- which
          can be used when you expect an integer and the result can differ slightly. Defaults to "equal".
        do_eval (bool): True: arguments are evaluated and compared. False: arguments are not evaluated but
            'string-matched'. None: arguments are not evaluated; it is only checked if they are specified.
        not_called_msg (str): feedback message if the function is not called.
        args_not_specified_msg (str): feedback message if the function is called but not all required arguments are specified
        incorrect_msg (str): feedback message if the arguments of the function in the solution doesn't match
          the one of the student.

    Raises:
        NameError: the eq_condition you passed is not "equal" or "equivalent".
        NameError: function is not called in the solution

    Examples:
        Student code

        | ``import numpy as np``
        | ``np.mean([1,2,3])``
        | ``np.std([2,3,4])``

        Solution code

        | ``import numpy``
        | ``numpy.mean([1,2,3], axis = 0)``
        | ``numpy.std([4,5,6])``

        SCT

        | ``test_function("numpy.mean", index = 1, keywords = [])``: pass.
        | ``test_function("numpy.mean", index = 1)``: fail.
        | ``test_function(index = 1, incorrect_op_msg = "Use the correct operators")``: fail.
        | ``test_function(index = 1, used = [], incorrect_result_msg = "Incorrect result")``: fail.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_function")

    index = index - 1

    eq_map = {"equal": EqualTest, "equivalent": EquivalentTest}
    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)
    eq_fun = eq_map[eq_condition]

    student_env, solution_env = state.student_env, state.solution_env

    state.extract_function_calls()
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

    rep.do_test(DefinedTest(name, student_calls, not_called_msg))
    if rep.failed_test:
        return

    rep.do_test(BiggerTest(len(student_calls[name]), index, not_called_msg))
    if rep.failed_test:
        return

    solution_call, args_solution, keyw_solution = solution_calls[name][index]
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
            student_call, args_student, keyw_student = student_calls[name][call_ind]
            keyw_student = {keyword.arg: keyword.value for keyword in keyw_student}

            success = True
            start = "Have you specified all required arguments inside `%s()`?" % stud_name

            if len(args) > 0 and (max(args) >= len(args_student)):
                if feedback is None:
                    if not args_not_specified_msg:
                        n = max(args)
                        if n == 0:
                            args_not_specified_msg = start + " You should specify one argument without naming it."
                        else:
                            args_not_specified_msg = start + (" You should specify %s arguments without naming them." % get_num(n + 1))
                    feedback = Feedback(args_not_specified_msg, student_call)
                success = False
                continue

            setdiff = list(set(keywords) - set(keyw_student.keys()))
            if len(setdiff) > 0:
                if feedback is None:
                    if not args_not_specified_msg:
                        args_not_specified_msg = start + " You should specify the keyword `%s` explicitly by its name." % setdiff[0]
                    feedback = Feedback(args_not_specified_msg, student_call)
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
                    add_more = True
                else:
                    msg = incorrect_msg
                    add_more = False

                test = build_test(arg_student, arg_solution,
                                  student_env, solution_env,
                                  do_eval, eq_fun, msg, add_more=add_more)
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
                                      student_env, solution_env,
                                      do_eval, eq_fun, msg, add_more=add_more)
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
                feedback = Feedback("You haven't used enough appropriate calls of `%s()`" % stud_name)
            rep.do_test(Test(feedback))

def test_print(index = 1,
               do_eval=True,
               eq_condition="equal",
               not_called_msg="Have you called `print()`?",
               params_not_matched_msg="Have you correctly called `print()`?",
               params_not_specified_msg="Have you correctly called `print()`?",
               incorrect_msg="Have you printed out the correct object?"):
    test_function_v2("print",
                     index=index,
                     params=["value"],
                     signature=None,
                     eq_condition=eq_condition,
                     do_eval=do_eval,
                     not_called_msg=not_called_msg,
                     params_not_matched_msg=params_not_matched_msg,
                     params_not_specified_msg=params_not_specified_msg,
                     incorrect_msg=incorrect_msg)
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
                     incorrect_msg=None):
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
        eq_condition (str): How objects should be compared ("equal" or "equivalent")
        do_eval (list(bool)): Boolean or list of booleans (parameter-specific) that specify whether or
            not arguments should be evaluated.
            True: arguments are evaluated and compared.
            False: arguments are not evaluated but 'string-matched'.
            None: arguments are not evaluated; it is only checked if they are specified.
        not_called_msg (str): custom feedback message if the function is not called.
        params_not_matched_message (str): custom feedback message if the function parameters were not successfully matched.
        params_not_specified_msg (str): custom feedback message if the function is called but not all parameters were specified
        incorrect_msg (list(str)): string or list of strings (parameter-specific). Custom feedback messages if the arguments
            don't correspond between student and solution code.
    """

    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_function")

    index = index - 1
    eq_map = {"equal": EqualTest, "equivalent": EquivalentTest}
    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)
    eq_fun = eq_map[eq_condition]

    if not isinstance(params, list):
        raise NameError("Inside test_function_v2, make sure to specify a LIST of params.")

    if isinstance(do_eval, bool) or do_eval is None:
        do_eval = [do_eval] * len(params)

    if len(params) != len(do_eval):
        raise NameError("Inside test_function_v2, make sure that do_eval has the same length as params.")

    if isinstance(incorrect_msg, str) or incorrect_msg is None:
        incorrect_msg = [incorrect_msg] * len(params)

    if len(params) != len(incorrect_msg):
        raise NameError("Inside test_function_v2, make sure that incorrect_msg has the same length as params.")

    student_env, solution_env = state.student_env, state.solution_env

    state.extract_function_calls()
    solution_calls = state.solution_function_calls
    student_calls = state.student_function_calls
    student_mappings = state.student_mappings
    solution_mappings = state.solution_mappings

    stud_name = get_mapped_name(name, student_mappings)
    sol_name = get_mapped_name(name, solution_mappings)

    if not_called_msg is None:
        if index == 0:
            not_called_msg = "Have you called `%s()`?" % stud_name
        else:
            not_called_msg = ("The system wants to check the %s call of `%s()`, " +
                "but hasn't found it; have another look at your code.") % (get_ord(index + 1), stud_name)

    if name not in solution_calls or len(solution_calls[name]) <= index:
        raise NameError("%r not in solution environment (often enough)" % name)

    rep.do_test(DefinedTest(name, student_calls, not_called_msg))
    if rep.failed_test:
        return

    rep.do_test(BiggerTest(len(student_calls[name]), index, not_called_msg))
    if rep.failed_test:
        return

    if len(params) > 0:

        try:
            sol_call, arguments, keywords = solution_calls[name][index]
            solution_args, _ = get_args(args=arguments, keyws=keywords,
                                        name=name, mapped_name=sol_name,
                                        signature=signature, env=solution_env)
        except:
            raise ValueError(("Something went wrong in matching the %s call of %s to its signature." + \
                " You might have to manually specify or correct the function signature.") % (get_ord(index + 1), sol_name))

        if len(list(set(params) - set(solution_args.keys()))) > 0:
            raise ValueError("When testing %s(), the solution call doesn't specify the listed parameters." % name)

        success = None

        # Get all options (some function calls may be blacklisted)
        call_indices = state.get_options(name, list(range(len(student_calls[name]))), index)

        feedback = None

        for call_ind in call_indices:

            # let's start with assuming all is good
            success = True

            try:
                student_call, arguments, keywords = student_calls[name][call_ind]
                student_args, student_params = get_args(args=arguments, keyws=keywords,
                         name=name, mapped_name=stud_name,
                         signature=signature, env=student_env)
            except:
                if feedback is None:
                    if not params_not_matched_msg:
                        params_not_matched_msg = ("Something went wrong in figuring out how you specified the " + \
                            "arguments for `%s()`; have another look at your code and its output.") % stud_name
                    feedback = Feedback(params_not_matched_msg, student_call)
                success = False
                continue

            setdiff = list(set(params) - set(student_args.keys()))
            if len(setdiff) > 0:
                if feedback is None:
                    if not params_not_specified_msg:
                        params_not_specified_msg = "Have you specified all required arguments inside `%s()`?" % stud_name
                        # only if value can be supplied as keyword argument, give more info:
                        first_missing = setdiff[0]
                        if student_params[first_missing].kind in [1, 3, 4]:
                            params_not_specified_msg += " You didn't specify `%s`." % first_missing
                    feedback = Feedback(params_not_specified_msg, student_call)
                success = False
                continue

            for ind, param in enumerate(params):

                if do_eval[ind] is None:
                    continue

                arg_student = student_args[param]
                arg_solution = solution_args[param]
                if incorrect_msg[ind] is None:
                    msg = "Did you call `%s()` with the correct arguments?" % stud_name
                    # only if value can be supplied as keyword argument, give more info:
                    if student_params[param].kind in [1, 3, 4]:
                            msg += " The argument you specified for `%s` seems to be incorrect." % param
                    add_more = True
                else:
                    msg = incorrect_msg[ind]
                    add_more = False

                test = build_test(arg_student, arg_solution,
                                  student_env, solution_env,
                                  do_eval[ind], eq_fun, msg, add_more)
                test.test()

                if not test.result:
                    if feedback is None:
                        feedback = test.get_feedback()
                    success = False
                    break

            # If all is still good, we have a winner!
            if success:
                state.set_used(name, call_ind, index)
                break

        if not success:
            if feedback is None:
                feedback = Feedback("You haven't used enough appropriate calls of `%s()`." % stud_name)
            rep.do_test(Test(feedback))

def get_mapped_name(name, mappings):
    mapped_name = name
    if "." in mapped_name:
        mappings_rev = {v: k for k, v in mappings.items()}
        els = name.split(".")
        if els[0] in mappings_rev.keys():
                mapped_name = ".".join([mappings_rev[els[0]]] + els[1:])
    return(mapped_name)


def get_args(args, keyws, name, mapped_name, signature, env):
    keyws = {keyword.arg: keyword.value for keyword in keyws}
    if signature is None:
        # establish function
        try:
            fun = eval(mapped_name, env)
        except:
            raise ValueError("%s() was not found." % mapped_name)

        # first go through manual sigs
        # try to get signature
        try:
            manual_sigs = get_manual_sigs()
            if name in manual_sigs:
                signature = inspect.Signature(manual_sigs[name])
            else:
                # it might be a method, and we have to find the general method name
                if "." in mapped_name:
                    els = name.split(".")
                    try:
                        els[0] = type(eval(els[0], env)).__name__
                        generic_name = ".".join(els[:])
                    except:
                        raise ValueError('signature error - cannot convert call')
                    if generic_name in manual_sigs:
                        signature = inspect.Signature(manual_sigs[generic_name])
                    else:
                        raise ValueError('signature error - %s not in builtins' % generic_name)
                else:
                    raise ValueError('manual signature not found')
        except:
            try:
                signature = inspect.signature(fun)
            except:
                raise ValueError('signature error - cannot determine signature')

    bound_args = signature.bind(*args, **keyws)
    return(bound_args.arguments, signature.parameters)

def build_test(stud, sol, student_env, solution_env, do_eval, eq_fun, feedback_msg, add_more):
    got_error = False
    if do_eval:
        try:
            eval_student = eval(
                compile(
                    ast.Expression(stud),
                    "<student>",
                    "eval"),
                student_env)
        except:
            got_error = True

        eval_solution = eval(
            compile(
                ast.Expression(sol),
                "<solution>",
                "eval"),
            solution_env)

        # The (eval_student, ) part is important, because when eval_student is a tuple, we don't want
        # to expand them all over the %'s during formatting, we just want the tuple to be represented
        # in the place of the %r. Same for eval_solution.
        if add_more:
            if got_error:
                feedback_msg += " Expected `%r`, but got %s." % (eval_solution, "an error")
            else:
                feedback_msg += " Expected `%r`, but got `%r`." % (eval_solution, eval_student)
    else:
        # We don't want the 'expected...' message here. It's a pain in the ass to deparse the ASTs to
        # give something meaningful.
        eval_student = ast.dump(stud)
        eval_solution = ast.dump(sol)

    return(Test(Feedback(feedback_msg, stud)) if got_error else
        eq_fun(eval_student, eval_solution, Feedback(feedback_msg, stud)))


def build_sig(*args):
    return(inspect.Signature(list(args)))

def get_manual_sigs():
    manual_sigs = {
        # builtins
        'abs': [param('x', param.POSITIONAL_ONLY)],
        'all': [param('iterable', param.POSITIONAL_ONLY)],
        'any': [param('iterable', param.POSITIONAL_ONLY)],
        'ascii': [param('obj', param.POSITIONAL_ONLY)],
        'bin': [param('number', param.POSITIONAL_ONLY)],
        'bool': [param('x', param.POSITIONAL_OR_KEYWORD)],
        'chr': [param('i', param.POSITIONAL_ONLY)],
        'callable': [param('obj', param.POSITIONAL_ONLY)],
        'classmethod': [param('function', param.POSITIONAL_ONLY)],
        'complex': [param('imag', param.POSITIONAL_OR_KEYWORD, default=0),
                    param('real', param.POSITIONAL_OR_KEYWORD, default=0)],
        'delattr': [param('obj', param.POSITIONAL_ONLY),
                    param('name', param.POSITIONAL_ONLY)],
        'dir': [param('object', param.POSITIONAL_OR_KEYWORD, default=None)],
        'divmod': [param('x', param.POSITIONAL_ONLY),
                   param('y', param.POSITIONAL_ONLY)],
        'enumerate': [param('iterable', param.POSITIONAL_ONLY),
                     param('start', param.POSITIONAL_OR_KEYWORD, default=0)],
        'float': [param('x', param.POSITIONAL_OR_KEYWORD)],
        'getattr': [param('object', param.POSITIONAL_ONLY),
                    param('name', param.POSITIONAL_ONLY),
                    param('default', param.POSITIONAL_ONLY, default=None)],
        'hasattr': [param('obj', param.POSITIONAL_ONLY),
                    param('name', param.POSITIONAL_ONLY)],
        'hash': [param('obj', param.POSITIONAL_ONLY)],
        'hex': [param('number', param.POSITIONAL_ONLY)],
        'id': [param('obj', param.POSITIONAL_ONLY)],
        'int': [param('x', param.POSITIONAL_OR_KEYWORD),
                param('base', param.POSITIONAL_OR_KEYWORD, default=10)],
        'isinstance': [param('obj', param.POSITIONAL_ONLY),
                       param('class_or_tuple', param.POSITIONAL_ONLY)],
        'issubclass': [param('cls', param.POSITIONAL_ONLY),
                       param('class_or_tuple', param.POSITIONAL_ONLY)],
        'list': [param('iterable', param.POSITIONAL_ONLY, default=None)],
        'len': [param('obj', param.POSITIONAL_ONLY)],
        'oct': [param('number', param.POSITIONAL_ONLY)],
        'open': [param('file', param.POSITIONAL_OR_KEYWORD),
                 param('mode', param.POSITIONAL_OR_KEYWORD, default='r'),
                 param('buffering', param.POSITIONAL_OR_KEYWORD, default=1),
                 param('encoding', param.POSITIONAL_OR_KEYWORD, default=None),
                 param('errors', param.POSITIONAL_OR_KEYWORD, default=None),
                 param('newline', param.POSITIONAL_OR_KEYWORD, default=None),
                 param('closefd', param.POSITIONAL_OR_KEYWORD, default=None),
                 param('opener', param.POSITIONAL_OR_KEYWORD, default=None)],
        'ord': [param('c', param.POSITIONAL_ONLY)],
        'pow': [param('x', param.POSITIONAL_ONLY),
                param('y', param.POSITIONAL_ONLY),
                param('z', param.POSITIONAL_ONLY, default=None)],
        'print': [param('value', param.POSITIONAL_ONLY)],
        'repr': [param('obj', param.POSITIONAL_ONLY)],
        'reversed': [param('sequence', param.POSITIONAL_ONLY)],
        'round': [param('number', param.POSITIONAL_OR_KEYWORD),
                  param('ndigits', param.POSITIONAL_OR_KEYWORD, default=0)],
        'set': [param('iterable', param.POSITIONAL_ONLY, default=None)],

        # Difference v3.4 vs v3.5!!!
        'setattr': [param('object', param.POSITIONAL_ONLY),
                    param('name', param.POSITIONAL_ONLY),
                    param('value', param.POSITIONAL_ONLY)],
        'sorted': [param('iterable', param.POSITIONAL_ONLY),
                   param('key', param.POSITIONAL_OR_KEYWORD, default=None),
                   param('reverse', param.POSITIONAL_OR_KEYWORD, default=None)],
        'str': [param('object', param.POSITIONAL_OR_KEYWORD)],
        'sum': [param('iterable', param.POSITIONAL_ONLY),
                param('start', param.POSITIONAL_ONLY, default=0)],
        'tuple': [param('iterable', param.POSITIONAL_ONLY, default=None)],
        'type': [param('object', param.POSITIONAL_ONLY)],
        'vars': [param('object', param.POSITIONAL_ONLY)],

        # int

        # str
        'str.center': [param('width', param.POSITIONAL_ONLY),
                       param('fillchar', param.POSITIONAL_ONLY, default=" ")],

        # list
        'list.append': [param('object', param.POSITIONAL_ONLY)],
        'list.count': [param('value', param.POSITIONAL_ONLY)],

        # dict

        # numpy
        'numpy.array': [param('object', param.POSITIONAL_OR_KEYWORD),
                        param('dtype', param.POSITIONAL_OR_KEYWORD, default=None),
                        param('copy', param.POSITIONAL_OR_KEYWORD, default=True),
                        param('order', param.POSITIONAL_OR_KEYWORD, default=None),
                        param('subok', param.POSITIONAL_OR_KEYWORD, default=False),
                        param('ndmin', param.POSITIONAL_OR_KEYWORD, default=0)],
        'numpy.random.seed': [param('seed', param.POSITIONAL_OR_KEYWORD, default=None)],
        'numpy.random.rand': [param('d0', param.POSITIONAL_ONLY, default=None),
                              param('d1', param.POSITIONAL_ONLY, default=None),
                              param('d2', param.POSITIONAL_ONLY, default=None),
                              param('d3', param.POSITIONAL_ONLY, default=None),
                              param('d4', param.POSITIONAL_ONLY, default=None),
                              param('d5', param.POSITIONAL_ONLY, default=None),
                              param('d6', param.POSITIONAL_ONLY, default=None)],
        'numpy.random.randint': [param('low', param.POSITIONAL_OR_KEYWORD),
                                 param('high', param.POSITIONAL_OR_KEYWORD, default=None),
                                 param('size', param.POSITIONAL_OR_KEYWORD, default=None),
                                 param('dtype', param.POSITIONAL_OR_KEYWORD, default='l')],

        # others
        'math.radians': [param('x', param.POSITIONAL_ONLY)]
    }
    return(manual_sigs)






