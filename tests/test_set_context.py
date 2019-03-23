import pytest
import tests.helper as helper


@pytest.mark.parametrize("spec", ["'test', 1", "word1 = 'test', echo = 1"])
def test_check_function_def(spec):
    code = """
def shout_echo(word1, echo=1):
    echo_word = word1 * echo
    shout_words = echo_word + '!!!'
    return shout_words
"""
    data = {
        "DC_CODE": code,
        "DC_SOLUTION": code,
        "DC_SCT": "Ex().check_function_def('shout_echo').check_body().set_context(%s).has_equal_value(name = 'shout_words')"
        % spec,
    }
    output = helper.run(data)
    assert output["correct"]


def test_check_function_def_2():
    code = """
def shout_echo(word1, echo=1):
    echo_word = word1 * echo
    shout_words = echo_word + '!!!'
    return shout_words
"""
    data = {
        "DC_CODE": code,
        "DC_SOLUTION": code.replace("word1", "w"),
        "DC_SCT": "Ex().check_function_def('shout_echo').check_body().set_context('test', 1).has_equal_value(name = 'shout_words')",
    }
    output = helper.run(data)
    assert output["correct"]


@pytest.mark.parametrize("spec", ["'a'", "m = 'a'"])
def test_check_dict_comp(spec):
    code = "x = { m:len(m) for m in ['a', 'b', 'c'] }"
    data = {
        "DC_CODE": code,
        "DC_SOLUTION": code,
        "DC_SCT": "Ex().check_dict_comp().check_key().set_context(%s).has_equal_value()"
        % spec,
    }
    output = helper.run(data)
    assert output["correct"]


def test_check_dict_comp_2():
    data = {
        "DC_CODE": "x = { m:len(m) for m in ['a', 'b', 'c'] }",
        "DC_SOLUTION": "x = { n:len(n) for n in ['a', 'b', 'c'] }",
        "DC_SCT": "Ex().check_dict_comp().check_key().set_context('a').has_equal_value()",
    }
    output = helper.run(data)
    assert output["correct"]


def test_fail():
    data = {
        "DC_CODE": "x = { m:len(m) for m in ['a', 'b', 'c'] }",
        "DC_SOLUTION": "x = { m*2:len(m) for m in ['a', 'b', 'c'] }",
        "DC_SCT": "Ex().check_dict_comp().check_key().set_context('a').has_equal_value()",
    }
    output = helper.run(data)
    assert not output["correct"]
