import pytest
import tests.helper as helper


@pytest.fixture
def data():
    return {
        "DC_PEC": "import numpy as np",
        "DC_SOLUTION": """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except __builtin__.ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except pd.io.common.CParserError:
    x = 'CParserError'
except :
    x = 'someerror'
else :
    passed = True
finally:
    print('done')
        """,
        "DC_SCT": """
Ex().check_try_except().multi(
    check_body().check_function('max', signature = False).check_args(0).has_equal_value(),
    check_handlers('TypeError').has_equal_value(name = 'x'),
    check_handlers('ValueError').has_equal_value(name = 'x'),
    check_handlers('ZeroDivisionError').set_context(e = 'anerror').has_equal_value(name = 'x'),
    check_handlers('IOError').set_context(e = 'anerror').has_equal_value(name = 'x'),
    check_handlers('CParserError').has_equal_value(name = 'x'),
    check_handlers('all').has_equal_value(name = 'x'),
    check_orelse().has_equal_value(name = 'passed'),
    check_finalbody().check_function('print').check_args(0).has_equal_value()
)
""",
    }


def test_fail_01(data):
    data["DC_CODE"] = ""
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "The system wants to check the first try statement but hasn't found it."
    )


def test_fail_02(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerrors'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Did you correctly specify the <code>TypeError</code> <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?"
    )


def test_fail_03(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Are you sure you defined the <code>ValueError</code> <code>except</code> block?"
    )


def test_fail_04(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerrors'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Did you correctly specify the <code>ValueError</code> <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?"
    )


def test_fail_05(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Are you sure you defined the <code>ZeroDivisionError</code> <code>except</code> block?"
    )


def test_fail_06(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except ZeroDivisionError as e:
    x = 'test'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Did you correctly specify the <code>ZeroDivisionError</code> <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?"
    )


def test_fail_07(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except ZeroDivisionError as e:
    x = e
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Are you sure you defined the <code>IOError</code> <code>except</code> block?"
    )


def test_fail_08(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = 'test'
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Did you correctly specify the <code>ZeroDivisionError</code> <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?"
    )


def test_fail_09(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Are you sure you defined the <code>CParserError</code> <code>except</code> block?"
    )

def test_fail_10(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except pd.io.common.CParserError as e:
    x = 'CParserError'
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Are you sure you defined the <code>all</code> <code>except</code> block?"
    )


def test_fail_11(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except pd.io.common.CParserError as e:
    x = 'CParserError'
except :
    x = 'someerrors'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Did you correctly specify the <code>all</code> <code>except</code> block? Are you sure you assigned the correct value to <code>x</code>?"
    )


def test_fail_12(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except pd.io.common.CParserError as e:
    x = 'CParserError'
except :
    x = 'someerror'
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Are you sure you defined the else part?"
    )


def test_fail_13(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except pd.io.common.CParserError as e:
    x = 'CParserError'
except :
    x = 'someerror'
else :
    passed = False
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Did you correctly specify the else part? Are you sure you assigned the correct value to <code>passed</code>?"
    )


def test_fail_14(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except pd.io.common.CParserError as e:
    x = 'CParserError'
except :
    x = 'someerror'
else :
    passed = True
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "Check the first try statement. Are you sure you defined the finally part?"
    )


def test_fail_15(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except pd.io.common.CParserError as e:
    x = 'CParserError'
except :
    x = 'someerror'
else :
    passed = True
finally:
    print('donessss')
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]


def test_pass(data):
    data["DC_CODE"] = data["DC_SOLUTION"]
    sct_payload = helper.run(data)
    assert sct_payload["correct"]
