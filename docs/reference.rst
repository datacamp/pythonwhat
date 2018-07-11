Simple tests
------------

.. note::

    - ``check_`` functions produce a child state that 'dives' deeper into a part of the state it was passed. They are typically chained off of for further checking.
    - ``has_`` functions always **return the state that they were intially passed** and are used at the 'end' of a chain.

Basic building blocks
=====================

.. autofunction:: pythonwhat.test_funcs.test_student_typed.has_code
.. autofunction:: pythonwhat.test_funcs.test_output_contains.has_output
.. autofunction:: pythonwhat.test_funcs.test_output_contains.has_printout
.. autofunction:: pythonwhat.test_funcs.test_import.has_import
.. autofunction:: pythonwhat.check_funcs.has_equal_value
.. autofunction:: pythonwhat.check_funcs.has_equal_error
.. autofunction:: pythonwhat.check_funcs.has_equal_output
.. autofunction:: pythonwhat.check_funcs.has_equal_ast

Checking objects
================

.. autofunction:: pythonwhat.check_object.check_object
.. autofunction:: pythonwhat.check_object.is_instance

Checking function calls
=======================

.. autofunction:: pythonwhat.check_function.check_function
.. autofunction:: pythonwhat.check_funcs.check_args

Checking function definitions
=============================

.. autofunction:: pythonwhat.check_funcs.check_args
.. autofunction:: pythonwhat.check_funcs.has_equal_part_len
.. autofunction:: pythonwhat.check_funcs.call

Logic tests
-----------

.. autofunction:: pythonwhat.check_funcs.multi
.. autofunction:: pythonwhat.test_funcs.test_correct.test_correct
.. autofunction:: pythonwhat.test_funcs.test_or.test_or

State-management
----------------

.. autofunction:: pythonwhat.check_funcs.set_context
.. autofunction:: pythonwhat.check_funcs.set_env
.. autofunction:: pythonwhat.check_funcs.disable_highlighting
