Simple Tests
============

Simple tests are the most basic tests available in pythonwhat. 
They usually don't focus on specific pieces of a submission (:doc:`like part checks </part_checks.rst>`), or re-run any code (:doc:`like expression tests </expression_tests.md>).
Instead, they simply look at things like imports, printed output, or raw code text.
A final, common use is to test the value of a variable in the final environment (that is, after the submission of solution code have been run).

.. toctree::
    :maxdepth: 2

    test_import
    test_object
    test_output_contains
    test_student_typed
    has_equal_ast
    test_mc
