import re
import pythonwhat.feedback as fb
import numpy as np

"""
This file contains all tests that can be done on specific objects. All tests are represented
an object. Tests that are alike can inherit from the same superclass. A test is first initialized
and can then be performed by calling the 'test()' function. The result will be stored inside
the result boolean. A test contains a failure message, which can be used by the reporter to
show when the test failed.
"""


class Test(object):
    """
    The basic Test. It should only contain a failure message, as all tests should result in
    a failure message when they fail.

    Note:
                    This test should not be used by itself, subclasses should be used.

    Attributes:
            failure_msg (str): A string containing the failure message in case the test fails.
            result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, failure_msg):
        """
        Initialize the standard test.

        Args:
                failure_msg (str): The failure message will be set to this.
        """
        if (issubclass(type(failure_msg), fb.FeedbackMessage)):
            self.failure_msg = failure_msg
        elif (issubclass(type(failure_msg), str)):
            self.failure_msg = fb.FeedbackMessage(failure_msg)
        else:
            raise TypeError(
                "Not a valid type for failure_msg: %r" %
                type(failure_msg))

        self.result = None

    def test(self):
        """
        Wrapper around specific tests. Tests only get one chance.
        """
        if self.result is None:
            try:
                self.specific_test()
                self.result = np.array(self.result).all()
            except:
                self.result = False

    def specific_test(self):
        """
        Perform the actual test. For the standard test, result will be set to False.
        """
        self.result = False

    def feedback(self):
        if (issubclass(type(self.failure_msg), fb.FeedbackMessage)):
            return(self.failure_msg.generateString())
        else:
            # Shouldn't happen.
            return(None)


class DefinedTest(Test):
    """
    Check if an object with a certain name is defined in a collection.

    Attributes:
            failure_msg (str): A string containing the failure message in case the test fails.
            obj (str): Contains the name of the object that is searched for.
            coll (list/dict/set): Contains any object on which the 'in' operator can be performed.
            result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj, coll, failure_msg):
        """
        Initialize the defined test.

        Args:
                obj (str): Value to which obj will be set.
                coll (list/dict/set): The coll will be set to this.
                failure_msg (str): The failure message will be set to this.
        """
        super().__init__(failure_msg)
        self.obj = obj
        self.coll = coll

    def specific_test(self):
        """
        Perform the actual test. Result is True if obj is in coll, False otherwise.

        """
        self.result = (self.obj in self.coll)


class EnvironmentTest(Test):
    """
    This class should be subclassed. Subclasses of this test will be performed within
    the student and the solution environment.

    Note:
            This test should not be used by itself, subclasses should be used.

    Attributes:
            failure_msg (str): A string containing the failure message in case the test fails.
            student_env (dict): Contains the student environment as a dictionary.
            solution_env (dict): Contains the solution environment as a dictionary.
            result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj, student_env, solution_env, failure_msg):
        """
        Initialize with a student and solution environment.

        Args:
                student_env (dict): The student environment will be set to this.
                solution_env (dict): The solution environment will be set to this.
                failure_msg (str): The failure message will be set to this.
        """
        super().__init__(failure_msg)
        self.student_env = student_env
        self.solution_env = solution_env
        self.obj = obj
        self.failure_msg.add_information("student", self.student_env[self.obj])
        self.failure_msg.add_information(
            "solution", self.solution_env[self.obj])

# TODO (Vincent): Add support for equivalence of strings. Use hamming distance.


class EquivalentEnvironmentTest(EnvironmentTest):
    """
    Check if an variable with a certain name is equivalent in both student and solution
    environment. Equivalence means the objects are almost the same. This test should
    only be used with numeric variables (for now).

    Attributes:
            failure_msg (str): A string containing the failure message in case the test fails.
            obj (str): The name of the variable that will be tested in both environments.
            student_env (dict): Contains the student environment as a dictionary.
            solution_env (dict): Contains the solution environment as a dictionary.
            result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj, student_env, solution_env, failure_msg):
        """
        Initialize with an object, student and solution environment.

        Args:
                obj (str): The variable name, obj will be set to this.
                student_env (dict): The student environment will be set to this.
                solution_env (dict): The solution environment will be set to this.
                failure_msg (str): The failure message will be set to this.
        """
        super().__init__(obj, student_env, solution_env, failure_msg)

    """
	Perform the actual test. result is set to False if the difference between the variables is
	more than 0.5e-8, True otherwise.
	"""

    def specific_test(self):
        self.result = (
            abs(self.student_env[self.obj] - self.solution_env[self.obj]) < 0.5e-8)


