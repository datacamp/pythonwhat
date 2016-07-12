import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test
from pythonwhat.utils import get_ord
from pythonwhat.feedback import Feedback

def test_while_loop(index=1,
                    test=None,
                    body=None,
                    orelse=None,
                    expand_message=True):
    """Test parts of the while loop.

    This test function will allow you to extract parts of a specific while loop and perform a set of tests
    specifically on these parts. A while loop generally consists of two parts: the condition test, `test`,
    which is the condition that is tested each loop, and the `body`. A for while can have a else part as well,
    `orelse`, but this is almost never used.
        | ``a = 10``
        | ``while a < 5:``
        |     ``print(a)``
        |     ``a -= 1``

    Has `a < 5` as the condition test and `print(i)` as the body.

    Args:
        index (int): index of the function call to be checked. Defaults to 1.
        test: this argument holds the part of code that will be ran to check the condition test of the while loop.
          It should be passed as a lambda expression or a function definition. The functions that are ran should
          be other pythonwhat test functions, and they will be tested specifically on only the condition test of
          the while loop.
        body: this argument holds the part of code that will be ran to check the body of the while loop.
          It should be passed as a lambda expression or a function definition. The functions that are ran should
          be other pythonwhat test functions, and they will be tested specifically on only the body of
          the while loop.
        orelse: this argument holds the part of code that will be ran to check the else part of the while loop.
          It should be passed as a lambda expression or a function definition. The functions that are ran should
          be other pythonwhat test functions, and they will be tested specifically on only the else part of
          the while loop.
        expand_message (bool): if true, feedback messages will be expanded with `in the ___ of the while loop on
          line ___`. Defaults to True. If False, `test_for_loop()` will generate no extra feedback.

    Examples:
        Student code

        | ``a = 10``
        | ``while a < 5:``
        |     ``print(a)``
        |     ``a -= 1``

        Solution code

        | ``a = 20``
        | ``while a < 5:``
        |     ``print(a)``
        |     ``a -= 1``

        SCT

        | ``test_while_loop(1,``
        |     ``test = lamdba: test_expression_result({"a": 5}),``
        |     ``body = lambda: test_expression_output({"a": 5}))``

      This SCT will evaluate to True as condition test will have thes same result in student
      and solution code and `test_exression_output()` will pass on the body code.
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
        test_student, body_student, orelse_student = student_whiles[index]
    except:
        rep.do_test(Test("Define more `while` loops."))
        return

    test_solution, body_solution, orelse_solution = solution_whiles[index]

    def sub_test(closure, subtree_student, subtree_solution, incorrect_part):
        if closure:
            failed_before = rep.failed_test
            child = state.to_child_state(subtree_student, subtree_solution)
            closure()
            child.to_parent_state()
            if expand_message and (failed_before is not rep.failed_test):
                rep.feedback = Feedback(rep.feedback.message + " in the " + incorrect_part + \
                    " of the " + get_ord(index + 1) + " `while` loop.")

    sub_test(test, test_student, test_solution, "condition")
    sub_test(body, body_student, body_solution, "body")
    sub_test(orelse, orelse_student, orelse_solution, "else part")
