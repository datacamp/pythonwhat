from protowhat.utils import _debug
from protowhat.checks.check_files import check_file, has_dir
from pythonwhat.checks.check_funcs import check_part, check_part_index, check_node
from pythonwhat.checks.has_funcs import has_equal_part
from pythonwhat.checks import check_object, check_logic, check_funcs, has_funcs
from pythonwhat.checks.check_function import check_function
from pythonwhat.checks.check_has_context import has_context

from inspect import signature, Parameter
from functools import partial, wraps
from jinja2 import Template

__PART_WRAPPERS__ = {
    "iter": "iterable part",
    "body": "body",
    "key": "key part",
    "value": "value part",
    "orelse": "else part",
    "finalbody": "finally part",
    "test": "condition",
}

__PART_INDEX_WRAPPERS__ = {
    "ifs": "{{ordinal}} if",
    "bases": "{{ordinal}} base class",
    "handlers": "`{{index}}` `except` block",
    "context": "{{ordinal}} context",
}

__NODE_WRAPPERS__ = {
    "list_comp": {
        "typestr": "{{ordinal}} list comprehension",
        "docstr": """Check whether a list comprehension was coded and zoom in on it.

        Can be chained with ``check_iter()``, ``check_body()``, and ``check_ifs()``.

        Args:
            index: Index of the list comprehension (0-based)
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you expect students to create a list ``my_list`` as follows: ::

                my_list = [ i*2 for i in range(0,10) if i>2 ]

            The following SCT would robustly verify this: ::

                Ex().check_correct(
                    check_object('my_list').has_equal_value(),
                    check_list_comp().multi(
                        check_iter().has_equal_value(),
                        check_body().set_context(4).has_equal_value(),
                        check_ifs(0).multi(
                            set_context(0).has_equal_value(),
                            set_context(3).has_equal_value(),
                            set_context(5).has_equal_value()
                        )
                    )
                )

            - With ``check_correct()``, we're making sure that the list comprehension
              checking is not executed if ``my_list`` was calculated properly.
            - If ``my_list`` is not correct, the 'diagnose' chain will run: ``check_list_comp()`` looks
              for the first list comprehension in the student's submission.
            - Next, ``check_iter()`` zooms in on the iterator, ``range(0, 10)`` in the case of the solution.
              ``has_equal_value()`` verifies whether the expression that the student used evaluates to the
              same value as the expression that the solution used.
            - ``check_body()`` zooms in on the body, ``i*2`` in the case of the solution.
              ``set_context()`` sets the iterator to 4, allowing for the fact that the student used another name instead of ``i`` for this iterator.
              ``has_equal_value()`` reruns the body in the student and solution code with the iterator set to 4, and checks if the results are the same.
            - ``check_ifs(0)`` zooms in on the first ``if`` of the list comprehension, ``i>2`` in case of the solution.
              With a series of ``set_context()`` and ``has_equal_value()``, it is verifies whether this condition evaluates to the same value in student
              and solution code for different values of the iterator (`i` in the case of the solution, whatever in the case of the student).

        """,
    },
    "generator_exp": {
        "typestr": "{{ordinal}} generator expression",
        "docstr": """Check whether a generator expression was coded and zoom in on it.

        Can be chained with ``check_iter()``, ``check_body()``, and ``check_ifs()``.

        Args:
            index: Index of the generator expression (0-based)
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you expect students to create a generator ``my_gen`` as follows: ::

                my_gen = ( i*2 for i in range(0,10) )

            The following SCT would robustly verify this: ::

                Ex().check_correct(
                    check_object('my_gen').has_equal_value(),
                    check_generator_exp().multi(
                        check_iter().has_equal_value(),
                        check_body().set_context(4).has_equal_value()
                    )
                )

            Have a look at ``check_list_comp`` to understand what's going on; it is very similar.

        """,
    },
    "dict_comp": {
        "typestr": "{{ordinal}} dictionary comprehension",
        "docstr": """Check whether a dictionary comprehension was coded and zoom in on it.

        Can be chained with ``check_key()``, ``check_value()``, and ``check_ifs()``.

        Args:
            index: Index of the dictionary comprehension (0-based)
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you expect students to create a dictionary ``my_dict`` as follows: ::

                my_dict = { m:len(m) for m in ['a', 'ab', 'abc'] }

            The following SCT would robustly verify this: ::

                Ex().check_correct(
                    check_object('my_dict').has_equal_value(),
                    check_dict_comp().multi(
                        check_iter().has_equal_value(),
                        check_key().set_context('ab').has_equal_value(),
                        check_value().set_context('ab').has_equal_value()
                    )
                )

            - With ``check_correct()``, we're making sure that the dictionary comprehension
              checking is not executed if ``my_dict`` was created properly.
            - If ``my_dict`` is not correct, the 'diagnose' chain will run: ``check_dict_comp()`` looks
              for the first dictionary comprehension in the student's submission.
            - Next, ``check_iter()`` zooms in on the iterator, ``['a', 'ab', 'abc']`` in the case of the solution.
              ``has_equal_value()`` verifies whether the expression that the student used evaluates to the
              same value as the expression that the solution used.
            - ``check_key()`` zooms in on the key of the comprehension, ``m`` in the case of the solution.
              ``set_context()`` temporaritly sets the iterator to ``'ab'``, allowing for the fact that the student used another name instead of ``m`` for this iterator.
              ``has_equal_value()`` reruns the key expression in the student and solution code with the iterator set to ``'ab'``, and checks if the results are the same.
            - ``check_value()`` zooms in on the value of the comprehension, ``len(m)`` in the case of the solution.
              ``has_equal_value()`` reruns the value expression in the student and solution code with the iterator set to ``'ab'``, and checks if the results are the same.

        """,
    },
    "for_loop": {
        "typestr": "{{ordinal}} for loop",
        "docstr": """Check whether a for loop was coded and zoom in on it.

        Can be chained with ``check_iter()`` and ``check_body()``.

        Args:
            index: Index of the for loop (0-based).
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you want a student to iterate over a predefined dictionary ``my_dict`` and do the appropriate printouts: ::

                for key, value in my_dict.items():
                    print(key + " - " + str(value))

            The following SCT would verify this: ::

                Ex().check_for_loop().multi(
                    check_iter().has_equal_value(),
                    check_body().multi(
                        set_context('a', 1).has_equal_output(),
                        set_context('b', 2).has_equal_output()
                    )
                )

            - ``check_for_loop()`` zooms in on the ``for`` loop, and makes its parts available for further checking.
            - ``check_iter()`` zooms in on the iterator part of the for loop, ``my_dict.items()`` in the solution.
              ``has_equal_value()`` re-executes the expressions specified by student and solution and compares their results.
            - ``check_body()`` zooms in on the body part of the for loop, ``print(key + " - " + str(value))``.
              For different values of ``key`` and ``value``, the student's body and solution's body are executed again and the printouts are captured and compared to see if they are equal.

            Notice how you do not need to specify the variables by name in ``set_context()``. pythonwhat can figure out the variable names used in both student and solution code, and
            can do the verification independent of that. That way, we can make the SCT robust against submissions that code the correct logic, but use different names for the context values.
            In other words, the following student submissions that would also pass the SCT: ::

                # passing submission 1
                my_dict = {'a': 1, 'b': 2}
                for k, v in my_dict.items():
                    print(k + " - " + str(v))

                # passing submission 2
                my_dict = {'a': 1, 'b': 2}
                for first, second in my_dict.items():
                    mess = first + " - " + str(second)
                    print(mess)

        :Example:

            As another example, suppose you want the student to build a list of doubles as follows: ::

                even = []
                for i in range(10):
                    even.append(2*i)

            The following SCT would robustly verify this: ::

                Ex().check_correct(
                    check_object('even').has_equal_value(),
                    check_for_loop().multi(
                        check_iter().has_equal_value(),
                        check_body().set_context(2).set_env(even = []).\\
                            has_equal_value(name = 'even')
                    )
                )

            - ``check_correct()`` makes sure that we do not dive into the ``for`` loop if the array ``even`` is correctly populated in the end.
            - If ``even`` was not correctly populated, ``check_for_loop()`` will zoom in on the for loop.
            - The ``check_iter()`` chain verifies whether `range(10)` (or something equivalent) was used to iterate over.
            - ``check_body()`` zooms in on the body, and reruns the body (``even.append(2*i)`` in the solution) for ``i`` equal to 2, and even temporarily set to an empty array.
              Notice how we use ``set_context()`` to robustly set the context value (the student can use a different variable name), while we have to explicitly set ``even`` with ``set_env()``.
              Also notice how we use ``has_equal_value(name = 'even')`` instead of the usual ``check_object()``; ``check_object()`` can only be called from the root state ``Ex()``.

        :Example:

            As a follow-up example, suppose you want the student to build a list of doubles of the even numbers only: ::

                even = []
                for i in range(10):
                    if i % 2 == 0:
                        even.append(2*i)

            The following SCT would robustly verify this: ::

                Ex().check_correct(
                    check_object('even').has_equal_value(),
                    check_for_loop().multi(
                        check_iter().has_equal_value(),
                        check_body().check_if_else().multi(
                            check_test().multi(
                                set_context(1).has_equal_value(),
                                set_context(2).has_equal_value()
                            ),
                            check_body().set_context(2).\\
                                set_env(even = []).has_equal_value(name = 'even')
                        )
                    )
                )

        """,
    },
    "function_def": {
        "typestr": "definition of `{{index}}()`",
        "docstr": """Check whether a function was defined and zoom in on it.

        Can be chained with ``check_call()``, ``check_args()`` and ``check_body()``.

        Args:
            index: the name of the function definition.
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you want a student to create a function ``shout_echo()``: ::

                def shout_echo(word1, echo=1):
                    echo_word = word1 * echo
                    shout_words = echo_word + '!!!'
                    return shout_words

            The following SCT robustly checks this: ::

                Ex().check_function_def('shout_echo').check_correct(
                    multi(
                        check_call("f('hey', 3)").has_equal_value(),
                        check_call("f('hi', 2)").has_equal_value(),
                        check_call("f('hi')").has_equal_value()
                    ),
                    check_body().set_context('test', 1).multi(
                        has_equal_value(name = 'echo_word'),
                        has_equal_value(name = 'shout_words')
                    )
                )

            Here:

            - ``check_function_def()`` zooms in on the function definition of ``shout_echo`` in both student and solution code (and process).
            - ``check_correct()`` is used to

                + First check whether the function gives the correct result when called in different ways (through ``check_call()``).
                + Only if these 'function unit tests' don't pass, ``check_correct()`` will run the `check_body()` chain that dives deeper into the
                  function definition body. This chain sets the context variables - ``word1`` and ``echo``, the arguments of the function - to
                  the values ``'test'`` and ``1`` respectively, again while being agnostic to the actual name of these context variables.

            Notice how ``check_correct()`` is used to great effect here: why check the function definition internals if the I/O of the function works fine?
            Because of this construct, all the following submissions will pass the SCT: ::

                # passing submission 1
                def shout_echo(w, e=1):
                    ew = w * e
                    return ew + '!!!'

                # passing submission 2
                def shout_echo(a, b=1):
                    return a * b + '!!!'

        :Example:

            ``check_args()`` is most commonly used in combination with ``check_function()``
            to verify the arguments of function **calls**, but it can also be used
            to verify the arguments specified in the signature of a function definition.

            We can extend the SCT for the previous example to explicitly verify the signature: ::


                msg1 = "Make sure to specify 2 arguments!"
                msg2 = "don't specify default arg!"
                msg3 = "specify a default arg!"
                Ex().check_function_def('shout_echo').check_correct(
                    multi(
                        check_call("f('hey', 3)").has_equal_value(),
                        check_call("f('hi', 2)").has_equal_value(),
                        check_call("f('hi')").has_equal_value()
                    ),
                    multi(
                        has_equal_part_len("args", unequal_msg=1),
                        check_args(0).has_equal_part('is_default', msg=msg2),
                        check_args('word1').has_equal_part('is_default', msg=msg2),
                        check_args(1).\\
                            has_equal_part('is_default', msg=msg3).has_equal_value(),
                        check_args('echo').\\
                            has_equal_part('is_default', msg=msg3).has_equal_value(),
                        check_body().set_context('test', 1).multi(
                            has_equal_value(name = 'echo_word'),
                            has_equal_value(name = 'shout_words')
                        )
                    )
                )

            - ``has_equal_part_len("args")`` verifies whether student and solution function
              definition have the same number of arguments.
            - ``check_args(0)`` refers to the first argument in the signature by position,
              and the chain checks whether the student did not specify a default as in the solution.
            - An alternative for the ``check_args(0)`` chain is to use ``check_args('word1')``
              to refer to the first argument. This is more restrictive, as the requires the
              student to use the exact same name.
            - ``check_args(1)`` refers to the second argument in the signature by position,
              and the chain checks whether the student specified a default, as in the solution, and
              whether the value of this default corresponds to the one in the solution.
            - The ``check_args('echo')`` chain is a more restrictive alternative for the ``check_args(1)``
              chain.

            Notice that support for verifying arguments is not great yet:

            - A lot of work is needed to verify the number of arguments and whether or not defaults are set.
            - You have to specify custom messages because pythonwhat doesn't automatically generate messages.

            We are working on it!

        """,
    },
    "class_def": {
        "typestr": "class definition of `{{index}}`",
        "docstr": """Check whether a class was defined and zoom in on its definition

        Can be chained with ``check_bases()`` and ``check_body()``.

        Args:
            index: the name of the function definition.
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you want to check whether a class was defined correctly: ::

                class MyInt(int):
                    def __init__(self, i):
                        super().__init__(i + 1)

            The following SCT would verify this: ::

                Ex().check_class_def('MyInt').multi(
                    check_bases(0).has_equal_ast(),
                    check_body().check_function_def('__init__').multi(
                        check_args('self'),
                        check_args('i'),
                        check_body().set_context(i = 2).multi(
                            check_function('super', signature=False),
                            check_function('super.__init__').check_args(0).has_equal_value()
                        )
                    )
                )

            - ``check_class_def()`` looks for the class definition itself.
            - With ``check_bases()``, you can zoom in on the different basse classes that the class definition inherits from.
            - With ``check_body()``, you zoom in on the class body, after which you can use other functions such
              as ``check_function_def()`` to look for class methods.
            - Of course, just like for other examples, you can use ``check_correct()`` where necessary,
              e.g. to verify whether class methods give the right behavior with ``check_call()``
              before diving into the body of the method itself.

        """,
    },
    "if_exp": {
        "typestr": "{{ordinal}} if expression",
        "docstr": """Check whether an if expression was coded zoom in on it.

        This function works the exact same way as ``check_if_else()``.
        """,
    },
    "if_else": {
        "typestr": "{{ordinal}} if statement",
        "docstr": """Check whether an if statement was coded zoom in on it.

        Args:
            index: the index of the if statement to look for (0 based)
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you want students to print out a message if ``x`` is larger than 0: ::

                x = 4
                if x > 0:
                    print("x is strictly positive")

            The following SCT would verify that: ::

                Ex().check_if_else().multi(
                    check_test().multi(
                        set_env(x = -1).has_equal_value(),
                        set_env(x =  1).has_equal_value(),
                        set_env(x =  0).has_equal_value()
                    ),
                    check_body().check_function('print', 0).\\
                        check_args('value').has_equal_value()
                )

            - ``check_if_else()`` zooms in on the first if statement in the student and solution submission.
            - ``check_test()`` zooms in on the 'test' portion of the if statement, ``x > 0`` in case of the solution.
              ``has_equal_value()`` reruns this expression and the corresponding expression in the student code for
              different values of ``x`` (set with ``set_env()``) and compare there results.
              This way, you can robustly verify whether the if test was coded up correctly. If the student
              codes up the condition as ``0 < x``, this would also be accepted.
            - ``check_body()`` zooms in on the 'body' portion of the if statement, ``print("...")`` in case of the solution.
              With a classical ``check_function()`` chain, it is verified whether the if statement contains a
              function ``print()`` and whether its argument is set correctly.

        :Example:

            In Python, when an if-else statement has an ``elif`` clause, it is held in the `orelse` part.
            In this sense, an if-elif-else statement is represented by python as nested if-elses.
            More specifically, this if-else statement: ::

                if x > 0:
                    print(x)
                elif y > 0:
                    print(y)
                else:
                    print('none')

            Is syntactically equivalent to: ::

                if x > 0:
                    print(x)
                else:
                    if y > 0:
                        print(y)
                    else:
                        print('none')

            The second representation has to be followed when writing the corresponding SCT: ::

                Ex().check_if_else().multi(
                    check_test(),          # zoom in on x > 0
                    check_body(),          # zoom in on print(x)
                    check_orelse().check_if_else().multi(
                        check_test(),      # zoom in on y > 0
                        check_body(),      # zoom in on print(y)
                        check_orelse()     # zoom in on print('none')
                    )
                )

        """,
    },
    "lambda_function": {
        "typestr": "{{ordinal}} lambda function",
        "docstr": """Check whether a lambda function was coded zoom in on it.

        Can be chained with ``check_call()``, ``check_args()`` and ``check_body()``.

        Args:
            index: the index of the lambda function (0-based).
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you want a student to create a lambda function
            that returns the length of an array times two: ::

                lambda x: len(x)*2

            The following SCT robustly checks this: ::

                Ex().check_lambda_function().check_correct(
                    multi(
                        check_call("f([1])").has_equal_value(),
                        check_call("f([1, 2])").has_equal_value()
                    ),
                    check_body().set_context([1, 2, 3]).has_equal_value()
                )

            Here:

            - ``check_lambda_function()`` zooms in on the first lambda function in both student and solution code.
            - ``check_correct()`` is used to

                + First check whether the lambda function gives the correct result when called in different ways (through ``check_call()``).
                + Only if these 'function unit tests' don't pass, ``check_correct()`` will run the `check_body()` chain that dives deeper into the
                  lambda function's body. This chain sets the context variable `x`, the argument of the function, to
                  the values ``[1, 2, 3]``, while being agnostic to the actual name the student used for this context variable.

            Notice how ``check_correct()`` is used to great effect here: why check the function definition internals if the I/O of the function works fine?
            Because of this construct, all the following submissions will pass the SCT: ::

                # passing submission 1
                lambda x: len(x) + len(x)

                # passing submission 2
                lambda y, times=2: len(y) * times
        """,
    },
    "try_except": {
        "typestr": "{{ordinal}} try statement",
        "docstr": """Check whether a try except statement was coded zoom in on it.

        Can be chained with ``check_body()``, ``check_handlers()``, ``check_orelse()`` and ``check_finalbody()``.

        Args:
            index: the index of the try except statement (0-based).
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you want to verify whether the student did a `try-except` statement properly: ::

                do_dangerous_thing = lambda n: n

                try:
                    x = do_dangerous_thing(n = 4)
                except ValueError as e:
                    x = 'something wrong with inputs'
                except:
                    x = 'something went wrong'
                finally:
                    print('ciao!')

            The following SCT can be used to verify this: ::

                Ex().check_try_except().multi(
                    check_body().\\
                        check_function('do_dangerous_thing').\\
                        check_args('n').has_equal_value(),
                    check_handlers('ValueError').\\
                        has_equal_value(name = 'x'),
                    check_handlers('all').\\
                        has_equal_value(name = 'x'),
                    check_finalbody().\\
                        check_function('print').check_args(0).has_equal_value()
                )

        """,
    },
    "while": {
        "typestr": "{{ordinal}} `while` loop",
        "docstr": """Check whether a while loop was coded and zoom in on it.

        Can be chained with ``check_test()``, ``check_body()`` and ``check_orelse()``.

        Args:
            index: the index of the while loop to verify (0-based).
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        :Example:

            Suppose you want a student to code a while loop that counts down a counter from 50 until
            a multilpe of 11 is found. If it is found, the value should be printed out. ::

                i = 50
                while i % 11 != 0:
                    i -= 1

            The following SCT robustly verifies this: ::

                Ex().check_correct(
                    check_object('i').has_equal_value(),
                    check_while().multi(
                            check_test().multi(
                                set_env(i = 45).has_equal_value(),
                                set_env(i = 44).has_equal_value()
                            ),
                            check_body().set_env(i = 3).has_equal_value(name = 'i')
                    )
                )

            - ``check_correct()`` first checks whether the end result of ``i`` is correct. If it is, the entire chain that checks the ``while`` loop is skipped.
            - If ``i`` is not correctly calculated, ``check_while_loop()`` zooms in on the while loop.
            - ``check_test()`` zooms in on the condition of the ``while`` loop, ``i % 11 != 0`` in the solution, and verifies whether
              the expression gives the same results for different values of ``i``, set through ``set_env()``, when comparing student and solution.
            - ``check_body()`` zooms in on the body of the ``while`` loop, and ``has_equal_value()`` checks whether rerunning this body
              updates ``i`` as expected when ``i`` is temporarily set to 3 with ``set_env()``.

        """,
    },
    "with": {
        "typestr": "{{ordinal}} `with` statement",
        "docstr": """Check whether a with statement was coded zoom in on it.

        Args:
            index: the index of the``with`` statement to verify (0-based)
            {{typestr}}
            {{missing_msg}}
            {{expand_msg}}

        """,
    },
}

