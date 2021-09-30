import re
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from pythonwhat.tasks import *
from protowhat.Test import Test

"""
This file contains all tests that can be done on specific objects. All tests are represented as
an object. Tests that are alike can inherit from the same superclass. A test is first initialized
and can then be performed by calling the 'test()' function. The result will be stored inside
the result boolean. A test contains a failure message, which can be used by the reporter to
show when the test failed.
"""


# Testing definition


class DefinedProcessTest(Test):
    def __init__(self, name, process, feedback):
        super().__init__(feedback)
        self.name = name
        self.process = process

    def test(self):
        self.result = isDefinedInProcess(self.name, self.process)


class DefinedCollTest(Test):
    """
    Check if an object with a certain name is defined in a collection.

    Attributes:
        feedback (str): A string containing the failure message in case the test fails.
        name (str): Contains the name of the object that is searched for.
        collection (list/dict/set): Contains any object on which the 'in' operator can be performed.
        result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, name, collection, feedback):
        super().__init__(feedback)
        self.name = name
        self.collection = collection

    def test(self):
        self.result = self.name in self.collection


class DefinedCollProcessTest(Test):
    def __init__(self, name, key, process, feedback):
        super().__init__(feedback)
        self.name = name
        self.key = key
        self.process = process

    def test(self):
        self.result = isDefinedCollInProcess(self.name, self.key, self.process)


# Testing class


class InstanceProcessTest(Test):
    def __init__(self, name, klass, process, feedback):
        super().__init__(feedback)
        self.name = name
        self.klass = klass
        self.process = process

    def test(self):
        self.result = isInstanceInProcess(self.name, self.klass, self.process)


# Testing equality


class EqualTest(Test):
    """
    Check if two objects are equal. Equal means the objects are exactly the same.
    This test should only be used with numeric variables (for now).

    Attributes:
        feedback (str): A string containing the failure message in case the test fails.
        obj1 (str): The first object that should be compared with.
        obj2 (str): This object is compared to obj1.
        result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj1, obj2, feedback, func=None):
        super().__init__(feedback)
        self.obj1 = obj1
        self.obj2 = obj2
        self.func = func if func is not None else is_equal

    def test(self):
        """
        Perform the actual test. result is set to False if the objects differ, True otherwise.
        """
        self.result = np.array(self.func(self.obj1, self.obj2)).all()


# Helpers for testing equality


def areinstance(x, y, tuple_of_classes):
    return isinstance(x, tuple_of_classes) and isinstance(y, tuple_of_classes)


# For equality of ndarrays, list, dicts, pd Series and pd DataFrames:
# First try to the faster equality functions. If these don't pass,
# Run the assertions that are typically slower.
def is_equal(x, y):
    try:
        if areinstance(x, y, (Exception,)):
            # Types of errors don't matter (this is debatable)
            return str(x) == str(y)
        if areinstance(x, y, (np.ndarray, dict, list, tuple)):
            np.testing.assert_equal(x, y)
            return True
        elif areinstance(x, y, (map, filter)):
            return np.array_equal(list(x), list(y))
        elif areinstance(x, y, (pd.DataFrame,)):
            if x.equals(y):
                return True
            assert_frame_equal(x, y)
            return True
        elif areinstance(x, y, (pd.Series,)):
            if x.equals(y):
                return True
            assert_series_equal(x, y)
            return True
        else:
            return x == y

    except Exception:
        return False


# Others


class BiggerTest(EqualTest):
    """
    Check if the first object is greater than another.
    """

    def __init__(self, *args):
        super().__init__(*args, func=lambda obj1, obj2: obj1 > obj2)


class StringContainsTest(Test):
    """
    Check if a string is present in a text. Can use literal strings or a regex.

    Attributes:
        feedback (str): A string containing the failure message in case the test fails.
        string (regex/str):  String or regular expression which is searched for.
        search_string (str): The text in which is searched.
        pattern (bool): If set to True, string is matched with a regex. Literal otherwise.
        result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, string, search_string, pattern, feedback):
        """
        Initialize with a string to look for, a string to search and whether or not to look for a pattern.

        Args:
            string (regex/str):  The string to look for will be set to this.
            search_string (str): The string to search in will be set to this.
            pattern (bool): The pattern boolean will be set to this.
            feedback (str): The failure message will be set to this.
        """
        super().__init__(feedback)
        self.string = string
        self.search_string = search_string
        self.pattern = pattern

    def test(self):
        """
        Perform the actual test. result will be True if string is found (whether or not with a pattern),
        False otherwise.
        """
        if self.pattern:
            self.result = re.search(self.search_string, self.string) is not None
        else:
            self.result = self.string.find(self.search_string) != -1
