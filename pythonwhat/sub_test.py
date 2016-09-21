from pythonwhat.Feedback import Feedback

def sub_test(state, rep, closure, subtree_student, subtree_solution, incorrect_part,
                student_context=None, solution_context=None, expand_message=""):
    if closure:
        child = state.to_child_state(subtree_student, subtree_solution)
        child.student_context = student_context
        child.solution_context = solution_context
        closure()
        child.to_parent_state()
        if rep.failed_test:
            if expand_message:
                rep.feedback.message = expand_message.format(incorrect_part = incorrect_part) + rep.feedback.message
            if not rep.feedback.line_info:
                rep.feedback = Feedback(rep.feedback.message, subtree_student)
