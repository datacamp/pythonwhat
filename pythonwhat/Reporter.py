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

    def __init__(self, error=None):
        self.success_msg = "Great work!"
        self.error = error
        self.errors_allowed = False

    def do_test(self, testobj):
        """Do test.

        Execute a given test, unless some previous test has failed. If the test has failed,
        the state of the reporter changes and the feedback is kept.
        """

        if isinstance(testobj, Test):
            testobj.test()
            result = testobj.result
            if (not result):
                feedback = testobj.get_feedback()
                raise TestFail(feedback, self.build_failed_payload(feedback))

        else:
            result = None
            testobj()    # run function for side effects

        return result

    def build_failed_payload(self, feedback):
        if not feedback.line_info:
            return {
                "correct": False,
                "message": Reporter.to_html(feedback.message)
                }
        else:
            return {
                "correct": False,
                "message": Reporter.to_html(feedback.message),
                "line_start": feedback.line_info["line_start"],
                "column_start": feedback.line_info["column_start"] + 1,
                "line_end": feedback.line_info["line_end"],
                "column_end": feedback.line_info["column_end"]
                }

    def build_final_payload(self):
        if (self.error and not self.errors_allowed):
            feedback_msg = "Have a look at the console: your code contains an error. Fix it and try again!"
            return {
                "correct": False,
                "message": Reporter.to_html(feedback_msg)
                }
        else:
            return({
                "correct": True,
                "message": Reporter.to_html(self.success_msg)
                })

    @staticmethod
    def to_html(msg):
        return(re.sub("<p>(.*)</p>", "\\1", markdown2.markdown(msg)).strip())