scts = dict()

# make has_equal_part wrappers


def partial_with_offset(offset=1):
    def bound_partial_with_offset(func, *partial_args, **partial_kwargs):
        kwargs_partial = partial(func, **partial_kwargs)

        @wraps(func)
        def full_partial(*args, **kwargs):
            full_args = args[:offset] + partial_args + args[offset:]
            return kwargs_partial(*full_args, **kwargs)

        # set correct signature of returned partial
        # todo: pass arguments as keywords to partial, instead of this decorator?
        #  (where args are always the same)
        func_sig = signature(full_partial)
        parameter_names = tuple(func_sig.parameters)

        partialed_positional_indices = []
        for kwarg in partial_kwargs:
            param = func_sig.parameters[kwarg]
            if param.default is param.empty:
                partialed_positional_indices.append(parameter_names.index(kwarg))

        partial_params = list(func_sig.parameters.values())
        for index in sorted(partialed_positional_indices, reverse=True):
            # appending isn't needed for functionality, but more similar to partial
            # and it shows that these arguments can still be updated as kwargs
            partial_params.append(
                partial_params[index].replace(
                    kind=Parameter.KEYWORD_ONLY,
                    default=partial_kwargs[partial_params[index].name],
                )
            )
            del partial_params[index]
        del partial_params[offset : offset + len(partial_args)]

        full_partial.__signature__ = func_sig.replace(parameters=partial_params)

        return full_partial

    return bound_partial_with_offset


