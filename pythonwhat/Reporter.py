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
        self.feedback_msg = "Oh no, your solution is incorrect! Please, try again."
        self.success_msg = "Great work!"
        self.allow_errors = False
        self.correct_steps = 0

    def set_success_msg(self, success_msg):
        self.success_msg = success_msg

    def allow_errors(self):
        self.allow_errors = True

    def reject_errors(self):
        self.allow_errors = False

    def inc_correct_steps_to(self, correct_steps):
        if self.correct_steps < correct_steps:
            self.correct_stepst = correct_steps

    def fail(self, failure_msg):
        self.failed_test = True
        self.feedback_msg = failure_msg

    def do_test(self, test_object):
        """Do test.

        Execute a given test, unless some previous test has failed. If the test has failed,
        the state of the reporter changes and the feedback is kept.
        """
        if self.failed_test:
            return

        test_object.test()
        result = test_object.result
        if (not result):
            self.failed_test = True
            self.feedback_msg = test_object.feedback()

    def do_tests(self, test_objects):
        """Do multiple tests.

        Execute an array of tests.
        """
        for test_object in test_objects:
            if self.failed_test:
                break

            self.do_test(test_object)
