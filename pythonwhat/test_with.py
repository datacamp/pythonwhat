import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedTest, EqualTest, Test

from pythonwhat import utils

ordinal = lambda n: "%d%s" % (
    n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])

def test_with(index,
              context_vals=False,
              context=None,
              body=None,
              undefined_msg=None,
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
    except KeyError:
        raise NameError("not enough with statements in solution environment" % name)

    try:
        student_with = student_withs[index]
    except:
        rep.do_test(Test(undefined_msg or "Define more `with` statements."))
        return

    if body is not None:
        subtree_solution = solution_with['body']
        subtree_student = student_with['body']
        failed_before = rep.failed_test
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
            rep.do_test(Test("In your %s `with` statement, you're not using a correct context manager." % (ordinal(index))))
            return
        except (AssertionError, ValueError, TypeError):
            rep.do_test(Test("In your %s `with` statement, the number of values in your context manager " + \
                "doesn't correspond to the number of variables you're trying to assign it to." % (ordinal(index))))
            return
        child = state.to_child_state(subtree_student, subtree_solution)
        child.solution_env = solution_env
        child.student_env = student_env
        try:
            body()
        finally:
            close_solution_context = context_objs_exit(solution_context_objs)
            if close_solution_context:
                raise Exception("error in the solution, closing the with on line %d fails with: %s" %
                    (solution_with['lineno'], close_solution_context))

            if context_objs_exit(student_context_objs):
                rep.do_test(Test("Your %s `with` statement can not be closed off correctly, you're " + \
                    "not using the context manager correctly." % (ordinal(index))))
        child.to_parent_state()
        if expand_message and (failed_before is not rep.failed_test):
            rep.feedback_msg = ("Check the `with` statement on line %d. " % student_with['lineno']) + \
                rep.feedback_msg

def context_env_update(context_list, env):
    env_update = {}
    context_objs = []
    for context in context_list:
        context_obj = eval(
            compile(context['context_expr'], '<context_eval>', 'eval'),
            env)
        context_objs.append(context_obj)
        context_obj_init = context_obj.__enter__()
        print("OPENED")
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
            context_obj.__exit__()
            print("CLOSED")
        except Exception as e:
            got_error = e

    return got_error

