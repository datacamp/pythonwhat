from pythonwhat.Test import StringContainsTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.tasks import getOutputInProcess

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

test_output_contains = has_output

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
