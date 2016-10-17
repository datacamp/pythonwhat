from pythonwhat.Test import DefinedProcessTest, EqualProcessTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isDefinedInProcess, getRepresentation, ReprFail

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

    state = check_object(name, undefined_msg, do_eval=do_eval, state=state)

    if do_eval:
        is_equal(name, incorrect_msg, state)

def get_assignment_node(obj_ass, name):
    nodes = obj_ass[name] if name in obj_ass else None
    
    # found a single case of assigning name
    if nodes and len(nodes) == 1: 
        return nodes[0]

# Check functions -------------------------------------------------------------

MSG_UNDEFINED = "Have you defined `{name}`?"
MSG_INCORRECT = "The contents of `{name}` aren't correct."

def check_object(name, undefined_msg, do_eval=True, state=None):
    rep = Reporter.active_reporter
    if not undefined_msg:
        undefined_msg = MSG_UNDEFINED.format(name=name)

    if not isDefinedInProcess(name, state.solution_process):
        raise NameError("%r not in solution environment " % name)

    rep.do_test(DefinedProcessTest(name, state.student_process, Feedback(undefined_msg)))

    if do_eval:
        sol_obj = getRepresentation(name, state.solution_process)
        if isinstance(sol_obj, ReprFail):
            raise NameError(sol_obj.info)

        state.solution_object = sol_obj

    return state

def is_equal(name, incorrect_msg, state=None):
    rep = Reporter.active_reporter
    if not incorrect_msg:
        incorrect_msg = MSG_INCORRECT.format(name=name)

    ass_node = get_assignment_node(state.student_object_assignments, name)
    rep.do_test(EqualProcessTest(name,
                                 state.student_process,
                                 state.solution_object,
                                 Feedback(incorrect_msg, ass_node)))
    return state

