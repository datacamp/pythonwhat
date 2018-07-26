from pythonwhat.tasks import getResultInProcess, getOutputInProcess, getErrorInProcess, ReprFail, isDefinedInProcess, getOptionFromProcess, ReprFail, UndefinedValue
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test, EqualTest
from pythonwhat.Feedback import Feedback
from pythonwhat import utils
from functools import partial
import re
import copy
import ast

evalCalls = {'value':  getResultInProcess,
             'output': getOutputInProcess,
             'error':  getErrorInProcess}

def has_part(name, msg, state=None, fmt_kwargs=None, index=None):
    rep = Reporter.active_reporter
    d = {'sol_part': state.solution_parts,
         'stu_part': state.student_parts,
         **fmt_kwargs
         }

    try: 
        part = state.student_parts[name]
        if index is not None:
            if isinstance(index, list):
                for ind in index:
                    part = part[ind]
            else:
                part = part[index]
        if part is None: raise KeyError
    except (KeyError, IndexError):
        _msg = state.build_message(msg, d)
        rep.do_test(Test(Feedback(_msg, state)))

    return state


def has_equal_part(name, msg, state):
    rep = Reporter.active_reporter
    d = {'stu_part': state.student_parts,
         'sol_part': state.solution_parts,
         'name': name}

    _msg = state.build_message(msg, d)
    rep.do_test(EqualTest(d['stu_part'][name], d['sol_part'][name], Feedback(_msg, state)))

    return state

# TODO: shouldn't have to hardcode message
def has_equal_part_len(name, unequal_msg, state=None):
    """Verify that a part that is zoomed in on has equal length.

    Typically used in the context of ``check_function_def()``

    Arguments:
        name (str): name of the part for which to check the length to the corresponding part in the solution.
        unequal_msg (str): Message in case the lengths do not match.
        state (State): state as passed by the SCT chain. Don't specify this explicitly.

    :Examples:

        Student and solution code::

            def shout(word):
                return word + '!!!'

        SCT that checks number of arguments::

            Ex().check_function_def('shout').has_equal_part_len('args', 'not enough args!')

    """
    rep = Reporter.active_reporter
    d = dict(stu_len = len(state.student_parts[name]),
             sol_len = len(state.solution_parts[name]))

    if d['stu_len'] != d['sol_len']:
        _msg = state.build_message(unequal_msg, d)
        rep.do_test(Test(Feedback(_msg, state)))

    return state

## Expression tests -----------------------------------------------------------

def has_equal_ast(incorrect_msg=None,
                  code=None,
                  exact=True,
                  append=None,
                  state=None):
    """Test whether abstract syntax trees match between the student and solution code.

    ``has_equal_ast()`` can be used in two ways:

    * As a robust version of ``has_code()``. By setting ``code``, you can look for the AST representation of ``code`` in the student's submission.
    * As an expression-based check when using more advanced SCT chain, e.g. to compare the equality of expressions to set function arguments.

    Args:
        incorrect_msg: message displayed when ASTs mismatch. When you specify ``code`` yourself, you have to specify this.
        code: optional code to use instead of the solution AST
        exact: whether the representations must match exactly. If false, the solution AST
               only needs to be contained within the student AST (similar to using test student typed).

    :Example:

        Student and Solution Code::

            dict(a = 'value').keys()

        SCT::

            # all pass
            Ex().has_equal_ast()
            Ex().has_equal_ast(code = "dict(a = 'value').keys()")
            Ex().has_equal_ast(code = "dict(a = 'value')", exact = False)

        Student and Solution Code::

            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])
            np.mean(arr)

        SCT::

            # Check underlying value of arugment a of np.mean:
            Ex().check_function('numpy.mean').check_args('a').has_equal_ast()

            # Only check AST equality of expression used to specify argument a:
            Ex().check_function('numpy.mean').check_args('a').has_equal_ast()

    """
    rep = Reporter.active_reporter

    if code and incorrect_msg is None:
        raise ValueError("If you manually specify the code to match inside has_equal_ast(), you have to explicitly set the `incorrect_msg` arugment.")

    if append is None: # if not specified, set to False if incorrect_msg was manually specified
        append = incorrect_msg is None
    if incorrect_msg is None:
        incorrect_msg = "__JINJA__:Expected `{{sol_str}}`, but got `{{stu_str}}`."

    def parse_tree(tree):
        # get contents of module.body if only 1 element
        crnt = tree.body[0] if isinstance(tree, ast.Module) and len(tree.body) == 1 else tree

        # remove Expr if it exists
        return ast.dump(crnt.value if isinstance(crnt, ast.Expr) else crnt)

    stu_rep = parse_tree(state.student_tree)
    sol_rep = parse_tree(state.solution_tree if not code else ast.parse(code))

    fmt_kwargs = {
        'sol_str': state.solution_code if not code else code,
        'stu_str': state.student_code
    }

    _msg = state.build_message(incorrect_msg, fmt_kwargs, append=append)

    if exact:
        rep.do_test(EqualTest(stu_rep, sol_rep, Feedback(_msg, state)))
    elif not sol_rep in stu_rep:
        rep.do_test(Test(Feedback(_msg, state)))

    return state

