from pythonwhat.check_funcs import check_part, check_node, multi
from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import check_node, check_part, check_part_index, call, fix_format, stringify, with_context
from pythonwhat.check_logic import multi
from pythonwhat.has_funcs import has_equal_part_len, has_equal_part, has_equal_value, has_equal_output
from pythonwhat.check_has_context import has_context
from functools import partial, update_wrapper
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, Test
from pythonwhat import utils

def test_if_else(index=1,
                 test=None,
                 body=None,
                 orelse=None,
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
    state = check_node('if_elses', index-1, typestr='{{ordinal}} if expression', state=state)
    multi(test, state = check_part('test', 'condition', state=state))
    multi(body, state = check_part('body', 'body', state=state))
    multi(orelse, state = check_part('orelse', 'else part', state=state))

def test_for_loop(index=1,
                  for_iter=None,
                  body=None,
                  orelse=None,
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
    state = check_node('for_loops', index-1, "{{ordinal}} for loop", state=state)

    multi(for_iter, state = check_part('iter', 'sequence part', state=state))
    multi(body,     state = check_part('body', 'body', state=state))
    multi(orelse,   state = check_part('orelse', 'else part', state=state))

def test_while_loop(index=1,
                    test=None,
                    body=None,
                    orelse=None,
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
    state = check_node('whiles', index-1, "{{ordinal}} while loop", state=state)
    multi(test, state = check_part('test', 'condition', state=state))
    multi(body, state = check_part('body', 'body', state=state))
    multi(orelse, state = check_part('orelse', 'else part', state=state))


def test_function_definition(name,
                             arg_names=True,
                             arg_defaults=True,
                             body=None,
                             results=None,
                             outputs=None,
                             errors=None,
                             not_called_msg=None,
                             nb_args_msg=None,
                             other_args_msg=None,
                             arg_names_msg=None,
                             arg_defaults_msg=None,
                             wrong_result_msg=None,
                             wrong_output_msg=None,
                             no_error_msg=None,
                             wrong_error_msg=None,
                             state=None):
    """Test a function definition.

    This function helps you test a function definition. Generally four things can be tested:
        1) The argument names of the function (including if the correct defaults are used)
        2) The body of the functions (does it output correctly, are the correct functions used)
        3) The return value with a certain input
        4) The output value with a certain input
        5) Whether certain inputs generate an error and what type of error

    Custom feedback messages can be set for all these parts, default messages are generated
    automatically if none are set.

    Args:
        name (str): the name of the function definition to be tested.
        arg_names (bool): if True, the argument names will be tested, if False they won't be tested. Defaults
            to True.
        arg_defaults (bool): if True, the default values of the arguments will be tested, if False they won't
            be tested. Defaults to True.
        body: this arguments holds the part of the code that will be ran to check the body of the function
            definition. It should be passed as a lambda expression or a function. The functions that are
            ran should be other pythonwhat test functions, and they will be tested specifically on only the
            body of the for loop. Defaults to None.
        results (list(list)): a list of lists representing arguments that should be passed to the defined
            function. These arguments are passed to the function in the student environment and the solution
            environment, the results (what's returned) are compared.
        outputs (list(list)): a list of lists representing arguments that should be passed to the defined
            function. These arguments are passed to the function in the student environment and the solution
            environment, the outpus are compared.
        errors (list(list)): a list of lists representing arguments that should be passed to the defined
            function. These arguments are passed to the function in the student environment and the solution
            environment, the errors they generate are compared.
        not_called_msg (str): message if the function is not defined.
        nb_args_msg (str): message if the number of arguments do not matched.
        arg_names_msg (str): message if the argument names do not match.
        arg_defaults_msg (str): message if the argument default values do not match.
        wrong_result_msg (str): message if one of the tested function calls' result did not match.
        wrong_output_msg (str): message if one of the tested functions calls' output did not match.
        no_error_msg (str): message if one of the tested function calls' result did not generate an error.
        wrong_error_msg (str): message if the error that one of the tested function calls generated did not match.

    :Example:

        Student code::

            def shout( word, times = 3):
                shout_word = not_word + '???'
                print( shout_word )
                return word * times

        Solution code::

            def shout( word = 'help', times = 3 ):
                shout_word = word + '!!!'
                print( shout_word )
                return word * times

        SCT::

            test_function_definition('shout')                          # fail
            test_function_definition('shout', arg_defaults = False)    # pass
            test_function_definition('shout', arg_defaults = False,    # fail
                                            outputs = [('help')])    

            test_function_definition('shout', arg_defaults = False,    # pass
                                            results = [('help', 2)]) 

            test_function_definition('shout', args_defaults = False    # pass
                    body = test_function('print', args = []]))
    """

    # what the function will be referred to as
    child = check_node('function_defs', name, 'definition of `{{index}}()`', state=state)

    test_args(arg_names, arg_defaults, 
              nb_args_msg, arg_names_msg, arg_defaults_msg,
              child)

    multi(body, state=check_part('body', "", state=child))

    # Test function calls -----------------------------------------------------

    for el in (results or []):
        el = fix_format(el)
        call(el, 'value',
                incorrect_msg = wrong_result_msg,
                error_msg = wrong_result_msg,
                argstr = '`{}{}`'.format(name, stringify(el)),
                state=child)

    for el in (outputs or []):
        el = fix_format(el)
        call(el, 'output',
                incorrect_msg = wrong_output_msg,
                error_msg = wrong_output_msg,
                argstr = '`{}{}`'.format(name, stringify(el)),
                state=child)

    for el in (errors or []):
        el = fix_format(el)
        call(el, 'error',
                incorrect_msg = wrong_error_msg,
                error_msg = no_error_msg,
                argstr = '`{}{}`'.format(name, stringify(el)),
                state=child)


def test_args(arg_names, arg_defaults, 
              nb_args_msg, arg_names_msg, arg_defaults_msg, 
              child):

    MSG_NUM_ARGS = "You should define {{parent[typestr]}} with {{sol_len}} arguments, instead got {{stu_len}}."
    MSG_BAD_ARG_NAME = "The {{parent[ordinal]}} {{parent[part]}} should be called `{{sol_part[name]}}`, instead got `{{stu_part[name]}}`."
    MSG_BAD_DEFAULT = "The {{parent[part]}} `{{stu_part[name]}}` should have no default."
    MSG_INC_DEFAULT = "The {{parent[part]}} `{{stu_part[name]}}` does not have the correct default."

    MSG_NO_VARARG = "Have you specified an argument to take a `*` argument and named it `{{sol_part['*args'][name]}}`?"
    MSG_NO_KWARGS = "Have you specified an argument to take a `**` argument and named it `{{sol_part['**kwargs'][name]}}`?"
    MSG_VARARG_NAME = "Have you specified an argument to take a `*` argument and named it `{{sol_part[name]}}`?"
    MSG_KWARG_NAME = "Have you specified an argument to take a `**` argument and named it `{{sol_part[name]}}`?"

    if arg_names or arg_defaults:
        # test number of args
        has_equal_part_len('_spec1_args', nb_args_msg or MSG_NUM_ARGS, state=child)

        # iterate over each arg, testing name and default
        for ii in range(len(child.solution_parts['_spec1_args'])):
            # get argument state
            arg_state = check_part_index('_spec1_args', ii, 'argument', "NO MISSING MSG", state=child)
            # test exact name
            has_equal_part('name', arg_names_msg or MSG_BAD_ARG_NAME, arg_state)

            if arg_defaults:
                # test whether is default
                has_equal_part('is_default', arg_defaults_msg or MSG_BAD_DEFAULT, arg_state)
                # test default value, use if to prevent running a process no default
                if arg_state.solution_parts['is_default']:
                    has_equal_value(incorrect_msg = arg_defaults_msg or MSG_INC_DEFAULT, append=True, state=arg_state)

        # test *args and **kwargs
        if child.solution_parts['*args']:
            vararg = check_part('*args', "", missing_msg=MSG_NO_VARARG, state=child)
            has_equal_part('name', MSG_VARARG_NAME, state=vararg)
        
        if child.solution_parts['**kwargs']:
            kwarg = check_part('**kwargs', "", missing_msg=MSG_NO_KWARGS, state=child)
            has_equal_part('name', MSG_KWARG_NAME, state=kwarg)


def test_expression_result(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           expr_code=None,
                           pre_code=None,
                           error_msg=None,
                           state=None,
                           **kwargs):
    has_equal_value(incorrect_msg=incorrect_msg,
                    error_msg=error_msg,
                    extra_env = extra_env,
                    context_vals=context_vals,
                    expr_code=expr_code,
                    pre_code=pre_code,
                    state = state, **kwargs)


def test_expression_output(extra_env=None,
                           context_vals=None,
                           incorrect_msg=None,
                           eq_condition="equal",
                           expr_code=None,
                           pre_code=None,
                           state=None,
                           **kwargs):
    has_equal_output(incorrect_msg = incorrect_msg,
                     extra_env = extra_env,
                     context_vals=context_vals,
                     expr_code=expr_code,
                     pre_code=pre_code,
                     state = state,
                     **kwargs)

def test_object_after_expression(name,
                                 extra_env=None,
                                 context_vals=None,
                                 undefined_msg=None,
                                 incorrect_msg=None,
                                 expr_code=None,
                                 pre_code=None,
                                 state=None,
                                 **kwargs):
    state.highlight = state.student_object_assignments.get(name, {}).get('highlight')
    has_equal_value(
            incorrect_msg = incorrect_msg,
            error_msg = undefined_msg,
            undefined_msg = undefined_msg,
            extra_env=extra_env,
            context_vals=context_vals,
            pre_code=pre_code,
            name = name,
            expr_code = expr_code,
            state=state,
            **kwargs)

def test_with(index,
              context_vals=False, # whether to check number of context vals
              context_tests=None, # check on context expressions
              body=None,
              undefined_msg=None,
              context_vals_len_msg=None,
              context_vals_msg=None,
              state=None):
    """Test a with statement.
with open_file('...') as bla:

    [ open_file('...').__enter__() ]


with open_file('...') as file:
    [ ]

    """

    MSG_NUM_CTXT = "Make sure to use the correct number of context variables. It seems you defined too many."
    MSG_NUM_CTXT2 = "Make sure to use the correct number of context variables. It seems you defined too little."
    MSG_CTXT_NAMES = "Make sure to use the correct context variable names. Was expecting `{{sol_vars}}` but got `{{stu_vars}}`."

    check_with = partial(check_node, 'withs', index-1, "{{ordinal}} `with` statement", state=state)

    child =  check_with()
    child2 = check_with()

    if context_vals:
        # test context var names ----
        has_context(incorrect_msg=context_vals_msg or MSG_CTXT_NAMES, exact_names = True, state=child)

        # test num context vars ----
        has_equal_part_len('context', MSG_NUM_CTXT, state=child)
        
    
    # Context sub tests ----
    if context_tests and not isinstance(context_tests, list): context_tests = [context_tests]

    for i, context_test in enumerate(context_tests or []):
        # partial the substate check, because the function uses two prepended messages
        check_context = partial(check_part_index, 'context', i, "%s context"%utils.get_ord(i+1), missing_msg=MSG_NUM_CTXT2)

        check_context(state=child)                   # test exist

        ctxt_state = check_context(state=child2)     # sub tests
        multi(context_test, state=ctxt_state)
    
    # Body sub tests ----
    if body is not None:
        body_state = check_part('body', 'body', state=child2)

        with_context(body, state=body_state)

def test_list_comp(index=1,
                   not_called_msg=None,
                   comp_iter=None,
                   iter_vars_names=False,
                   incorrect_iter_vars_msg=None,
                   body=None,
                   ifs=None,
                   insufficient_ifs_msg=None,
                   state=None):
    """Test list comprehension."""
    test_comp("{{ordinal}} list comprehension", 'list_comps', **(locals()))


def test_comp(typestr, comptype, index, iter_vars_names,
              not_called_msg, insufficient_ifs_msg, incorrect_iter_vars_msg,
              comp_iter, ifs, key=None, body=None, value=None,
              rep=None, state=None):

    MSG_INCORRECT_ITER_VARS = "Have you used the correct iterator variables?"
    MSG_INCORRECT_NUM_ITER_VARS = "Have you used {{num_vars}} iterator variables?"
    MSG_INSUFFICIENT_IFS = "Have you used {{sol_len}} ifs?"

    # make sure other messages are set to default if None
    if insufficient_ifs_msg is None:
        insufficient_ifs_msg = MSG_INSUFFICIENT_IFS

    # get comprehension
    child = check_node(comptype, index-1, typestr, missing_msg=not_called_msg, state=state)

    # test comprehension iter and its variable names (or number of variables)
    if comp_iter: multi(comp_iter, state=check_part("iter", "iterable part", state=child))

    # test iterator variables
    default_msg = MSG_INCORRECT_ITER_VARS if iter_vars_names else MSG_INCORRECT_NUM_ITER_VARS
    has_context(incorrect_iter_vars_msg or default_msg, iter_vars_names, state=child)

    # test the main expressions.
    if body:   multi(body,  state=check_part("body", "body", state=child))        # list and gen comp
    if key:    multi(key,   state=check_part("key", "key part",  state=child))    # dict comp
    if value:  multi(value, state=check_part("value", "value part", state=child)) # ""

    # test a list of ifs. each entry corresponds to a filter in the comprehension.
    for i, if_test in enumerate(ifs or []):
        # test that ifs are same length
        has_equal_part_len('ifs', insufficient_ifs_msg, state=child)
        # test individual ifs
        multi(if_test, state=check_part_index("ifs", i, utils.get_ord(i+1) + " if", state=child))

