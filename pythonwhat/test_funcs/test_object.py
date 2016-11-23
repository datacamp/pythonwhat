import ast
from pythonwhat.parsing import ObjectAssignmentParser
from pythonwhat.Test import DefinedProcessTest, EqualProcessTest
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isDefinedInProcess, getRepresentation
from pythonwhat.check_funcs import part_to_child, has_equal_value

MSG_UNDEFINED = "Have you defined `{parent[sol_part][name]}`?"
MSG_INCORRECT = "The contents of `{parent[sol_part][name]}` aren't correct."

def test_object(name,
                eq_condition="equal",
                eq_fun=None,
                do_eval=True,
                undefined_msg=None,
                incorrect_msg=None,
                state=None):
    """Test object.

    The value of an object in the ending environment is compared in the student's environment and the
    solution environment.

    Args:
        name (str): the name of the object which value has to be checked.
        eq_condition (str): how objects are compared. Currently, only "equal" is supported,
          meaning that the object in student and solution process should have exactly the same value.
        do_eval (bool): if False, the object will only be checked for existence. Defaults to True.
        undefined_msg (str): feedback message when the object is not defined
        incorrect_msg (str): feedback message if the value of the object in the solution environment doesn't match
          the one in the student environment.

    Examples:
        Student code

        | ``a = 1``
        | ``b = 5``

        Solution code

        | ``a = 1``
        | ``b = 2``

        SCT

        | ``test_object("a")``: pass.
        | ``test_object("b")``: fail.
    """
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_object")

    child = check_object(name, undefined_msg or MSG_UNDEFINED, state=state)

    if do_eval:

        has_equal_value(incorrect_msg or MSG_INCORRECT, state=child)

def get_assignment_node(obj_ass, name):
    nodes = obj_ass[name] if name in obj_ass else None
    
    # found a single case of assigning name
    if nodes and len(nodes) == 1: 
        return nodes[0]

# Check functions -------------------------------------------------------------

def check_object(name, undefined_msg=MSG_UNDEFINED, state=None):
    rep = Reporter.active_reporter

    if not isDefinedInProcess(name, state.solution_process):
        raise NameError("%r not in solution environment " % name)

    # create child state, using either parser output, or create part from name
    fallback = lambda: ObjectAssignmentParser.get_part(name)
    stu_part = state.student_object_assignments.get(name, fallback())
    sol_part = state.solution_object_assignments.get(name, fallback())
    
    child = part_to_child(stu_part, sol_part, {'msg': '', 'kwargs': {}}, state)

    # test object exists
    _msg = child.build_message(undefined_msg)
    rep.do_test(DefinedProcessTest(name, child.student_process, Feedback(_msg)))

    return child
