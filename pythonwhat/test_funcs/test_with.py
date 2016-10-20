import ast
from pythonwhat.State import State
from pythonwhat.Feedback import Feedback
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import EqualTest, Test
from pythonwhat import utils
from pythonwhat.tasks import setUpNewEnvInProcess, breakDownNewEnvInProcess

from pythonwhat.sub_test import sub_test

def test_with(index,
              context_vals=False, # whether to check number of context vals
              context_tests=None, # check on context expressions
              body=None,
              undefined_msg=None,
              context_vals_len_msg=None,
              context_vals_msg=None,
              expand_message=True,
              state=None):
    """Test a with statement.
with open_file('...') as bla:

    [ open_file('...').__enter__() ]


with open_file('...') as file:
    [ ]

    """
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_with")

    index = index - 1

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

        for (solution_context, student_context) in zip(solution_with['context'], student_with['context']):
            c_context_vals_msg = context_vals_msg or "In your %s `with` statement, make sure to use the correct context variable names. Was expecting `%s` but got `%s`."\
                % (utils.get_ord(index + 1), names_as_string(solution_context['optional_vars']),
                    names_as_string(student_context['optional_vars']))
            rep.do_test(EqualTest(solution_context['optional_vars'], student_context['optional_vars'],
                Feedback(c_context_vals_msg, student_with['node'])))

    if context_tests is not None:
        feedback_fmt = "Check the {0} context in the {1} `with` statement. " 

        if not isinstance(context_tests, list):
            context_tests = [context_tests]
        for i in range(len(context_tests)):

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
            # TODO does the test about need to be in this loop?
            prepend = feedback_fmt.format(utils.get_ord(i+1), utils.get_ord(index + 1)) if expand_message else ""
            sub_test(state, rep, context_test, student_context, solution_context, expand_message=prepend)

    if body is not None:

        solution_res = setUpNewEnvInProcess(process = state.solution_process,
                                            context = solution_with['context'])
        if isinstance(solution_res, Exception):
            raise Exception("error in the solution, running test_with() on with %d: %s" % (index, str(solution_res)))

        student_res = setUpNewEnvInProcess(process = state.student_process,
                                           context = student_with['context'])
        if isinstance(student_res, AttributeError):
            rep.do_test(Test(Feedback("In your %s `with` statement, you're not using a correct context manager." % (utils.get_ord(index + 1)), student_with['node'])))

        if isinstance(student_res, (AssertionError, ValueError, TypeError)):
            rep.do_test(Test(Feedback("In your %s `with` statement, the number of values in your context manager " + \
                "doesn't correspond to the number of variables you're trying to assign it to." % (utils.get_ord(index + 1)), student_with['node'])))

        child = state.to_child_state(student_with['body'], solution_with['body'])

        # TODO clean up feedback related variables a bit
        #      add line_info unit test
        # feedback pasted on failed sub_test messages
        feedback = "Check the body of the %s `with` statement. " % utils.get_ord(index + 1)
        try:
            sub_test(child, rep, body, None, None, 
                     expand_message=feedback if expand_message else "")
        finally:
            if breakDownNewEnvInProcess(process = state.solution_process):
                raise Exception("error in the solution, closing the %s with fails with: %s" %
                    (utils.get_ord(index + 1), close_solution_context))

            if breakDownNewEnvInProcess(process = state.student_process):

                rep.do_test(Test(Feedback("Your %s `with` statement can not be closed off correctly, you're " + \
                                "not using the context manager correctly." % (utils.get_ord(index + 1)), student_width['node'])),
                            prepend_on_fail = feedback if expand_message else "",
                            fallback_ast = student_with['body'])

        child.to_parent_state()

def names_as_string(names):
    if len(names) > 1:
        return ("(%s)" % (', '.join(names)))
    else:
        return names[0]
