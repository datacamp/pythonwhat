Reference
=========

.. note::

    - ``check_`` functions typically 'dive' deeper into a part of the state it was passed. They are typically chained for further checking.
    - ``has_`` functions always return the state that they were intially passed and are used at the 'end' of a chain.

Objects
-------

.. autofunction:: pythonwhat.checks.check_object.check_object
.. autofunction:: pythonwhat.checks.check_object.is_instance
.. autofunction:: pythonwhat.checks.check_object.check_df
.. autofunction:: pythonwhat.checks.check_object.check_keys

Function calls
--------------

.. autofunction:: pythonwhat.checks.check_function.check_function
.. autofunction:: pythonwhat.checks.check_funcs.check_args

Output
------

.. autofunction:: pythonwhat.checks.has_funcs.has_output
.. autofunction:: pythonwhat.checks.has_funcs.has_printout
.. autofunction:: pythonwhat.checks.has_funcs.has_no_error

Code
----

.. autofunction:: pythonwhat.checks.has_funcs.has_code
.. autofunction:: pythonwhat.checks.has_funcs.has_import

has_equal_x
-----------

.. autofunction:: pythonwhat.checks.has_funcs.has_equal_value
.. autofunction:: pythonwhat.checks.has_funcs.has_equal_output
.. autofunction:: pythonwhat.checks.has_funcs.has_equal_error
.. autofunction:: pythonwhat.checks.has_funcs.has_equal_ast

Combining SCTs
--------------

.. autofunction:: pythonwhat.checks.check_logic.multi
.. autofunction:: pythonwhat.checks.check_logic.check_correct
.. autofunction:: pythonwhat.checks.check_logic.check_or
.. autofunction:: pythonwhat.checks.check_logic.check_not

Function/Class/Lambda definitions
---------------------------------

.. autofunction:: pythonwhat.checks.check_wrappers.check_function_def
.. autofunction:: pythonwhat.checks.has_funcs.has_equal_part_len
.. autofunction:: pythonwhat.checks.check_funcs.check_call
.. autofunction:: pythonwhat.checks.check_wrappers.check_class_def
.. autofunction:: pythonwhat.checks.check_wrappers.check_lambda_function

Control flow
------------

.. autofunction:: pythonwhat.checks.check_wrappers.check_if_else
.. autofunction:: pythonwhat.checks.check_wrappers.check_try_except
.. autofunction:: pythonwhat.checks.check_wrappers.check_if_exp
.. autofunction:: pythonwhat.checks.check_wrappers.check_with

Loops
-----

.. autofunction:: pythonwhat.checks.check_wrappers.check_for_loop
.. autofunction:: pythonwhat.checks.check_wrappers.check_while
.. autofunction:: pythonwhat.checks.check_wrappers.check_list_comp
.. autofunction:: pythonwhat.checks.check_wrappers.check_dict_comp
.. autofunction:: pythonwhat.checks.check_wrappers.check_generator_exp

State management
----------------

.. autofunction:: pythonwhat.checks.check_logic.override
.. autofunction:: pythonwhat.checks.check_logic.disable_highlighting
.. autofunction:: pythonwhat.checks.check_logic.set_context
.. autofunction:: pythonwhat.checks.check_logic.set_env

Checking files
--------------

.. autofunction:: pythonwhat.checks.check_wrappers.check_file
.. autofunction:: pythonwhat.checks.check_wrappers.has_dir
.. autofunction:: pythonwhat.local.run

Electives
---------

.. autofunction:: pythonwhat.checks.has_funcs.has_chosen
.. autofunction:: pythonwhat.test_exercise.success_msg
.. autofunction:: pythonwhat.checks.check_logic.fail
