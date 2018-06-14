import pytest
import helper
from pythonwhat.local import setup_state


@pytest.mark.debug
def test_disable_highlighting():
    s = setup_state(stu_code = "round(1.234, 2)", sol_code = "round(2.345, 2)")
    assert s._state.highlighting_disabled is None
    assert s.disable_highlighting()._state.highlighting_disabled
    assert s.disable_highlighting().check_function('round')._state.highlighting_disabled
    assert s.check_function('round').disable_highlighting()._state.highlighting_disabled

@pytest.fixture
def data():
    return {
		'DC_CODE': 'round(1.234, 2)',
		'DC_SOLUTION': 'round(2.345, 2)',
	}

def test_with_highlighting(data):
    data['DC_SCT'] = 'Ex().check_function("round").check_args("number").has_equal_value()'
    output = helper.run(data)
    assert not output['correct']
    helper.with_line_info(output, 1, 1, 7, 11)

@pytest.mark.parametrize('sct', [
    'Ex().disable_highlighting().check_function("round").check_args("number").has_equal_value()',
    'Ex().check_function("round").disable_highlighting().check_args("number").has_equal_value()',
    'Ex().check_function("round").check_args("number").disable_highlighting().has_equal_value()'
])
def test_without_highlighting(data, sct):
    data['DC_SCT'] = sct
    output = helper.run(data)
    assert not output['correct']
    helper.no_line_info(output)

