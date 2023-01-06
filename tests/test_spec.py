import pytest
import tests.helper as helper
from protowhat.failure import InstructorError


@pytest.mark.parametrize(
    "sct",
    [
        """
list_comp = F().check_list_comp(0).check_body().set_context(ii=2).has_equal_value('unequal')
Ex().check_list_comp(0).check_body().set_context(aa=2).multi(list_comp)
""",
        """
list_comp = check_list_comp(0).check_body().set_context(ii=2).has_equal_value('unequal')
Ex().check_list_comp(0).check_body().set_context(aa=2).multi(list_comp)
""",
        """
# funky, but we're testing nested check functions!
multi_test = multi(check_list_comp(0).check_body().set_context(aa=2).has_equal_value('badbody'))
Ex().multi(multi_test)
""",
        """
list_comp = F().check_list_comp(0).check_body().set_context(ii=2).has_equal_value('unequal')
Ex().check_list_comp(0).check_body().set_context(aa=2).multi(list_comp)
Ex().check_list_comp(1).check_body().set_context(bb=4).multi(list_comp)
""",
        """
eq_test = F().check_list_comp(0).check_body().set_context(1).has_equal_value
Ex().multi(eq_test('unequal'))
""",
    ],
)
def test_f_chain(sct):
    code = "[[ii+1 for ii in range(aa)] for aa in range(2)]\n[[ii*2 for ii in range(bb)] for bb in range(1,3)]"
    res = helper.run({"DC_SOLUTION": code, "DC_CODE": code, "DC_SCT": sct})
    assert res["correct"]


@pytest.mark.parametrize(
    "stu, sct, passes, patt",
    [
        (
            None,
            """
te = test_expression_result(extra_env={'aa':2}, incorrect_msg='unequal')
Ex().multi(test_list_comp(body=te))                                                        # spec 1 inside multi
Ex().check_list_comp(0).check_body().multi(te)                                             # half of each spec
Ex().check_list_comp(0).check_body().set_context(aa=2).has_equal_value('unequal')          # full spec 2
test_list_comp(body=te)                                                                    # full spec 1
""",
            True,
            None,
        ),
        # TODO: this test fails because spec1 tests are run after spec2 tests,
        #       even if they come first in the SCT script, due to building the tree
        #       for spec1 tests but not spec2 (which are run immediately)
        (
            "for aa in range(3): aa",
            """
test_list_comp(body=test_expression_result(expr_code = 'aa', incorrect_msg='unequal'))
Ex().check_list_comp(0).check_body().multi(test_expression_result(incorrect_msg='unequal'))
Ex().check_list_comp(0).check_body().has_equal_value('unequal')
    """,
            False,
            None,
        ),
        (
            "[aa for aa in range(2)]",
            """
Ex().test_list_comp(body=test_expression_result(extra_env={'aa': 2}, incorrect_msg = 'spec1'))
Ex().check_list_comp(0).check_body().set_context(aa=2).has_equal_value('spec2')
    """,
            False,
            "spec1",
        ),
    ],
)
def test_spec_interoperability(stu, sct, passes, patt):
    code = "[aa+1 for aa in range(2)]"
    res = helper.run({"DC_SOLUTION": code, "DC_CODE": stu or code, "DC_SCT": sct})
    assert res["correct"] == passes
    if patt:
        assert patt in res["message"]


@pytest.mark.parametrize(
    "sct",
    [
        """
test_body = F().check_body().set_context(aa=2).has_equal_value('wrong')
Ex().check_list_comp(0).multi(F().multi(test_body))
    """,
        """
test_body = F().check_list_comp(0).check_body().set_context(aa=2).has_equal_value('wrong')
Ex().check_list_comp(0).multi(F().check_body().set_context(aa=2).has_equal_value('wrong'))
    """,
        """
Ex().check_list_comp(0).check_body()\
        .multi(set_context(aa=i).has_equal_value('wrong') for i in range(2))
    """,
    ],
)
def test_multi(sct):
    code = "[aa+1 for aa in range(2)]"
    res = helper.run({"DC_SOLUTION": code, "DC_CODE": code, "DC_SCT": sct})
    assert res["correct"]


def test_fail():
    res = helper.run({"DC_SOLUTION": "", "DC_SCT": "Ex().fail()"})
    assert not res["correct"]


@pytest.fixture
def data():
    return {
        "DC_SOLUTION": """dict(a = "a").keys()""",
        "DC_CODE": """dict(a = 'a')    .keys()""",
    }


def failing_submission(data):
    data["DC_CODE"] = "dict(A = 'a').keys(somearg = 2)" ""
    sct_payload = helper.run(data, run_code=False)
    assert not sct_payload["correct"]


def test_has_equal_ast_code_without_msg(data):
    data["DC_SCT"] = "Ex().has_equal_ast(code = 'test')"
    with pytest.raises(InstructorError):
        helper.run(data)


def test_has_equal_ast_simple_pass(data):
    data["DC_SCT"] = "Ex().has_equal_ast()"
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