DEFAULT_INCORRECT_MSG="__JINJA__:Expected {{test_desc}}`{{sol_eval}}`, but got `{{stu_eval}}`."
DEFAULT_ERROR_MSG="__JINJA__:Running {{'it' if parent['part'] else 'the higlighted expression'}} generated an error: `{{stu_str}}`."
DEFAULT_ERROR_MSG_INV="__JINJA__:Running {{'it' if parent['part'] else 'the higlighted expression'}} didn't generate an error, but it should!"
DEFAULT_UNDEFINED_NAME_MSG="__JINJA__:Running {{'it' if parent['part'] else 'the higlighted expression'}} should define a variable `{{name}}` without errors, but it doesn't."
DEFAULT_INCORRECT_NAME_MSG="__JINJA__:Are you sure you assigned the correct value to `{{name}}`?"
def has_expr(incorrect_msg=None,
             error_msg=None,
             undefined_msg=None,
             append=None,
             extra_env=None,
             context_vals=None,
             pre_code=None,
             expr_code=None,
             name=None,
             copy=True,
             func=None,
             state=None,
             test=None):

    if append is None: # if not specified, set to False if incorrect_msg was manually specified
        append = incorrect_msg is None
    if incorrect_msg is None:
        incorrect_msg = DEFAULT_INCORRECT_MSG if name is None else DEFAULT_INCORRECT_NAME_MSG
    if undefined_msg is None:
        undefined_msg = DEFAULT_UNDEFINED_NAME_MSG
    if error_msg is None:
        error_msg = DEFAULT_ERROR_MSG_INV if test == 'error' else DEFAULT_ERROR_MSG

    rep = Reporter.active_reporter

    get_func = partial(evalCalls[test], 
                       extra_env = extra_env,
                       context_vals = context_vals,
                       pre_code = pre_code,
                       expr_code = expr_code,
                       name = name,
                       copy=copy,
                       do_exec = True if test == 'output' else False)

    eval_sol, str_sol = get_func(tree = state.solution_tree,
                                 process = state.solution_process,
                                 context = state.solution_context,
                                 env = state.solution_env)

    if (test == 'error') ^ isinstance(eval_sol, Exception):
        raise ValueError("Evaluating expression raised error in solution process (or not an error if testing for one). "
                         "Error: {} - {}".format(type(eval_sol), str_sol))
    if isinstance(eval_sol, ReprFail):
        raise ValueError("Couldn't figure out the value of a default argument: " + eval_sol.info)

    eval_stu, str_stu = get_func(tree = state.student_tree,
                                 process = state.student_process,
                                 context = state.student_context,
                                 env = state.student_env)

    # kwargs ---
    fmt_kwargs = {
        'stu_part': state.student_parts,
        'sol_part': state.solution_parts,
        'name': name, 'test': test,
        'test_desc': '' if test == 'value' else 'the %s ' % test
    }
    fmt_kwargs['stu_eval'] = utils.shorten_str(str(eval_stu))
    fmt_kwargs['sol_eval'] = utils.shorten_str(str(eval_sol))

    # tests ---
    # error in process
    if (test == 'error') ^ isinstance(eval_stu, Exception):
        fmt_kwargs['stu_str'] = str_stu
        _msg = state.build_message(error_msg, fmt_kwargs, append=append)
        feedback = Feedback(_msg, state)
        rep.do_test(Test(feedback))

    # name is undefined after running expression
    if isinstance(eval_stu, UndefinedValue):
        _msg = state.build_message(undefined_msg, fmt_kwargs, append=append)
        rep.do_test(Test(Feedback(_msg, state)))

    # test equality of results
    _msg = state.build_message(incorrect_msg, fmt_kwargs, append=append)
    rep.do_test(EqualTest(eval_stu, eval_sol, Feedback(_msg, state), func))

    return state



