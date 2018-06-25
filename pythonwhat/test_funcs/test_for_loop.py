from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import check_part, check_node, multi

from functools import partial

MSG_MISSING = "FMT:Define more for loops."
MSG_PREPEND = "FMT:Check the {typestr}. "

def test_for_loop(index=1,
                  for_iter=None,
                  body=None,
                  orelse=None,
                  expand_message=True,
                  state=None):
    """Test parts of the for loop.

    This test function will allow you to extract parts of a specific for loop and perform a set of tests
    specifically on these parts. A for loop consists of two parts: the sequence, `for_iter`, which is the
    values over which are looped, and the `body`. A for loop can have a else part as well, `orelse`, but
    this is almost never used.::

        for i in range(10):
            print(i)

    Has :code:`range(10)` as the sequence and :code:`print(i)` as the body.

    Args:
      index (int): index of the function call to be checked. Defaults to 1.
      for_iter: this argument holds the part of code that will be ran to check the sequence of the for loop.
        It should be passed as a lambda expression or a function. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the sequence part of
        the for loop.
      body: this argument holds the part of code that will be ran to check the body of the for loop.
        It should be passed as a lambda expression or a function. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the body of
        the for loop.
      orelse: this argument holds the part of code that will be ran to check the else part of the for loop.
        It should be passed as a lambda expression or a function. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the else part of
        the for loop.
      expand_message (bool): if true, feedback messages will be expanded with :code:`in the ___ of the for loop on
        line ___`. Defaults to True. If False, :code:`test_for_loop()` will generate no extra feedback.

    :Example:
        Student code::

            for i in range(10):
                print(i)

        Solution code::

            for n in range(10):
                print(n)

        SCT::

            test_for_loop(1,
                for_iter = test_function("range"),
                body = test_expression_output(context_val = [5])

        This SCT will evaluate to True as the function :code:`range` is used in the sequence and the function
        :code:`test_exression_output()` will pass on the body code.
    """
    state = check_node('for_loops', index-1, "{ordinal} for loop", MSG_MISSING, MSG_PREPEND, state=state)

    # TODO for_iter is a level up, so shouldn't have targets set, but this is done is check_node
    multi(for_iter, state = check_part('iter', 'sequence part', expand_msg=None if expand_message else "", state=state))
    multi(body,     state = check_part('body', 'body', expand_msg=None if expand_message else "", state=state))
    multi(orelse,   state = check_part('orelse', 'else part', expand_msg=None if expand_message else "", state=state))

