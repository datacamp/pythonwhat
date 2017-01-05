Spec2 Changes
==================

.. role:: python(code)
   :language: python


Lambdaless test functions
---------------------------

Sometimes you want to pass a test function as an argument to another test function. For the examples below, we'll use the following solution code

.. code:: python

  # solution code
  [1 if True else 0 for i in range(10)]

Removing Lambdas
~~~~~~~~~~~~~~~~

Using an SCT that works in pythonwhat v2,

.. code:: python
    
    # pythonwhat v2 SCT
    test_list_comp(
            body=test_if_exp(
                    body=test_student_typed('1'))      # line 4

would do the following (in order)...

1. run the test_student_typed function on line 4, which runs over the whole code, rather than just the body of the inline if.
2. pass its return value (None) to the body argument of ``test_if_exp``.
3. run ``test_if_exp``, whose body argument is None, rather than a sub-test.
4. run test_list_comp, whose body argument is None, rather than a sub-test.

Instead, in pythonwhat v1, testing the inline if expression (`1 if True else 0`) requires an SCT peppered with lambdas, such as

.. code:: python

    # v1 SCT
    test_list_comp(
            body=lambda: test_if_exp(
                    body = lambda: test_student_typed('1'))

Removing temporary functions for multiple sub-tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In pythonwhat v2, multiple sub-tests may be run by putting them in a list, such as

.. code:: python

    # v2 SCT
    # list of sub-tests
    if_body_tests = [test_student_typed('1'), test_expression_result(context_vals=[1])]
    # main test
    test_list_comp(
            body = test_if_exp(
                      body = if_body_tests)   # list could also be put here directly

which, in pythonwhat v1 would try to run the tests in ``if_body_tests`` first, rather than as sub-tests.
In order to accomplish this in pythonwhat v1, temporary functions were necessary, such as,

.. code:: python

    # v1 SCT
    # temporary function for testing inline if expression
    def inner_test():
        test_student_typed('1')
        test_expression_result(context_vals=[1])
    # main test
    test_list_comp(
            body=lambda: test_if_exp(body = inner_test))

while not too different, this approach can spiral out of control for complex SCTs (temporary functions within temporary functions, etc..).



How it works
^^^^^^^^^^^^
+---------+--------------------------------------+-------------------------------------+
| spec    | SCT                                  | effect                              |       
+=========+======================================+=====================================+
| v1 test | :python:`test_list_comp()`           | runs test                           |
+---------+--------------------------------------+-------------------------------------+
| v1 test | :python:`lambda: test_list_comp()`   | waits to run                        |
+---------+--------------------------------------+-------------------------------------+
| v2 check| :python:`check_list_comp()`          | waits to run                        |
+---------+--------------------------------------+-------------------------------------+
| v2 check| :python:`Ex().check_list_comp()`     | runs test                           |
+---------+--------------------------------------+-------------------------------------+
| v2 test | :python:`F().test_list_comp()`       | waits to run                        |
+---------+--------------------------------------+-------------------------------------+
| v2 test | :python:`test_list_comp()`           | runs test if not argument to another|
+---------+--------------------------------------+-------------------------------------+

The critical message is in pythonwhat

* **v1**: you have to do something special (use a lambda) to **opt-out** of running a test immediately.
* **v2**: you have to do something special (use ``Ex()``) to **opt-in** to running a test immediately.

pythonwhat v2 is Backwards Compatibile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

for all test\_ functions, pythonwhat v2's behavior is completely backwards compatible (and in fact was put in pythonwhat v1 several weeks before releasing v2). If you want to be explicit about any test function not being run, you can use the function chain object ``F``, for example

.. code::
    
    # Implicit
    sub_test = test_if_exp(ETC...)          # waits to run only if passed to another SCT
    test_list_comp(body=sub_test)           # comment out this line, and sub_test will run (as in pythonwhat v1)
    
    # Explicit
    sub_test = F().test_if_exp(ETC...)      # always waits to run
    Ex().test_list_comp(body=sub_test)

Never mix Explicit and Implicit approaches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you choose to use the explicit approach (``Ex()`` and ``F()``), **don't expect the implicit approach to work**.
That is, if you want ``test_if_exp`` below to run immediately, do not write

.. code::

    test_if_exp(1)            # implicit, should use Ex() or F()
    Ex().check_list_comp(1)   # explicit

and expect the SCTs to run in a predictable order.

If you want to create a bunch of sub-tests, but don't want to preface each with F(), you can use the pythonwhat v2 function multi, as below.

.. code::

   subtest = multi(test_if_exp(ETC...), test_list_comp(ETC...))
   
    
Context values for nested parts
-------------------------------

Context values may now be defined for nested parts. For example, the print statement below,

.. code::

    for i in range(2):              # outer for loop part
        for j in range(3):          # inner for loop part
            print(i + j)

may be tested by setting context values at each level,

.. code::

    (Ex()
        .check_for_loop(0).check_body().set_context(i = 1)    # outer for
        .check_for_loop(0).check_body().set_context(j = 2)    # inner for
            .has_equal_output()
        )

For more on context valus see [PROCESSES LINK HERE].

Can call code chunks that before could only be split up
-------------------------------------------------------

Entire code pieces, such as the inline if statement below,

.. code::

    'yes' if True else 'no'

may be tested using something like,

.. code::

    Ex().check_if_exp(0).has_equal_value()

Argument checking
-----------------

The arguments of a function definition, such as

.. code::

    def f(a=1): print(a)

are now parts and may be checked as below..

.. code::

    (Ex().check_function_def('f')   # does f exist?
         .check_args('a')           # does a exist?
         .is_default()              # is it a default argument?
         .has_equal_value()         # is it's default equal to solution?
         )
         
For more on the argument part, see [PART CHEATSHEET LINK HERE].


Deprecate test_expression_result and friends
--------------------------------------------

In pythonwhat v1, the functions 

* test_expression_result
* test_expression_output
* test_object_after_expression

and various arguments of test_function_definition, test_lambda_function ran code and then
checked the result, printed output, or errors against eachother.

These functions have been deprecated in favor of similar function..

* `has_equal_value`
* `has_equal_output`
* `has_equal_error`

These functions include identical arguments as the above.

Feedback messages may use templating (via str.format or Jinja2)
-----------------------------------------------------------------

**This feature is not stable, and should not be used in production**


Cleaned up internals
--------------------

Yayyyy.