args_string = """

    Args:
        incorrect_msg (str): feedback message if the {0} of the expression in the solution
          doesn't match the one of the student. This feedback message will be expanded if it is used
          in the context of another check function, like ``check_if_else``.
        error_msg (str): feedback message if there was an error when running the targeted student code.
          Note that when testing for an error, this message is displayed when none is raised.
        undefined_msg (str): feedback message if the ``name`` argument is defined, but a variable
          with that name doesn't exist after running the targeted student code.
        extra_env (dict): set variables to the extra environment. They will update the student and solution environment in
          the active state before the student/solution code in the active state is ran. This argument should contain a
          dictionary with the keys the names of the variables you want to set, and the values are the values of these variables.
          You can also use ``set_env()`` for this.
        context_vals (list): set variables which are bound in a ``for`` loop to certain values.
          This argument is only useful when checking a for loop (or list comprehensions).
          It contains a list with the values of the bound variables.
          You can also use ``set_context()`` for this.
        pre_code (str): the code in string form that should be executed before the expression is executed.
          This is the ideal place to set a random seed, for example.
        expr_code (str): if this argument is set, the expression in the student/solution code will not
          be ran. Instead, the given piece of code will be ran in the student as well as the solution environment
          and the result will be compared.
        name (str): If this is specified, the {1} of running this expression after running the focused expression
          is returned, instead of the {1} of the focussed expression in itself. This is typically used to inspect the
          {1} of an object after executing the body of e.g. a ``for`` loop.
        copy (bool): whether to try to deep copy objects in the environment, such as lists, that could
          accidentally be mutated. Disable to speed up SCTs. Disabling may lead to cryptic mutation issues.
        func: custom binary function of form f(stu_result, sol_result), for equality testing.
    """

has_equal_value =  partial(has_expr, test = 'value')
has_equal_value.__doc__ = """Run targeted student and solution code, and compare returned value.

    When called on an SCT chain, ``has_equal_value()`` will execute the student and solution
    code that is 'zoomed in on' and compare the returned values.
    """ + args_string.format("returned value", "value") + """
    :Example:

        Student code and solution code::

            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])
            np.mean(arr)

        SCT::

            # Verify equality of arr:
            Ex().check_object('arr').has_equal_value()

            # Verify whether arr was correctly set in np.mean
            Ex().check_function('numpy.mean').check_args('a').has_equal_value()

            # Verify whether np.mean(arr) produced the same result
            Ex().check_function('numpy.mean').has_equal_value()

    """


has_equal_output = partial(has_expr, test = 'output')
has_equal_output.__doc__ = """Run targeted student and solution code, and compare output.

    When called on an SCT chain, ``has_equal_output()`` will execute the student and solution
    code that is 'zoomed in on' and compare the output.
    """ + args_string.format("output", "output")

