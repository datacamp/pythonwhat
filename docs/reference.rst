Simple tests
------------

Basic building blocks
=====================

.. autofunction:: pythonwhat.test_funcs.test_student_typed.has_code
.. autofunction:: pythonwhat.test_funcs.test_output_contains.has_output
.. autofunction:: pythonwhat.test_funcs.test_import.has_import
.. autofunction:: pythonwhat.check_funcs.has_equal_value
.. autofunction:: pythonwhat.check_funcs.has_equal_error
.. autofunction:: pythonwhat.check_funcs.has_equal_output
.. autofunction:: pythonwhat.check_funcs.has_equal_ast

Checking objects
================

.. autofunction:: pythonwhat.check_object.check_object
.. autofunction:: pythonwhat.check_object.is_instance
.. autofunction:: pythonwhat.check_object.has_key
.. autofunction:: pythonwhat.check_object.has_equal_key

Checking function calls
=======================

.. autofunction:: pythonwhat.check_function.check_function
.. autofunction:: pythonwhat.check_funcs.check_args

Part Checks
-----------

TODO add part on default signature of every ``check_<statement>`` function

.. autofunction:: pythonwhat.check_funcs.set_context
.. autofunction:: pythonwhat.check_has_context.has_context
.. autofunction:: pythonwhat.check_funcs.with_context

Logic tests
-----------

.. autofunction:: pythonwhat.check_funcs.multi
.. autofunction:: pythonwhat.test_funcs.test_correct.test_correct
.. autofunction:: pythonwhat.test_funcs.test_or.test_or
