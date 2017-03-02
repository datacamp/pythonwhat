from pythonbackend.Exercise import Exercise
from pythonbackend import utils
import re

def get_sct_payload(output):
    sct_output = [out for out in output if out['type'] == 'sct']
    if (len(sct_output) > 0):
        return(sct_output[0]['payload'])
    else:
        print(output)
        return(None)

def run(data):
    exercise = Exercise(data)
    output = exercise.runInit()
    if 'backend-error' in str(output):
        print(output)
        raise(ValueError("Backend error"))
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

def test_builtin(test, name, params, arguments):
    test.data = {
        "DC_PEC": "",
        "DC_SOLUTION": "%s(%s)" % (name, arguments),
        "DC_CODE": "%s(%s)" % (name, arguments),
        "DC_SCT": "test_function_v2('%s', params=[%s])" % (name, params)
    }
    sct_payload = run(test.data)
    test.assertTrue(sct_payload['correct'])

def remove_lambdas(sct_str, count=0, with_args = False): 
    if with_args: return re.sub("lambda.*?:", "", sct_str, count=count)
    else: return re.sub("lambda:", "", sct_str, count=count)

def replace_test_if(sct):
    return re.sub(r"test_if_else\(", "test_if_exp(", sct)
