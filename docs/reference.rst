.. note::

    - ``check_`` functions produce a child state that 'dives' deeper into a part of the state it was passed. They are typically chained off of for further checking.
    - ``has_`` functions always **return the state that they were intially passed** and are used at the 'end' of a chain.

SCT building blocks
-------------------

.. autofunction:: pythonwhat.has_funcs.has_code
.. autofunction:: pythonwhat.has_funcs.has_output
.. autofunction:: pythonwhat.has_funcs.has_printout
.. autofunction:: pythonwhat.has_funcs.has_no_error
.. autofunction:: pythonwhat.has_funcs.has_import
.. autofunction:: pythonwhat.has_funcs.has_equal_value
.. autofunction:: pythonwhat.has_funcs.has_equal_output
.. autofunction:: pythonwhat.has_funcs.has_equal_error
.. autofunction:: pythonwhat.has_funcs.has_equal_ast

Checking objects
----------------

.. autofunction:: pythonwhat.check_object.check_object
.. autofunction:: pythonwhat.check_object.is_instance
.. autofunction:: pythonwhat.check_object.check_df
.. autofunction:: pythonwhat.check_object.check_keys

Checking function calls and definitions
---------------------------------------

.. autofunction:: pythonwhat.has_funcs.has_equal_part_len
.. autofunction:: pythonwhat.check_function.check_function
.. autofunction:: pythonwhat.check_funcs.check_call
.. autofunction:: pythonwhat.check_funcs.check_args

Combining SCTs
--------------

.. autofunction:: pythonwhat.check_logic.multi
.. autofunction:: pythonwhat.check_logic.check_correct
.. autofunction:: pythonwhat.check_logic.check_or
.. autofunction:: pythonwhat.check_logic.check_not

State Management
----------------

.. autofunction:: pythonwhat.check_logic.override
.. autofunction:: pythonwhat.check_logic.disable_highlighting
.. autofunction:: pythonwhat.check_logic.set_context
.. autofunction:: pythonwhat.check_logic.set_env
