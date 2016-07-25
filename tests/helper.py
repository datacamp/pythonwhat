from pythonbackend.Exercise import Exercise
from pythonbackend import utils

def get_sct_payload(output):
	output = [out for out in output if out['type'] == 'sct']
	if (len(output) > 0):
		return(output[0]['payload'])
	else:
		return(None)

def run(data):
    exercise = Exercise(data)
    exercise.runInit()
    output = exercise.runSubmit(data)
    return(get_sct_payload(output))

def test_lines(test, sct_payload, ls, le, cs, ce):
    test.assertEqual(sct_payload['line_start'], ls)
    test.assertEqual(sct_payload['line_end'], le)
    test.assertEqual(sct_payload['column_start'], cs)
    test.assertEqual(sct_payload['column_end'], ce)

def test_absent_lines(test, sct_payload):
    test.assertFalse('line_start' in sct_payload)
    test.assertFalse('line_end' in sct_payload)
    test.assertFalse('column_start' in sct_payload)
    test.assertFalse('column_end' in sct_payload)