def test_has_equal_ast_formatting(data):
    data["DC_CODE"] = """
def car_wash(env):
    car_wash_num = 0
    while True:
        car_wash_num += 2
        
        # Get the current simulation time and clock-in the process time
        yield env.timeout(5)

a = 2
b = 3
"""
    data["DC_SOLUTION"] = """
def car_wash(env):
    car_wash_num = 0
    while True:
        car_wash_num += 1
        
        # Get the current simulation time and clock-in the process time
        yield env.timeout(5)

a = 2
b = 3
"""
    data["DC_SCT"] = """
Ex().check_function_def("car_wash").multi(
    check_body().check_while().has_equal_ast()
)
"""
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    incorrect_msg = """Did you correctly specify the body? Check the first <code>while</code> loop. Expected 

<pre><code>while True:
    car_wash_num += 1

    # Get the current simulation time and clock-in the process time
    yield env.timeout(5)
</code></pre>

, but got 

<pre><code>while True:
    car_wash_num += 2

    # Get the current simulation time and clock-in the process time
    yield env.timeout(5)
</code></pre>"""
    assert sct_payload["message"] == incorrect_msg


def test_black_formatting_errors_catch(data):
    data["DC_CODE"] = """
# Define a function called plot_timeseries
def plot_timeseries(axes, x, y, color, xlabel, ylabel):

  # Plot the inputs x,y in the provided color
  axes.plot(x, y, color=color)

  # Set the x-axis label
  axes.set_xlabel(xlabel)

  # Set the y-axis label
  axes.set_ylabel(ylabel, color=color)

  # Set the colors tick params for y-axis
  axes.tick_params('y', colors=color)
"""
    data["DC_SOLUTION"] = """
# Define a function called plot_timeseries
def plot_timeseries(axes, x, y, color, xlabel, ylabel):

  # Plot the inputs x,y in the provided color
  axes.plot(x, y, color=color)

  # Set the x-axis label
  axes.set_xlabel(xlabel)

  # Set the y-axis label
  axes.set_ylabel(ylabel, color=color)

  # Set the colors tick params for y-axis
  axes.tick_params('y', colors=color)
"""
    data["DC_SCT"] = """
msg1 = "Did you plot the x and y in the provided color?"
msg2 = "Did you set the x-axis label?"
msg3 = "Did you set the y-axis label?"
msg4 = "Did you set the colors tick params for y-axis?"

Ex().check_function_def("plot_timeseries").check_body().multi(
    check_or(
        has_equal_ast(msg1, "axes.plot(x, y, color=color)", exact = False), 
        has_equal_ast(msg1, "axes.plot(x, y, c=color)", exact = False)
    ), 
    check_or(
        has_equal_ast(msg2, "axes.set_xlabel(xlabel)", exact = False), 
        has_equal_ast(msg2, "axes.set_xlabel(xlabel=xlabel)", exact = False)
    ), 
    check_or(
        has_equal_ast(msg3, "axes.set_ylabel(ylabel, color=color)", exact = False),
        has_equal_ast(msg3, "axes.set_ylabel(ylabel, c=color)", exact = False),
        has_equal_ast(msg3, "axes.set_ylabel(ylabel=ylabel, color=color)", exact = False), 
        has_equal_ast(msg3, "axes.set_ylabel(ylabel=ylabel, c=color)", exact = False)
    ), 
    has_equal_ast(msg4, "axes.tick_params('y', colors=color)", exact = False),
)

success_msg("Very good. Next, let's use this function!")
"""
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


def test_has_equal_ast_simple_fail(data):
    data["DC_SCT"] = "Ex().has_equal_ast()"
    failing_submission(data)


def test_has_equal_ast_function_pass(data):
    data["DC_SCT"] = "Ex().check_function('dict', 0, signature=False).has_equal_ast()"
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


def test_has_equal_ast_function_fail(data):
    data["DC_SCT"] = "Ex().check_function('dict', 0, signature=False).has_equal_ast()"
    failing_submission(data)


def test_has_equal_ast_function_code_pass(data):
    data[
        "DC_SCT"
    ] = """Ex().has_equal_ast(code = 'dict(a = "a").keys()', incorrect_msg = 'icr')"""
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


def test_has_equal_ast_function_code_fail(data):
    data[
        "DC_SCT"
    ] = """Ex().has_equal_ast(code = 'dict(a = "a").keys()', incorrect_msg = 'icr')"""
    failing_submission(data)


def test_has_equal_ast_exact_false_pass(data):
    data["DC_CODE"] = """dict(a = 'a').keys()\nprint('extra')"""
    data["DC_SCT"] = "Ex().has_equal_ast(exact=False)"
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


def test_has_equal_ast_exact_false_fail(data):
    data["DC_SCT"] = "Ex().has_equal_ast(exact=False)"
    failing_submission(data)


def test_has_equal_ast_part_of_method_pass(data):
    data[
        "DC_SCT"
    ] = """Ex().has_equal_ast(code = 'dict(a = "a")', exact=False, incorrect_msg = 'icr')"""
    sct_payload = helper.run(data)
    assert sct_payload["correct"]


def test_has_equal_ast_part_of_method_fail(data):
    data[
        "DC_SCT"
    ] = """Ex().has_equal_ast(code = 'dict(a = "a")', exact=False, incorrect_msg = 'icr')"""
    failing_submission(data)


