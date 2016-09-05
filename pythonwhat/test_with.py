import ast
from pythonwhat.State import State
from pythonwhat.Feedback import Feedback
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedTest, EqualTest, Test
from pythonwhat import utils


def test_with(index,
              context_vals=False,
              context_tests=None,
              body=None,
              undefined_msg=None,
              context_vals_len_msg=None,
              context_vals_msg=None,
              expand_message=True):
    """Test a with statement.


    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_with")

    index = index - 1

    state.extract_withs()
    solution_withs = state.solution_withs
    student_withs = state.student_withs

    try:
        solution_with = solution_withs[index]
    except IndexError:
        raise NameError("not enough with statements in solution environment")

    try:
        student_with = student_withs[index]
    except:
        rep.do_test(Test(undefined_msg or "Define more `with` statements."))
        return

    if context_vals:
        len_solution_context = len(solution_with['context'])
        len_student_context = len(student_with['context'])

        if len_solution_context > len_student_context:
            enough_contexts_string = "too little"
        else:
            enough_contexts_string = "too many"

        c_context_vals_len_msg = context_vals_len_msg or \
            "In your %s `with` statement, make sure to use the correct number of context variables. It seems you defined %s."\
                % (utils.get_ord(index + 1), enough_contexts_string)

        rep.do_test(EqualTest(len_solution_context, len_student_context, Feedback(c_context_vals_len_msg, student_with['node'])))
        if rep.failed_test:
            return

        for (solution_context, student_context) in zip(solution_with['context'], student_with['context']):
            c_context_vals_msg = context_vals_msg or "In your %s `with` statement, make sure to use the correct context variable names. Was expecting `%s` but got `%s`."\
                % (utils.get_ord(index + 1), names_as_string(solution_context['optional_vars']),
                    names_as_string(student_context['optional_vars']))
            rep.do_test(EqualTest(solution_context['optional_vars'], student_context['optional_vars'],
                Feedback(c_context_vals_msg, student_with['node'])))
            if rep.failed_test:
                return

    if context_tests is not None:
        if not isinstance(context_tests, list):
            context_tests = [context_tests]
        for i in range(len(context_tests)):
            if rep.failed_test:
                return
            context_test = context_tests[i]
            try:
                solution_context = solution_with['context'][i]['context_expr']
            except IndexError:
                raise NameError("not enough contexts in %s with statement in solution " % utils.get_ord(index + 1))
            try:
                student_context = student_with['context'][i]['context_expr']
            except:
                rep.do_test(Test(Feedback(context_vals_len_msg or "In your %s `with` statement, make sure to use the correct number of context variables. It seems you defined too little."\
                        % (utils.get_ord(index + 1)), student_with['node'])))
                return
            if rep.failed_test:
                return
            child = state.to_child_state(student_context, solution_context)
            context_test()
            child.to_parent_state()
            if rep.failed_test:
                if expand_message:
                    rep.feedback.message = ("Check the %s context in the %s `with` statement. " % (utils.get_ord(i+1), utils.get_ord(index + 1))) + \
                        rep.feedback.message
                if not rep.feedback.line_info:
                    rep.feedback = Feedback(rep.feedback.message, student_context)

    if rep.failed_test:
        return

    if body is not None:
        subtree_solution = solution_with['body']
        subtree_student = student_with['body']
        solution_env = {}
        solution_env.update(state.solution_env)
        try:
            solution_context_env, solution_context_objs = context_env_update(solution_with['context'], solution_env)
            solution_env.update(solution_context_env)
        except Exception as e:
            raise Exception("error in the solution, running test_with() on with %d: %s" % (index, e))
        student_env = {}
        student_env.update(state.student_env)
        try:
            student_context_env, student_context_objs = context_env_update(student_with['context'], student_env)
            student_env.update(student_context_env)
        except AttributeError:
            rep.do_test(Test(Feedback("In your %s `with` statement, you're not using a correct context manager." % (utils.get_ord(index + 1)), student_with['node'])))
            return
        except (AssertionError, ValueError, TypeError):
            rep.do_test(Test(Feedback("In your %s `with` statement, the number of values in your context manager " + \
                "doesn't correspond to the number of variables you're trying to assign it to." % (utils.get_ord(index + 1)), student_with['node'])))
            return
        if rep.failed_test:
            return
        child = state.to_child_state(subtree_student, subtree_solution)
        child.solution_env = solution_env
        child.student_env = student_env
        try:
            body()
        finally:
            close_solution_context = context_objs_exit(solution_context_objs)
            if close_solution_context:
                raise Exception("error in the solution, closing the %s with fails with: %s" %
                    (utils.get_ord(index + 1), close_solution_context))

            if context_objs_exit(student_context_objs):
                rep.do_test(Test(Feedback("Your %s `with` statement can not be closed off correctly, you're " + \
                    "not using the context manager correctly." % (utils.get_ord(index + 1)), student_width['node'])))
        child.to_parent_state()
        if rep.failed_test:
            if expand_message and rep.failed_test:
                rep.feedback.message = ("Check the body of the %s `with` statement. " % utils.get_ord(index + 1)) + \
                    rep.feedback.message
            if not rep.feedback.line_info and rep.failed_test:
                rep.feedback = Feedback(rep.feedback.message, subtree_student)

def context_env_update(context_list, env):
    env_update = {}
    context_objs = []
    for context in context_list:
        context_obj = eval(
            compile(context['context_expr'], '<context_eval>', 'eval'),
            env)
        context_objs.append(context_obj)
        context_obj_init = context_obj.__enter__()
        context_keys = context['optional_vars']
        if context_keys is None:
            continue
        elif len(context_keys) == 1:
            env_update[context_keys[0]] = context_obj_init
        else:
            assert len(context_keys) == len(context_obj_init)
            for (context_key, current_obj) in zip(context_keys, context_obj_init):
                env_update[context_key] = current_obj
    return (env_update, context_objs)

def context_objs_exit(context_objs):
    got_error = False
    for context_obj in context_objs:
        try:
            context_obj.__exit__(*([None]*3))
        except Exception as e:
            got_error = e

    return got_error

def names_as_string(names):
    if len(names) > 1:
        return ("(%s)" % (', '.join(names)))
    else:
        return names[0]
