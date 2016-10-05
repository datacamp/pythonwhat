from pythonwhat.Feedback import Feedback
import re
import markdown2
from pythonwhat.Test import TestFail, Test

"""
This file holds the reporter class.
"""

class Reporter(object):
    """Do reporting.

    This class holds the feedback- or success message and tracks whether there are failed tests
    or not. All tests are executed trough do_test() in the Reporter.
    """
    active_reporter = None

    def __init__(self):
        self.failed_test = False
        self.feedback = Feedback("Oh no, your solution is incorrect! Please, try again.")
        self.success_msg = "Great work!"
        self.errors_allowed = False
        self.tags = {}
        self.failure_msg_stack = []
        self.fallback_ast = None
        self.test_stack = []
        self.test_mode = None

    def set_success_msg(self, success_msg):
        self.success_msg = success_msg

    def allow_errors(self):
        self.errors_allowed = True

    def reject_errors(self):
        self.errors_allowed = False

    def fail(self, failure_msg):
        self.failed_test = True
        self.feedback = Feedback(failure_msg)

    def do_test(self, testobj, prepend_on_fail="", fallback_ast=None):
        """Do test.

        Execute a given test, unless some previous test has failed. If the test has failed,
        the state of the reporter changes and the feedback is kept.
        """

        if self.test_mode is 'or': 
            return self.test_stack.append([testobj, prepend_on_fail, fallback_ast])

        self.failure_msg_stack.append(prepend_on_fail)
        if fallback_ast: self.fallback_ast = fallback_ast

        if self.failed_test:
            self.feedback.message = "".join(self.failure_msg_stack) + self.feedback.message
            raise TestFail
            return
        if isinstance(testobj, Test):
            testobj.test()
            result = testobj.result
            if (not result):
                self.failed_test = True
                self.feedback = testobj.get_feedback()
                self.feedback.message = "".join(self.failure_msg_stack) + self.feedback.message
                if not self.feedback.line_info and self.fallback_ast: 
                    self.feedback = Feedback(self.feedback.message, self.fallback_ast)
                raise TestFail

        else: 
            result = None
            testobj()    # run function for side effects

        self.failure_msg_stack.pop()
        return result

    def do_tests(self, testobjs):
        """Do multiple tests.

        Execute an array of tests.
        """
        for testobj in testobjs:
            if self.failed_test:
                break

            self.do_test(testobj)

    def start_or_test(self):
        self.test_mode = 'or'
        self.test_stack = []

    def end_or_test(self):
        self.test_mode = None
        first_message = None
        success = False
        for sct_args in self.test_stack: 
            try: 
                self.do_test(*sct_args)
                success = True
            except TestFail as e:
                if not first_message: first_message = self.feedback.message 
                self.failed_test = False

            if success: return
        
        self.failed_test = True
        self.feedback.message = first_message
        raise TestFail

    def set_tag(self, key, value):
        self.tags[key] = value


    def build_payload(self, error):
        if (error and not self.failed_test and not self.errors_allowed):
            feedback_msg = "Your code contains an error: `%s`" % str(error[1])
            return({
                "correct": False,
                "message": Reporter.to_html(feedback_msg),
                "tags": {"fun": "runtime_error"}})

        if self.failed_test:
            if not self.feedback.line_info:
                return({
                    "correct": False,
                    "message": Reporter.to_html(self.feedback.message),
                    "tags": self.tags})
            else:
                # Hack to make it work with campus app implementation
                if self.feedback.line_info["column_start"] is None:
                    col_start = None
                else:
                    col_start = self.feedback.line_info["column_start"] + 1

                return({
                    "correct": False,
                    "message": Reporter.to_html(self.feedback.message),
                    "line_start": self.feedback.line_info["line_start"],
                    "column_start": col_start,
                    "line_end": self.feedback.line_info["line_end"],
                    "column_end": self.feedback.line_info["column_end"],
                    "tags": self.tags})
                
            
        else:
            return({
                "correct": True,
                "message": Reporter.to_html(self.success_msg)
                })

    @staticmethod
    def to_html(msg):
        return(re.sub("<p>(.*)</p>", "\\1", markdown2.markdown(msg)).strip())
