from pythonwhat.parsing import ObjectAssignmentParser
from pythonwhat.Test import DefinedProcessTest, InstanceProcessTest, DefinedCollProcessTest
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isDefinedInProcess, isInstanceInProcess, isDefinedCollInProcess
from pythonwhat.check_funcs import part_to_child
from pythonwhat.has_funcs import has_equal_value
import pandas as pd
import ast

def check_object(index, missing_msg=None, expand_msg=None, state=None, typestr="variable"):
    """Check object existence (and equality)

    Check whether an object is defined in the student's environment, and zoom in on its value in both
    student and solution environment to inspect quality (with has_equal_value().

    Args:
        index (str): the name of the object which value has to be checked.
        missing_msg (str): feedback message when the object is not defined in the student's environment.
        expand_msg (str): prepending message to put in front.

    :Example:

        Student code::

            b = 1
            c = 3

        Solution code::

            a = 1
            b = 2
            c = 3

        SCT::

            Ex().check_object("a")                    # fail
            Ex().check_object("b")                    # pass
            Ex().check_object("b").has_equal_value()  # fail
            Ex().check_object("c").has_equal_value()  # pass

    """

    if missing_msg is None:
        missing_msg = "__JINJA__:Did you define the {{typestr}} `{{index}}` without errors?"

    if expand_msg is None:
        expand_msg = "__JINJA__:Did you correctly define the {{typestr}} `{{index}}`? "

    rep = Reporter.active_reporter

    if not isDefinedInProcess(index, state.solution_process) and state.has_different_processes():
        raise NameError("%r not in solution environment " % index)

    append_message = {'msg': expand_msg, 'kwargs': {'index': index, 'typestr': typestr}}

    # create child state, using either parser output, or create part from name
    fallback = lambda: ObjectAssignmentParser.get_part(index)
    stu_part = state.student_object_assignments.get(index, fallback())
    sol_part = state.solution_object_assignments.get(index, fallback())

    # test object exists
    _msg = state.build_message(missing_msg, append_message['kwargs'])
    rep.do_test(DefinedProcessTest(index, state.student_process, Feedback(_msg)))

    child = part_to_child(stu_part, sol_part, append_message, state)

    return child

def is_instance(inst, not_instance_msg=None, state=None):
    """Check whether an object is an instance of a certain class.

    ``is_instance()`` can currently only be used when chained from ``check_object()``, the function that is
    used to 'zoom in' on the object of interest.

    Args:
        inst (class): The class that the object should have.
        not_instance_msg (str): When specified, this overrides the automatically generated message in case
            the object does not have the expected class.
        state (State): The state that is passed in through the SCT chain (don't specify this).

    :Example:

        Student code and solution code::

            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])

        SCT::

            # Verify the class of arr
            import numpy
            Ex().check_object('arr').is_instance(numpy.ndarray)
    """
    rep = Reporter.active_reporter

    sol_name = state.solution_parts.get('name')
    stu_name = state.student_parts.get('name')

    if not_instance_msg is None: not_instance_msg = "__JINJA__:Is it a {{inst.__name__}}?"

    if not isInstanceInProcess(sol_name, inst, state.solution_process):
        raise ValueError("%r is not a %s in the solution environment" % (sol_name, type(inst)))

    _msg = state.build_message(not_instance_msg, {'inst': inst})
    feedback = Feedback(_msg, state)
    rep.do_test(InstanceProcessTest(stu_name, inst, state.student_process, feedback))

    return state

def check_df(index, missing_msg=None, not_instance_msg=None, expand_msg=None, state=None):
    """Check whether a DataFrame was defined and it is the right type"""
    child = check_object(index, missing_msg=missing_msg, expand_msg=expand_msg, state=state, typestr="pandas DataFrame")
    is_instance(pd.DataFrame, not_instance_msg=not_instance_msg, state=child)
    return child

def check_keys(key, missing_msg=None, expand_msg=None, state=None):
    """Check whether an object (dict, DataFrame, etc) has a key.

    ``check_keys()`` can currently only be used when chained from ``check_object()``, the function that is
    used to 'zoom in' on the object of interest.

    Args:
        key (str): Name of the key that the object should have.
        missing_msg (str): When specified, this overrides the automatically generated
            message in case the key does not exist.
        state (State): The state that is passed in through the SCT chain (don't specify this).

    :Example:

        Student code and solution code::

            x = {'a': 2}

        SCT::

            # Verify that x contains a key a
            Ex().check_object('x').check_keys('a')

            # Verify that x contains a key a and a is correct.
            Ex().check_object('x').check_keys('a').has_equal_value()

    """

    if missing_msg is None:
        missing_msg = "__JINJA__:There is no {{ 'column' if 'DataFrame' in parent.typestr else 'key' }} `'{{key}}'`."
    if expand_msg is None:
        expand_msg = "__JINJA__:Did you correctly set the {{ 'column' if 'DataFrame' in parent.typestr else 'key' }} `'{{key}}'`? "

    rep = Reporter.active_reporter

    sol_name = state.solution_parts.get('name')
    stu_name = state.student_parts.get('name')

    if not isDefinedCollInProcess(sol_name, key, state.solution_process):
        raise NameError("Not all keys you specified are actually keys in %s in the solution process" % sol_name)

    # check if key available
    _msg = state.build_message(missing_msg, {'key': key})
    rep.do_test(DefinedCollProcessTest(stu_name, key, state.student_process, 
                                       Feedback(_msg, state)))

    def get_part(name, key, highlight):
        if isinstance(key, str):
            slice_val = ast.Str(s=key)
        else:
            slice_val = ast.parse('{}'.format(key)).body[0].value
        expr = ast.Subscript(value=ast.Name(id=name, ctx=ast.Load()),
                             slice=ast.Index(value=slice_val),
                             ctx=ast.Load())
        ast.fix_missing_locations(expr)
        return {
            'node': expr,
            'highlight': highlight
        }

    stu_part = get_part(stu_name, key, state.student_parts.get('highlight'))
    sol_part = get_part(sol_name, key, state.solution_parts.get('highlight'))
    append_message = {'msg': expand_msg, 'kwargs': {'key': key }}
    child = part_to_child(stu_part, sol_part, append_message, state)
    return child