# Test overriding fucntionality -----------------------------------------------


def do_override_test(
    code, base_check, parts, override=None, part_name=None, part_index="", passes=True
):
    """High level function used to generate tests"""
    if part_name:
        if not override:
            override = parts[part_name]
        sct = base_check + '.check_{}({}).override("""{}""").has_equal_ast()'.format(
            part_name, part_index, override
        )
    else:
        # whole code (e.g. if expression, or for loop)
        if not override:
            override = code.format(**parts)
        sct = base_check + '.override("""{}""").has_equal_ast()'.format(override)

    data = {
        "DC_SOLUTION": code.format(**parts),
        "DC_CODE": code.format(**parts),
        "DC_SCT": sct,
    }
    # import pdb; pdb.set_trace()
    sct_payload = helper.run(data)
    assert sct_payload["correct"] == passes


PARTS = {
    "body": "1",
    "test": "False",
    "orelse": "2",
    "iter": "range(3)",
    "key": "3",
    "value": "4",
    "args": "(1,2,3)",
}

import re


@pytest.mark.parametrize(
    "k, code",
    [
        ("if_exp", "{body} if {test} else {orelse}"),
        ("list_comp", "[{body} for i in {iter}]"),
        ("dict_comp", "{{ {key}: {value}  for i in {iter} }}"),
        ("for_loop", "for i in {iter}: {body}"),
        ("while", "while {test}: {body}"),
        ("try_except", "try: {body}\nexcept: pass\nelse: {orelse}"),
        ("lambda_function", "lambda a={args}: {body}"),
        ("function_def", ["'sum'", "def sum(a={args}): {body}"]),
        ("function", ["'sum', 0", "sum({args})"]),
    ],
)
def test_override(k, code):
    # base SCT, w/ special indexing if function checks
    if isinstance(code, list):
        indx, code = code
    else:
        indx = "0"

    base_check = "Ex().check_{}({})".format(k, indx)

    # pass overall test ----
    do_override_test(code, base_check, PARTS)

    # fail overall test ----
    do_override_test(code, base_check, PARTS, override="'WRONG ANSWER'", passes=False)

    # test individual pieces --------------------------------------------------
    # find all str.format vars, e.g. {body}
    for part in re.findall("{([^{]*?)}", code):
        part_index = "" if part != "args" else 0

        # pass individual piece ----
        do_override_test(code, base_check, PARTS, part_name=part, part_index=part_index)

        # fail individual piece ----
        bad_code = code.format(**{part: "[]", **PARTS})
        do_override_test(
            code,
            base_check,
            PARTS,
            part_name=part,
            part_index=part_index,
            override=bad_code,
            passes=False,
        )


# Test SCT Ex syntax (copied from sqlwhat)  -----------------------------------

from protowhat.sct_syntax import ChainExtender, ChainedCall, LazyChain
from pythonwhat.sct_syntax import Ex, EagerChain, state_dec


@pytest.fixture
def addx():
    return lambda state, x: state + x


@pytest.fixture
def f():
    return LazyChain(ChainedCall(lambda state, b: state + b, kwargs={"b": "b"}))


@pytest.fixture
def f2():
    return LazyChain(ChainedCall(lambda state, c: state + c, kwargs={"c": "c"}))


def test_f_from_func(f):
    assert f("a") == "ab"


def test_f_sct_copy_kw(addx):
    assert LazyChain(ChainedCall(addx, kwargs={"x": "x"}))("state") == "statex"


def test_f_sct_copy_pos(addx):
    assert LazyChain(ChainedCall(addx, ("x",)))("state") == "statex"


def test_ex_sct_copy_kw(addx):
    assert (
        EagerChain(ChainedCall(addx, kwargs={"x": "x"}), state="state")._state
        == "statex"
    )


def test_ex_sct_copy_pos(addx):
    assert EagerChain(ChainedCall(addx, ("x",)), state="state")._state == "statex"


def test_f_2_funcs(f, addx):
    g = ChainExtender(f, addx)

    assert g(x="x")("a") == "abx"


def test_f_add_unary_func(f):
    g = f >> (lambda state: state + "c")
    assert g("a") == "abc"


def test_f_add_f(f, f2):
    g = f >> f2
    assert g("a") == "abc"


def test_f_from_state_dec(addx):
    dec_addx = state_dec(addx)
    f = dec_addx(x="x")
    isinstance(f, LazyChain)
    assert f("state") == "statex"


@pytest.fixture
def ex():
    return ChainExtender(Ex("state"), lambda state, x: state + x)("x")


def test_ex_add_f(ex, f):
    assert (ex >> f)._state == "statexb"


def test_ex_add_f_add_f(ex, f, f2):
    assert (ex >> (f >> f2))._state == "statexbc"


def test_ex_add_unary(ex):
    assert (ex >> (lambda state: state + "b"))._state == "statexb"


def test_ex_add_ex_err(ex):
    with pytest.raises(BaseException):
        ex >> ex


def test_f_add_ex_err(f, ex):
    with pytest.raises(BaseException):
        f >> ex
