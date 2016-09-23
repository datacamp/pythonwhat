from pythonwhat.Feedback import Feedback

def sub_test(state, rep, closure, subtree_student, subtree_solution, incorrect_part,
                student_context=None, solution_context=None, expand_message=""):
    prefix = expand_message.format(incorrect_part=incorrect_part) if expand_message else ""
    if closure:
        child = state.to_child_state(subtree_student, subtree_solution)
        child.student_context = student_context
        child.solution_context = solution_context
        rep.do_test(closure, prefix, subtree_student)
        child.to_parent_state()
