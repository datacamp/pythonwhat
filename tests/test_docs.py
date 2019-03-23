import pytest
import tests.helper as helper


@pytest.fixture
def data1():
    return {
        "DC_SOLUTION": 'x = 4\nif x > 0:\n    print("x is strictly positive")',
        "DC_SCT": """
Ex().check_if_else().multi(
    check_test().multi(
        set_env(x = -1).has_equal_value(), # chain A1
        set_env(x =  1).has_equal_value(), # chain A2
        set_env(x =  0).has_equal_value()  # chain A3
    ),
    check_body().check_function('print', 0).check_args('value').has_equal_value() # chain B
)
        """,
    }


def test_compound_statement_if_1(data1):
    data1["DC_CODE"] = data1["DC_SOLUTION"]
    output = helper.run(data1)
    assert output["correct"]


def test_compound_statement_if_2(data1):
    data1["DC_CODE"] = 'x = 4\nif 0 < x:\n    print("x is strictly positive")'
    output = helper.run(data1)
    assert output["correct"]


def test_compount_statement_if_fail(data1):
    data1["DC_CODE"] = 'x = 4\nif x >= 0:\n    print("x is strictly positive")'
    output = helper.run(data1)
    assert not output["correct"]


@pytest.fixture
def data2():
    return {
        "DC_SOLUTION": """    
my_dict = {'a': 1, 'b': 2}
for key, value in my_dict.items():
    print(key + " - " + str(value))
""",
        "DC_SCT": """
Ex().check_object('my_dict').has_equal_value()
Ex().check_for_loop().multi(
    check_iter().has_equal_value(),
    check_body().multi(
        set_context('a', 1).has_equal_output(),
        set_context('b', 2).has_equal_output()
    )
)
""",
    }


def test_compound_statement_for_1(data2):
    data2["DC_CODE"] = data2["DC_SOLUTION"]
    output = helper.run(data2)
    assert output["correct"]


def test_compound_statement_for_2(data2):
    data2[
        "DC_CODE"
    ] = "my_dict = {'a': 1, 'b': 2}\nfor k, v in my_dict.items():\n    print(k + ' - ' + str(v))"
    output = helper.run(data2)
    assert output["correct"]


def test_compount_statement_for_3(data2):
    data2[
        "DC_CODE"
    ] = "my_dict = {'a': 1, 'b': 2}\nfor first, second in my_dict.items():\n    mess = first + ' - ' + str(second)\n    print(mess)"
    output = helper.run(data2)
    assert output["correct"]


@pytest.fixture
def data3():
    return {
        "DC_SOLUTION": """
def shout_echo(word1, echo=1):
    echo_word = word1 * echo
    shout_words = echo_word + '!!!'
    return shout_words
        """,
        "DC_SCT": """
Ex().check_function_def('shout_echo').test_correct(
    multi(
        check_call("f('hey', 3)").has_equal_value(),
        check_call("f('hi', 2)").has_equal_value(),
        check_call("f('hi')").has_equal_value()
    ),
    check_body().set_context('test', 1).multi(
        has_equal_value(name = 'echo_word'),
        has_equal_value(name = 'shout_words')
    )
)
        """,
    }


def test_compound_statement_fun_def_1(data3):
    data3["DC_CODE"] = data3["DC_SOLUTION"]
    output = helper.run(data3)
    assert output["correct"]


def test_compound_statement_fun_def_2(data3):
    data3["DC_CODE"] = "def shout_echo(w, e=1):\n    ew = w * e\n    return ew + '!!!'"
    output = helper.run(data3)
    assert output["correct"]


def test_compound_statement_fun_def_3(data3):
    data3["DC_CODE"] = "def shout_echo(a, b=1):\n    return a * b + '!!!'"
    output = helper.run(data3)
    assert output["correct"]


@pytest.fixture
def data4():
    return {
        "DC_SOLUTION": """
def counter(lst, key):
    count = 0
    for l in lst:
        count += l[key]
    return count
        """,
        "DC_SCT": """
Ex().check_function_def('counter').test_correct(
    multi(
        check_call("f([{'a': 1}], 'a')").has_equal_value(),
        check_call("f([{'b': 1}, {'b': 2}], 'b')").has_equal_value()
    ),
    check_body().set_context([{'a': 1}, {'a': 2}], 'a').set_env(count = 0).check_for_loop().multi(
        check_iter().has_equal_value(),
        check_body().set_context({'a': 1}).has_equal_value(name = 'count')
    )
)
        """,
    }


def test_compound_statement_crazy_combo_1(data4):
    data4["DC_CODE"] = data4["DC_SOLUTION"]
    output = helper.run(data4)
    assert output["correct"]
