import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test


def test_while_loop(index=1,
                    test=None,
                    body=None,
                    orelse=None,
                    expand_message=True):
    """Test parts of the for loop.

    This test function will allow you to extract parts of a specific for loop and perform a set of tests
    specifically on these parts. A for loop consists of two parts: the sequence, `for_iter`, which is the
    values over which are looped, and the `body`. A for loop can have a else part as well, `orelse`, but
    this is almost never used.

        ``for i in range(10):``
        ``    print(i)``

    Has `range(10)` as the sequence and `print(i)` as the body.

    Example:
      student_code
        | ``for i in range(10):``
        | ``    print(i)``
      solution_code
        | ``for n in range(10):``
        | ``    print(n)``
      sct
        | ``test_for_loop(1,``
        | ``              for_iter = lamdba: test_function("range"),``
        | ``              body = lambda: test_expression_output(context_val = [5])``
      This SCT will evaluate to TRUE as the function `"range"` is used in the sequence and the function
      `test_exression_output()` will pass on the body code.

    Args:
      index (int): index of the function call to be checked. Defaults to 1.
      for_iter: this argument holds the part of code that will be ran to check the sequence of the for loop.
        It should be passed as a lambda expression or a function definition. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the sequence part of
        the for loop.
      body: this argument holds the part of code that will be ran to check the body of the for loop.
        It should be passed as a lambda expression or a function definition. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the body of
        the for loop.
      orelse: this argument holds the part of code that will be ran to check the else part of the for loop.
        It should be passed as a lambda expression or a function definition. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the else part of
        the for loop.
      expand_message (bool): if true, feedback messages will be expanded with `in the ___ of the for loop on
        line ___`. Defaults to True. If False, `test_for_loop()` will generate no extra feedback.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_while_loop")

    index = index - 1

    student_env, solution_env = state.student_env, state.solution_env

    state.extract_while_calls()
    student_whiles = state.student_while_calls
    solution_whiles = state.solution_while_calls

    try:
        lineno_student, test_student, body_student, orelse_student = student_whiles[
            index]
    except:
        rep.do_test(Test("Define more `while` loops."))
        return

    lineno_solution, test_solution, body_solution, orelse_solution = solution_whiles[
        index]

    def sub_test(closure, subtree_student, subtree_solution, incorrect_part):
        if closure:
            failed_before = rep.failed_test
            child = state.to_child_state(subtree_student, subtree_solution)
            closure()
            child.to_parent_state()
            if expand_message and (failed_before is not rep.failed_test):
                rep.feedback_msg = rep.feedback_msg + " in the " + incorrect_part + \
                    " of the `while` loop on line " + str(lineno_student) + "."

    sub_test(test, test_student, test_solution, "condition")
    sub_test(body, body_student, body_solution, "body")
    sub_test(orelse, orelse_student, orelse_solution, "else part")
