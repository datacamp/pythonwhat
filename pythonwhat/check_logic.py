from types import GeneratorType
from functools import partial
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test, TestFail
from pythonwhat.Feedback import Feedback
import copy
import ast

def multi(*args, state=None):
    """Run multiple subtests. Return original state (for chaining)."""
    if any(args):
        rep = Reporter.active_reporter

        # when input is a single list of subtests
        if len(args) == 1 and isinstance(args[0], (list, tuple, GeneratorType)):
            args = args[0]

        for test in args:
            # assume test is function needing a state argument
            # partial state so reporter can test
            rep.do_test(partial(test, state=state))

    # return original state, so can be chained
    return state

def check_not(*tests, msg, state=None):
    """Run multiple subtests that should fail. If all subtests fail, returns original state (for chaining)

    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        args: one or more sub-SCTs to run.
    :Example:
        Thh SCT below runs two test_student_typed cases.. ::

            Ex().multi(test_student_typed('INNER'), test_student_typed('OUTER'))

        If students use INNER (JOIN) or OUTER (JOIN) in their code, this test will fail.

    Note:
        - This function is currently only tested in working with test_student_typed in the subtests.
        - This function can be thought as a NOT(x OR y OR ...) statement, since all tests it runs must fail
        - This function can be considered a direct counterpart of multi.

    """
    rep = Reporter.active_reporter

    for test in tests:
        try:
            multi(test, state=state)
        except TestFail:
            # it fails, as expected, off to next one
            continue
        return rep.do_test(Test(msg))

    # return original state, so can be chained
    return state

def check_or(*tests, state=None):
    """Test whether at least one SCT passes."""

    rep = Reporter.active_reporter

    success = False
    first_feedback = None
    for test in tests:
        try:
            multi(test, state=state)
            success = True
        except TestFail as e:
            if not first_feedback: first_feedback = e.feedback
        if success:
            return
    
    rep.do_test(Test(first_feedback))

def check_correct(check, diagnose, state=None):
    """Allows feedback from a diagnostic SCT, only if a check SCT fails. """
    def diagnose_and_check(state=None):
        # use multi twice, since diagnose and check may be lists of tests
        multi(diagnose, state=state)
        multi(check, state=state)

    check_or(diagnose_and_check, check, state=state)

# utility functions -----------------------------------------------------------

def quiet(n = 0, state=None):
    """Turn off prepended messages. Defaults to turning all off."""
    cpy = copy.copy(state)
    hushed = [{**m, 'msg': ""} for m in cpy.messages]
    cpy.messages = hushed
    return cpy

def fail(msg="", state=None):
    """Fail test with message"""
    rep = Reporter.active_reporter
    _msg = state.build_message(msg)
    rep.do_test(Test(Feedback(_msg, state)))

    return state

def override(solution, state=None):
    """Change the focused solution code."""

    # the old ast may be a number of node types, but generally either a
    # (1) ast.Module, or for single expressions...
    # (2) whatever was grabbed using module.body[0]
    # (3) module.body[0].value, when module.body[0] is an Expr node
    old_ast = state.solution_tree
    new_ast = ast.parse(solution)
    if not isinstance(old_ast, ast.Module) and len(new_ast.body) == 1:
        expr = new_ast.body[0]
        candidates = [expr, expr.value] if isinstance(expr, ast.Expr) else [expr]
        for node in candidates:
            if isinstance(node, old_ast.__class__): 
                new_ast = node
                break

    kwargs  = state.messages[-1] if state.messages else {}
    child = state.to_child_state(
            solution_subtree = new_ast,
            student_subtree = state.student_tree,
            highlight = state.highlight,
            append_message = {'msg': "", 'kwargs': kwargs}
            )

    return child


