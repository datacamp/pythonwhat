from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import check_part, check_node, multi

MSG_MISSING = "FMT:Define more while loops."
MSG_PREPEND = "FMT:Check the {typestr}. "

def test_while_loop(index=1,
                    test=None,
                    body=None,
                    orelse=None,
                    expand_message=True,
                    state=None):
    """Test parts of the while loop.

    This test function will allow you to extract parts of a specific while loop and perform a set of tests
    specifically on these parts. A while loop generally consists of two parts: the condition test, :code:`test`,
    which is the condition that is tested each loop, and the :code:`body`. A for while can have a else part as well,
    :code:`orelse`, but this is almost never used.::

        a = 10
        while a < 5:
            print(a)
            a -= 1

    Has :code:`a < 5` as the condition test and `print(i)` as the body.

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
        expand_message (bool): if true, feedback messages will be expanded with :code:`in the ___ of the while loop on
          line ___`. Defaults to True. If False, `test_for_loop()` will generate no extra feedback.

    :Example:

        Student code::

            a = 10
            while a < 5:
                print(a)
                a -= 1

        Solution code::

            a = 20
            while a < 5:
                print(a)
                a -= 1

        SCT::

            test_while_loop(1,
                    test = test_expression_result({"a": 5}),
                    body = test_expression_output({"a": 5}))

      This SCT will evaluate to True as condition test will have thes same result in student
      and solution code and `test_exression_output()` will pass on the body code.
    """

    state = check_node('whiles', index-1, "{ordinal} while loop", MSG_MISSING, MSG_PREPEND if expand_message else "", state=state)

    expand_msg = None if expand_message else ""
    multi(test, state = check_part('test', 'condition', expand_msg=expand_msg, state=state))
    multi(body, state = check_part('body', 'body', expand_msg=expand_msg, state=state))
    multi(orelse, state = check_part('orelse', 'else part', expand_msg=expand_msg, state=state))