class EqualEnvironmentTest(EnvironmentTest):
    """
    Check if an variable with a certain name is equal in both student and solution
    environment. Equal means the objects are exactly the same.

    Attributes:
            failure_msg (str): A string containing the failure message in case the test fails.
            obj (str): The name of the variable that will be tested in both environments.
            student_env (dict): Contains the student environment as a dictionary.
            solution_env (dict): Contains the solution environment as a dictionary.
            result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj, student_env, solution_env, failure_msg):
        """
        Initialize with an object, student and solution environment.

        Args:
                obj (str): The variable name, obj will be set to this.
                student_env (dict): The student environment will be set to this.
                solution_env (dict): The solution environment will be set to this.
                failure_msg (str): The failure message will be set to this.
        """
        super().__init__(obj, student_env, solution_env, failure_msg)

    def specific_test(self):
        """
        Perform the actual test. result is set to False if the variables differ, True otherwise.
        """
        self.result = (
            self.student_env[
                self.obj] == self.solution_env[
                self.obj])

# TODO (Vincent): Add support for equivalence of strings. Use hamming distance.


class EquivalentTest(Test):
    """
    Check if two objects are equivalent. Equivalence means the objects are almost the same.
    This test should only be used with numeric variables (for now).

    Attributes:
            failure_msg (str): A string containing the failure message in case the test fails.
            obj1 (str): The first object that should be compared with.
            obj2 (str): This object is compared to obj1.
            result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj1, obj2, failure_msg):
        """
        Initialize with two objects.

        Args:
                obj1 (str): The first object, obj1 will be set to this.
                obj2 (str): The second object, obj2 will be set to this.
                failure_msg (str): The failure message will be set to this.
        """
        super().__init__(failure_msg)
        self.obj1 = obj1
        self.obj2 = obj2

    def specific_test(self):
        """
        Perform the actual test. result is set to False if the difference between the objects is
        more than 0.5e-8, True otherwise.
        """
        self.result = (abs(self.obj1 - self.obj2) < 0.5e-8)


class EqualTest(Test):
    """
    Check if two objects are equal. Equal means the objects are exactly the same.
    This test should only be used with numeric variables (for now).

    Attributes:
            failure_msg (str): A string containing the failure message in case the test fails.
            obj1 (str): The first object that should be compared with.
            obj2 (str): This object is compared to obj1.
            result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj1, obj2, failure_msg):
        """
        Initialize with two objects.

        Args:
                obj1 (str): The first object, obj1 will be set to this.
                obj2 (str): The second object, obj2 will be set to this.
                failure_msg (str): The failure message will be set to this.
        """
        super().__init__(failure_msg)
        self.obj1 = obj1
        self.obj2 = obj2

    def specific_test(self):
        """
        Perform the actual test. result is set to False if the objects differ, True otherwise.
        """
        if isinstance(self.obj1, type(self.obj2)):
            self.result = (self.obj1 == self.obj2)
        else:
            self.result = False


class BiggerTest(Test):
    """
    Check if two objects are equal. Equal means the objects are exactly the same.
    This test should only be used with numeric variables (for now).

    Attributes:
            failure_msg (str): A string containing the failure message in case the test fails.
            obj1 (str): The first object that should be compared with.
            obj2 (str): This object is compared to obj1.
            result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj1, obj2, failure_msg):
        """
        Initialize with two objects.

        Args:
                obj1 (str): The first object, obj1 will be set to this.
                obj2 (str): The second object, obj2 will be set to this.
                failure_msg (str): The failure message will be set to this.
        """
        super().__init__(failure_msg)
        self.obj1 = obj1
        self.obj2 = obj2

    def specific_test(self):
        """
        Perform the actual test. result is set to False if the objects differ, True otherwise.
        """
        self.result = (self.obj1 > self.obj2)


class StringContainsTest(Test):
    """
    Check if a string is present in a text. Can use literal strings or a regex.

    Attributes:
            failure_msg (str): A string containing the failure message in case the test fails.
            string (regex/str):  String or regular expression which is searched for.
            search_string (str): The text in which is searched.
            pattern (bool): If set to True, string is matched with a regex. Literal otherwise.
            result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, string, search_string, pattern, failure_msg):
        """
        Initialize with a string to look for, a string to search and whether or not to look for a pattern.

        Args:
                string (regex/str):  The string to look for will be set to this.
                search_string (str): The string to search in will be set to this.
                pattern (bool): The pattern boolean will be set to this.
                failure_msg (str): The failure message will be set to this.
        """
        super().__init__(failure_msg)
        self.string = string
        self.search_string = search_string
        self.pattern = pattern

    def specific_test(self):
        """
        Perform the actual test. result will be True if string is found (whether or not with a pattern),
        False otherwise.
        """
        if self.pattern:
            self.result = (
                re.search(
                    self.search_string,
                    self.string) is not None)
        else:
            self.result = (self.string.find(self.search_string) is not -1)

# TODO (Vincent): Remove this -> same as DefinedTest - used in test_operator()


class CollectionContainsTest(Test):

    def __init__(self, obj, coll, failure_msg):
        super().__init__(failure_msg)
        self.obj = obj
        self.coll = coll

    def specific_test(self):
        self.result = self.obj in self.coll
