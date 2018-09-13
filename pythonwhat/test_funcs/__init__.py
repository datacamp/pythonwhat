
from .test_compound_statement import test_with, test_list_comp, \
    test_if_else, test_for_loop, test_while_loop, \
    test_expression_output, test_expression_result, \
    test_object_after_expression, test_function_definition

from .test_object import test_object, test_data_frame
from .test_function import test_function, test_function_v2
from .test_object_accessed import test_object_accessed

from pythonwhat.check_logic import check_or as test_or, check_correct as test_correct

from pythonwhat.has_funcs import has_code as test_student_typed, \
    has_import as test_import, \
    has_output as test_output_contains, \
    has_chosen as test_mc