def set_context(*args, state=None, **kwargs):
    """Update context values for student and solution environments.
    
    When ``has_equal_x()`` is used after this, the context values (in ``for`` loops and function definitions, for example)
    will have the values specified throught his function. It is the function equivalent of the ``context_vals`` argument of
    the ``has_equal_x()`` functions.

    - Note 1: excess args and unmatched kwargs will be unused in the student environment.
    - Note 2: positional arguments are more robust to the student using different names for context values.
    - Note 3: You have to specify arguments either by position, either by name. A combination is not possible.

    :Example:

        Solution code::

            total = 0
            for i in range(10):
                print(i ** 2)

        Student submission that will pass (different iterator, different calculation)::

            total = 0
            for j in range(10):
                print(j * j)

        SCT::

            # set_context is robust against different names of context values.
            Ex().check_for_loop().check_body().multi(
                set_context(1).has_equal_output(),
                set_context(2).has_equal_output(),
                set_context(3).has_equal_output()
            )

            # equivalent SCT, by setting context_vals in has_equal_output()
            Ex().check_for_loop().check_body().\\
                multi([s.has_equal_output(context_vals=[i]) for i in range(1, 4)])

    """

    stu_crnt = state.student_context.context
    sol_crnt = state.solution_context.context

    # for now, you can't specify both
    if len(args) > 0 and len(kwargs) > 0:
        raise ValueError("In set_context() make sure to specify arguments either by position, either by name")

    # set args specified by pos -----------------------------------------------
    if args:
        # stop if too many pos args for solution
        if len(args) > len(sol_crnt): 
            raise IndexError("Too many positional args. There are {} context vals, but tried to set {}"
                                .format(len(sol_crnt), len(args)))
        # set pos args
        upd_sol = sol_crnt.update(dict(zip(sol_crnt.keys(), args)))
        upd_stu = stu_crnt.update(dict(zip(stu_crnt.keys(), args)))
    else:
        upd_sol = sol_crnt
        upd_stu = stu_crnt

    # set args specified by keyword -------------------------------------------
    if kwargs:
        # stop if keywords don't match with solution
        if set(kwargs) - set(upd_sol):
            raise KeyError("Context val names are {}, but tried to set {}"
                                .format(upd_sol or "none", kwargs.keys()))
        out_sol = upd_sol.update(kwargs)
        # need to match keys in kwargs with corresponding keys in stu context
        # in case they used, e.g., different loop variable names
        match_keys = dict(zip(sol_crnt.keys(), stu_crnt.keys()))
        out_stu = upd_stu.update({match_keys[k]: v for k,v in kwargs.items() if k in match_keys})
    else:
        out_sol = upd_sol
        out_stu = upd_stu

    return state.to_child_state(student_context = out_stu,
                                solution_context = out_sol,
                                highlight = state.highlight)

def set_env(state = None, **kwargs):
    """Update/set environemnt variables for student and solution environments.

    When ``has_equal_x()`` is used after this, the variables specified through this function will
    be available in the student and solution process. Note that you will not see these variables
    in the student process of the state produced by this function: the values are saved on the state
    and are only added to the student and solution processes when ``has_equal_ast()`` is called.

    :Example:

        Student and Solution Code::

            a = 1
            if a > 4:
                print('pretty large')

        SCT::

            # check if condition works with different values of a
            Ex().check_if_else().check_test().multi(
                set_env(a = 3).has_equal_value()
                set_env(a = 4).has_equal_value()
                set_env(a = 5).has_equal_value()
            )

            # equivalent SCT, by setting extra_env in has_equal_value()
            Ex().check_if_else().check_test().\\
                multi([has_equal_value(extra_env={'a': i}) for i in range(3, 6)])
    """

    stu_crnt = state.student_env.context
    sol_crnt = state.solution_env.context

    stu_new = stu_crnt.update(kwargs)
    sol_new = sol_crnt.update(kwargs)

    return state.to_child_state(student_env = stu_new,
                                solution_env = sol_new,
                                highlight = state.highlight)

def disable_highlighting(state = None):
    """Disable highlighting in the remainder of the SCT chain.

    Include this function if you want to avoid that pythonwhat marks which part of the student submission is incorrect.

    :Examples:

        SCT that will mark the 'number' portion if it is incorrect::

            Ex().check_function('round').check_args(0).has_equal_ast()

        SCT chains that will not mark certain mistakes. The earlier you put the function, the more types of mistakes will no longer be highlighted::

            Ex().disable_highlighting().check_function('round').check_args(0).has_equal_ast()
            Ex().check_function('round').disable_highlighting().check_args(0).has_equal_ast()
            Ex().check_function('round').check_args(0).disable_highlighting().has_equal_ast()
    """
    return state.to_child_state(highlighting_disabled = True)