has_equal_error  = partial(has_expr, test = 'error')
has_equal_error.__doc__ = """Run targeted student and solution code, and compare generated errors.

    When called on an SCT chain, ``has_equal_error()`` will execute the student and solution
    code that is 'zoomed in on' and compare the errors that they generate.
    """ + args_string.format("error", "error")

## Various has tests ----------------------------------------------------------

from pythonwhat.Test import StringContainsTest

def has_code(text,
             pattern=True,
             not_typed_msg=None,
             state=None):
    """Test the student code.

    Tests if the student typed a (pattern of) text. It is advised to use ``has_equal_ast()`` instead of ``has_code()``,
    as it is more robust to small syntactical differences that don't change the code's behavior.

    Args:
        text (str): the text that is searched for
        pattern (bool): if True (the default), the text is treated as a pattern. If False, it is treated as plain text.
        not_typed_msg (str): feedback message to be displayed if the student did not type the text.

    :Example:

        Student code and solution code::

            y = 1 + 2 + 3

        SCT::

            # Verify that student code contains pattern (not robust!!):
            Ex().has_code(r"1\s*\+2\s*\+3")

    """
    rep = Reporter.active_reporter

    if not not_typed_msg:
        if pattern:
            not_typed_msg = "Could not find the correct pattern in your code."
        else:
            not_typed_msg = "Could not find the following text in your code: %r" % text

    student_code = state.student_code

    _msg = state.build_message(not_typed_msg)
    rep.do_test(StringContainsTest(student_code, text, pattern, Feedback(_msg, state)))

    return state

from pythonwhat.Test import Test, DefinedCollTest, EqualTest

def has_import(name,
               same_as=True,
               not_imported_msg="__JINJA__:Did you import `{{pkg}}`?",
               incorrect_as_msg="__JINJA__:Did you import `{{pkg}}` as `{{alias}}`?",
               state=None):
    """Check whether code has certain import statement.

    Test whether an import statement is used the same in the student's environment as in the solution
    environment.

    Args:
        name (str): the name of the package that has to be checked.
        same_as (bool): if false, the alias of the package doesn't have to be the same. Defaults to True.
        not_imported_msg (str): feedback message when the package is not imported.
        incorrect_as_msg (str): feedback message if the alias is wrong.


    :Example:

        Student code::

            import numpy as np
            import pandas as pa

        Solution code::

            import numpy as np
            import pandas as pd

        SCT::

            Ex().has_import("numpy")  # pass
            Ex().has_import("pandas") # fail
            Ex().has_import("pandas", same_as = False) # pass

    """

    rep = Reporter.active_reporter

    student_imports = state.student_imports
    solution_imports = state.solution_imports

    if name not in solution_imports:
        raise NameError("The package you specified is not in the solution imports itself. %r not in solution imports" % name)

    fmt_kwargs = { 'pkg': name, 'alias': solution_imports[name] }

    _msg = state.build_message(not_imported_msg, fmt_kwargs)
    rep.do_test(DefinedCollTest(name, student_imports, _msg))

    if (same_as):
        _msg = state.build_message(incorrect_as_msg, fmt_kwargs)
        rep.do_test(EqualTest(solution_imports[name], student_imports[name], _msg))

    return state

def has_output(text,
               pattern=True,
               no_output_msg=None,
               state=None):
    """Search student output.

    Checks if the output contains a (pattern of) text.

    Args:
        text (str): the text that is searched for
        pattern (bool): if True (default), the text is treated as a pattern. If False, it is treated as plain text.
        no_output_msg (str): feedback message to be displayed if the output is not found.

    :Example:

        SCT::

            Ex().has_output(r'[H|h]i,*\\s+there!')

        Submissions::

            print("Hi, there!")     # pass
            print("hi  there!")     # pass
            print("Hello there")    # fail
    """
    rep = Reporter.active_reporter

    if not no_output_msg:
        no_output_msg = "You did not output the correct things."
        # raise ValueError("Inside has_output(), specify the `no_output_msg` manually.")

    student_output = state.raw_student_output

    _msg = state.build_message(no_output_msg)
    rep.do_test(
        StringContainsTest(
            student_output,
            text,
            pattern,
            _msg))

    return state

