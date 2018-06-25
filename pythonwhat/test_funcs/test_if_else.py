from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import check_part, check_node, multi

from functools import partial, update_wrapper

MSG_MISSING = "FMT:The system wants to check the {typestr}, but it hasn't found it. Have another look at your code."
MSG_PREPEND = "FMT:Check the {typestr}. "

def test_if_else(index=1,
                 test=None,
                 body=None,
                 orelse=None,
                 expand_message=True,
                 use_if_exp=False,
                 state=None):
    """Test parts of the if statement.

    This test function will allow you to extract parts of a specific if statement and perform a set of tests
    specifically on these parts. A for loop consists of three potential parts: the condition test, :code:`test`,
    which specifies the condition of the if statement, the :code:`body`, which is what's executed if the condition is
    True and a else part, :code:`orelse`, which will be executed if the condition is not True.::

        if 5 == 3:
            print("success")
        else:
            print("fail")

    Has :code:`5 == 3` as the condition test, :code:`print("success")` as the body and :code:`print("fail")` as the else part.

    Args:
      index (int): index of the function call to be checked. Defaults to 1.
      test: this argument holds the part of code that will be ran to check the condition test of the if statement.
        It should be passed as a lambda expression or a function definition. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the condition test of
        the if statement.
      body: this argument holds the part of code that will be ran to check the body of the if statement.
        It should be passed as a lambda expression or a function definition. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the body of
        the if statement.
      orelse: this argument holds the part of code that will be ran to check the else part of the if statement.
        It should be passed as a lambda expression or a function definition. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the else part of
        the if statement.
      expand_message (bool): if true, feedback messages will be expanded with :code:`in the ___ of the if statement on
        line ___`. Defaults to True. If False, :code:`test_if_else()` will generate no extra feedback.

    :Example:

        Student code::

            a = 12
            if a > 3:
                print('test %d' % a)

        Solution code::

            a = 4
            if a > 3:
                print('test %d' % a)

        SCT::

            test_if_else(1,
                body = test_expression_output(
                        extra_env = { 'a': 5 }
                        incorrect_msg = "Print out the correct things"))

        This SCT will pass as :code:`test_expression_output()` is ran on the body of the if statement and it will output
        the same thing in the solution as in the student code.
    """

    # get state with specific if block
    node_name = 'if_exps' if use_if_exp else 'if_elses'
    # TODO original typestr for check_node used if rather than `if`
    state = check_node(node_name, index-1, "{ordinal} if statement", MSG_MISSING, MSG_PREPEND if expand_message else "", state=state)

    # run sub tests
    multi(test, state = check_part('test', 'condition', expand_msg=None if expand_message else "", state=state))
    multi(body, state = check_part('body', 'body', expand_msg=None if expand_message else "", state=state))
    multi(orelse, state = check_part('orelse', 'else part', expand_msg=None if expand_message else "", state=state))


test_if_exp = partial(test_if_else, use_if_exp = True)
# update test_if_exp function signature (docstring, etc..)
update_wrapper(test_if_exp, test_if_else)
test_if_exp.__name__ = 'test_if_exp'
