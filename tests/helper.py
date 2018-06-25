import re
import os

from pythonwhat.local import StubProcess
from contextlib import redirect_stdout
from pythonwhat.test_exercise import test_exercise
import io
import tempfile

def run(data, run_code = True):

    pec = data.get("DC_PEC", "")
    stu_code = data.get("DC_CODE", "")
    sol_code = data.get("DC_SOLUTION", "")
    sct = data.get("DC_SCT", "")

    class ChDir(object):
        """
        Step into a directory temporarily.
        """
        def __init__(self, path):
            self.old_dir = os.getcwd()
            self.new_dir = path

        def __enter__(self):
            os.chdir(self.new_dir)

        def __exit__(self, *args):
            os.chdir(self.old_dir)

    with tempfile.TemporaryDirectory() as d:
        with ChDir(d):
            if run_code :
                stu_output = io.StringIO()
                stu_process = StubProcess(init_code = pec)
                try:
                    with redirect_stdout(stu_output):
                        stu_process.shell.run_code(stu_code)
                    raw_stu_output = stu_output.getvalue()
                    error = None
                except Exception as e:
                    raw_stu_output = ""
                    error = str(e)
                sol_output = io.StringIO()
                with redirect_stdout(sol_output):
                    sol_process = StubProcess(init_code =  "%s\n%s" % (pec, sol_code))
            else :
                raw_stu_output = ""
                stu_process = StubProcess()
                sol_process = StubProcess()
                error = None

            sct_output = io.StringIO()
            with redirect_stdout(sct_output):
                res = test_exercise(sct=sct,
                                    student_code=stu_code,
                                    solution_code=sol_code,
                                    pre_exercise_code=pec,
                                    student_process=stu_process,
                                    solution_process=sol_process,
                                    raw_student_output = raw_stu_output,
                                    ex_type = "NormalExercise",
                                    error = error)

    return res


def get_sct_payload(output):
    sct_output = [out for out in output if out['type'] == 'sct']
    if (len(sct_output) > 0):
        return(sct_output[0]['payload'])
    else:
        print(output)
        return(None)

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

def with_line_info(output, ls, le, cs, ce):
    assert output['line_start'] == ls
    assert output['line_end'] == le
    assert output['column_start'] == cs
    assert output['column_end'] == ce

def no_line_info(output):
    assert 'line_start' not in output
    assert 'line_end' not in output
    assert 'column_start' not in output
    assert 'column_end' not in output

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