def has_printout(index,
                 not_printed_msg=None,
                 pre_code=None,
                 name=None,
                 copy=False,
                 state=None):
    """Check if the output of print() statement in the solution is in the output the student generated.

    This is more robust as ``Ex().check_function('print')`` initiated chains as students can use as many
    printouts as they want, as long as they do the correct one somewhere.

    .. note::

        When zooming in on parts of the student submission (with e.g. ``check_for_loop()``), we are not
        zooming in on the piece of the student output that is related to that piece of the student code.
        In other words, ``has_printout()`` always considers the entire student output.

    Args:
        index (int): index of the ``print()`` call in the solution whose output you want to search for in the student output.
        not_printed_msg (str): if specified, this overrides the default message that is generated when the output
          is not found in the student output.
        pre_code (str): Python code as a string that is executed before running the targeted student call.
          This is the ideal place to set a random seed, for example.
        copy (bool): whether to try to deep copy objects in the environment, such as lists, that could
          accidentally be mutated. Disabled by default, which speeds up SCTs.
        state (State): state as passed by the SCT chain. Don't specify this explicitly.

    :Example:

        Solution::

            print(1, 2, 3, 4)

        SCT::

            Ex().has_printout(0)

        Each of these submissions will pass::

            print(1, 2, 3, 4)
            print('1 2 3 4')
            print(1, 2, '3 4')
            print("random"); print(1, 2, 3, 4)
    """

    if not_printed_msg is None:
        not_printed_msg = "__JINJA__:Have you used `{{sol_call}}` to do the appropriate printouts?"

    try:
        sol_call_ast = state.solution_function_calls['print'][index]['node']
    except (KeyError, IndexError):
        raise ValueError("Using has_printout() with index {} expects that there is/are at least {} print() call(s) in your solution."
                         "Is that the case?".format(index, index+1))

    out_sol, str_sol = getOutputInProcess(
        tree = sol_call_ast,
        process = state.solution_process,
        context = state.solution_context,
        env = state.solution_env,
        pre_code = pre_code,
        copy = copy
    )

    sol_call_str = state.solution_tree_tokens.get_text(sol_call_ast)

    if isinstance(str_sol, Exception):
            raise ValueError("Evaluating the solution expression {} raised error in solution process."
                             "Error: {} - {}".format(sol_call_str, type(out_sol), str_sol))

    _msg = state.build_message(not_printed_msg, { 'sol_call': sol_call_str })

    has_output(out_sol.strip(), pattern = False, no_output_msg=_msg, state=state)

    return state

MC_VAR_NAME = "selected_option"

def has_chosen(correct, msgs, state=None):
    """Test multiple choice exercise.

    Test for a MultipleChoiceExercise. The correct answer (as an integer) and feedback messages
    are passed to this function.

    Args:
        correct (int): the index of the correct answer (should be an instruction). Starts at 1.
        msgs (list(str)): a list containing all feedback messages belonging to each choice of the
                          student. The list should have the same length as the number of instructions.
    """
    if not issubclass(type(correct), int):
        raise ValueError("correct should be an integer")

    rep = Reporter.active_reporter
    student_process = state.student_process
    if not isDefinedInProcess(MC_VAR_NAME, student_process):
        raise NameError("Option not available in the student process")
    else:
        selected_option = getOptionFromProcess(student_process, MC_VAR_NAME)
        if not issubclass(type(selected_option), int):
            raise ValueError("selected_option should be an integer")

        if selected_option < 1 or correct < 1:
            raise ValueError(
                "selected_option and correct should be greater than zero")

        if selected_option > len(msgs) or correct > len(msgs):
            raise ValueError("there are not enough feedback messages defined")

        feedback_msg = msgs[selected_option - 1]

        rep.success_msg = msgs[correct - 1]

        rep.do_test(EqualTest(selected_option, correct, feedback_msg))
