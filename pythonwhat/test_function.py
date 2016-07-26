import ast

from pythonwhat.Test import Test, DefinedTest, EqualTest, EquivalentTest, BiggerTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Fb import Feedback
from pythonwhat.utils import get_ord, get_num
import inspect

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
    student_env, solution_env = state.student_env, state.solution_env

    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)

    state.extract_function_calls()
    solution_calls = state.solution_function_calls
    student_calls = state.student_function_calls
    student_mappings = state.student_mappings

    # for messaging purposes: replace with original alias or import again.
    stud_name = name
    if "." in stud_name:
        student_mappings_rev = {v: k for k, v in student_mappings.items()}
        els = name.split(".")
        front_part = ".".join(els[0:-1])
        if front_part in student_mappings_rev.keys():
                stud_name = student_mappings_rev[front_part] + "." + els[-1]

    if not_called_msg is None:
        if index == 0:
            not_called_msg = "Have you called `%s()`?" % stud_name
        else:
            not_called_msg = ("The system wants to check the %s call of `%s()`, " +
                "but hasn't found it; have another look at your code.") % (get_ord(index + 1), stud_name)

    if name not in solution_calls:
        raise NameError("%r not in solution environment" % name)

    rep.do_test(DefinedTest(name, student_calls, not_called_msg))
    if rep.failed_test:
        return

    rep.do_test(BiggerTest(len(student_calls[name]), index, not_called_msg))
    if rep.failed_test:
        return

    args_solution, keyw_solution = solution_calls[name][index]
    keyw_solution = {keyword.arg: keyword.value for keyword in keyw_solution}


    if args is None:
        args = list(range(len(args_solution)))

    if keywords is None:
        keywords = list(keyw_solution.keys())

    def build_test(stud, sol, feedback_msg, add_more):
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
            eq_map[eq_condition](eval_student, eval_solution, Feedback(feedback_msg, stud)))


    if len(args) > 0 or len(keywords) > 0:

        success = None

        # Get all options (some function calls may be blacklisted)
        call_indices = state.get_options(name, list(range(len(student_calls[name]))), index)

        feedback = None

        for call_ind in call_indices:
            args_student, keyw_student = student_calls[name][call_ind]
            keyw_student = {keyword.arg: keyword.value for keyword in keyw_student}

            success = True
            start = "Have you specified all required arguments inside `%s()` function?" % stud_name

            if len(args) > 0 and (max(args) >= len(args_student)):
                if feedback is None:
                    if not args_not_specified_msg:
                        n = max(args)
                        if n == 0:
                            args_not_specified_msg = start + " You should specify one argument without naming it."
                        else:
                            args_not_specified_msg = start + (" You should specify %s arguments without naming them." % get_num(n + 1))
                    feedback = Feedback(args_not_specified_msg)
                success = False
                continue

            setdiff = list(set(keywords) - set(keyw_student.keys()))
            if len(setdiff) > 0:
                if feedback is None:
                    if not args_not_specified_msg:
                        args_not_specified_msg = start + " You should specify the keyword `%s` explicitly by its name." % setdiff[0]
                    feedback = Feedback(args_not_specified_msg)
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
                arg_feedback_msg = feedback_msg + (" The %s argument seems to be incorrect." % get_ord(arg + 1))
                if incorrect_msg is None:
                    test = build_test(arg_student, arg_solution, arg_feedback_msg, add_more = True)
                else:
                    test = build_test(arg_student, arg_solution, incorrect_msg, add_more = False)
                
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
                    key_feedback_msg = feedback_msg + (" Keyword `%s` seems to be incorrect." % key)
                    if incorrect_msg is None:
                        test = build_test(key_student, key_solution, key_feedback_msg, add_more = True)
                    else:
                        test = build_test(key_student, key_solution, incorrect_msg, add_more = False)
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



def get_function_signature(fun):

    if (inspect.isclass(fun) or
        inspect.ismethod(fun) or
        inspect.isfunction(fun)):
        arginfo = inspect.signature(fun)
        import pdb; pdb.set_trace()
        print(arginfo)
    elif inspect.isbuiltin(fun):
        print("Builtin!")