state_partial = partial_with_offset()


def rename_function(func, name):
    # see functools.wraps
    func.__name__ = func.__qualname__ = name


scts["has_equal_name"] = state_partial(
    has_equal_part,
    "name",
    msg="Make sure to use the correct {{name}}, was expecting {{sol_part[name]}}, instead got {{stu_part[name]}}.",
)
scts["is_default"] = state_partial(
    has_equal_part,
    "is_default",
    msg="Make sure it {{ 'has' if sol_part.is_default else 'does not have'}} a default argument.",
)

# include rest of wrappers
for k, v in __PART_WRAPPERS__.items():
    check_fun = state_partial(check_part, k, v)
    rename_function(check_fun, "check_" + k)
    scts[check_fun.__name__] = check_fun

for k, v in __PART_INDEX_WRAPPERS__.items():
    check_fun = state_partial(check_part_index, k, part_msg=v)
    rename_function(check_fun, "check_" + k)
    scts[check_fun.__name__] = check_fun

for k, v in __NODE_WRAPPERS__.items():
    check_fun = state_partial(check_node, k + "s", typestr=v["typestr"])
    check_fun.__doc__ = Template(v["docstr"]).render(
        typestr="typestr: If specified, this overrides the standard way of referring to the construct you're zooming in on.",
        missing_msg="missing_msg: If specified, this overrides the automatically generated feedback message in case the construct could not be found.",
        expand_msg="expand_msg: If specified, this overrides the automatically generated feedback message that is prepended to feedback messages that are thrown further in the SCT chain.",
    )
    rename_function(check_fun, "check_" + k)
    scts[check_fun.__name__] = check_fun

for k in [
    "set_context",
    "set_env",
    "disable_highlighting",
    "check_not",
    "check_or",
    "check_correct",
    "fail",
    "override",
    "multi",
]:
    scts[k] = getattr(check_logic, k)

for k in ["with_context", "check_args", "check_call"]:
    scts[k] = getattr(check_funcs, k)

for k in [
    "has_equal_value",
    "has_equal_output",
    "has_equal_error",
    "has_equal_ast",
    "has_equal_part_len",
    "has_equal_part",
    "has_import",
    "has_output",
    "has_printout",
    "has_code",
    "has_no_error",
    "has_chosen",
]:
    scts[k] = getattr(has_funcs, k)

# include check_object and friends ------
for k in ["check_object", "is_instance", "check_df", "check_keys"]:
    scts[k] = getattr(check_object, k)

scts["has_context"] = has_context
scts["check_function"] = check_function
scts["check_file"] = check_file
scts["has_dir"] = has_dir
scts["_debug"] = _debug

locals().update(scts)
