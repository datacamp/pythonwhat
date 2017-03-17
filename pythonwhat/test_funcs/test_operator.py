import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, DefinedCollTest, BiggerTest
from pythonwhat import utils
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import getResultInProcess, ReprFail

def test_operator(index=1,
                  eq_condition="equal",
                  used=None,
                  do_eval=True,
                  not_found_msg=None,
                  incorrect_op_msg=None,
                  incorrect_result_msg=None,
                  state=None):
    """THIS FUNCTION IS DEPRECATED

    Test if operator groups match.

    This function compares an operator group in the student's code with the corresponding one in the solution
    code. It will cause the reporter to fail if the corresponding operators do not match. The fail message
    that is returned will depend on the sort of fail. We say that one operator group correpsonds to a group of
    operators that is evaluated to one value (e.g. 3 + 5 * (1/3)).

    Args:
        index (int): Index of the operator group to be checked. Defaults to 1.
        eq_condition (str): how results of operators are compared. Currently, only "equal" is supported,
            meaning that the result in student and solution process should have exactly the same value.
        used(List[str]): A list of operators that have to be in the group. Valid operators are: "+", "-",
          "*", "/", "%", "**", "<<", ">>", "|", "^", "&" and "//". If the list is None, operators that are
          in the group in the solution have to be in the student code. Defaults to None.
        do_eval (bool): Boolean representing whether the group should be evaluated and compared or not.
          Defaults to True.
        not_found_msg (str): Feedback message if not enough operators groups are found in the student's code.
        incorrect_op_msg (str): Feedback message if the wrong operators are used in the student's code.
        incorrect_result_msg (str): Feedback message if the operator group evaluates to the wrong result in
          the student's code.

    :Example:

        Student code::

            1 + 5 * (3+5)
            1 + 1 * 238

        Solution code::

            3.1415 + 5
            1 + 238

        SCT::

            test_operator(index = 2, used = ["+"]) # pass
            test_operator(index = 2) # fail
            test_operator(index = 1, incorrect_op_msg = "Use the correct operators") # fail
            test_operator(index = 1, used = [], incorrect_result_msg = "Incorrect result") # fail

    """
    rep = Reporter.active_reporter

    # Indexing starts at 1 for the pythonwhat user.
    index = index - 1
    eq_map = {"equal": EqualTest}

    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)

    # Parses through code and extracts a data structure holding all operator groups.
    student_ops = state.student_operators
    solution_ops = state.solution_operators

    # Check if number of student operations is greater than index (which is decreased with 1 by now)
    _msg = state.build_message(not_found_msg or "You didn't define enough operations in your code.")
    rep.do_test(
        BiggerTest(
            len(student_ops),
            index,
            _msg))

    expr_student, used_student = student_ops[index]

    # Throw error if solution code is invalid with SCT
    if index > len(solution_ops) + 1:
        raise IndexError("index not found in solution: %d" % index)

    expr_solution, used_solution = solution_ops[index]

    build_incorrect_msg = "The highlighted operation"

    used_student = set(used_student)
    used_solution = set(used_solution)
    if used is not None:
        used = set(used)
    else:
        used = used_solution

    for op in used:
        if incorrect_op_msg is None:
            incorrect_op_msg = build_incorrect_msg + (" is missing a `%s` operation." % op)

        _msg = state.build_message(incorrect_op_msg)
        rep.do_test(DefinedCollTest(op, used_student,
            Feedback(_msg, expr_student)))

    if (do_eval):


        eval_solution, str_solution = getResultInProcess(process = state.solution_process, tree = expr_solution)

        if str_solution is None:
            raise ValueError("Running the operation in the solution environment raised an error")
        if isinstance(eval_solution, ReprFail):
            raise ValueError("Couldn't find the result of the operation in the solution process: " + eval_solution.info)

        eval_student, str_student = getResultInProcess(process = state.student_process, tree = expr_student)

        # Compare the evaluated operation groups
        if incorrect_result_msg is None:
            if isinstance(str_student, Exception):
                stud_patt = "an error"
            else:
                stud_patt = "`%s`" % utils.shorten_str(str_student)

            incorrect_result_msg = build_incorrect_msg + (" evaluates to %s, should be `%s`." % (stud_patt, utils.shorten_str(str_solution)))

        _msg = state.build_message(incorrect_result_msg)
        rep.do_test(eq_map[eq_condition](
            eval_student, eval_solution, Feedback(_msg, expr_student)))
