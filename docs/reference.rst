Reference
=========

.. note::

    - ``check_`` functions typically 'dive' deeper into a part of the state it was passed. They are typically chained for further checking.
    - ``has_`` functions always return the state that they were intially passed and are used at the 'end' of a chain.

Building blocks
---------------

.. autofunction:: pythonwhat.has_funcs.has_code
.. autofunction:: pythonwhat.has_funcs.has_output
.. autofunction:: pythonwhat.has_funcs.has_printout
.. autofunction:: pythonwhat.has_funcs.has_no_error
.. autofunction:: pythonwhat.has_funcs.has_import
.. autofunction:: pythonwhat.has_funcs.has_equal_value
.. autofunction:: pythonwhat.has_funcs.has_equal_output
.. autofunction:: pythonwhat.has_funcs.has_equal_error
.. autofunction:: pythonwhat.has_funcs.has_equal_ast

Combining SCTs
--------------

.. autofunction:: pythonwhat.check_logic.multi
.. autofunction:: pythonwhat.check_logic.check_correct
.. autofunction:: pythonwhat.check_logic.check_or
.. autofunction:: pythonwhat.check_logic.check_not

Objects
-------

.. autofunction:: pythonwhat.check_object.check_object
.. autofunction:: pythonwhat.check_object.is_instance
.. autofunction:: pythonwhat.check_object.check_df
.. autofunction:: pythonwhat.check_object.check_keys

Function calls
--------------

.. autofunction:: pythonwhat.check_function.check_function
.. autofunction:: pythonwhat.check_funcs.check_args

Function/Class/Lambda definitions
---------------------------------

.. autofunction:: pythonwhat.check_wrappers.check_function_def
.. autofunction:: pythonwhat.has_funcs.has_equal_part_len
.. autofunction:: pythonwhat.check_funcs.check_call
.. autofunction:: pythonwhat.check_wrappers.check_class_def
.. autofunction:: pythonwhat.check_wrappers.check_lambda_function

Control flow
------------

.. autofunction:: pythonwhat.check_wrappers.check_if_else
.. autofunction:: pythonwhat.check_wrappers.check_try_except
.. autofunction:: pythonwhat.check_wrappers.check_if_exp
.. autofunction:: pythonwhat.check_wrappers.check_with

Loops
-----

.. autofunction:: pythonwhat.check_wrappers.check_for_loop
.. autofunction:: pythonwhat.check_wrappers.check_while
.. autofunction:: pythonwhat.check_wrappers.check_list_comp
.. autofunction:: pythonwhat.check_wrappers.check_dict_comp
.. autofunction:: pythonwhat.check_wrappers.check_generator_exp

State Management
----------------

.. autofunction:: pythonwhat.check_logic.override
.. autofunction:: pythonwhat.check_logic.disable_highlighting
.. autofunction:: pythonwhat.check_logic.set_context
.. autofunction:: pythonwhat.check_logic.set_env

Electives
---------

.. autofunction:: pythonwhat.has_funcs.has_chosen
.. autofunction:: pythonwhat.test_exercise.success_msg
.. autofunction:: pythonwhat.check_logic.fail