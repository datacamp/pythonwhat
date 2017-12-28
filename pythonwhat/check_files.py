from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.utils import get_ord

from pathlib import Path
from collections.abc import Mapping

def check_file(fname, 
               msg = "",
               msg_is_dir = "",
               parse = True,
               use_fs = False,
               use_solution = True,
               state = None
               ):
    """Test whether file exists, and make its contents the student code.
    
    Note: this SCT fails if the file is a directory.
    """

    # TODO can only occur on root state
    # TODO message with fname
    # TODO what happens on parse failures?

    rep = Reporter.active_reporter

    if use_fs:
        p = Path(fname)
        if not p.exists(): rep.do_test(msg.format(fname))          # test file exists
        if     p.is_dir(): rep.do_test(msg_is_dir.format(fname))   # test its not a dir

        code = p.read_text()
    else:
        code = _get_fname(state, 'student_code', fname)

        if code is None: rep.do_test(msg.format(fname))           # test file exists

    sol_kwargs = {'solution_code': None, 'solution_tree': None}
    if use_solution:
        sol_code = _get_fname(state, 'solution_code', fname)
        if sol_code is None: raise Exception("Solution code does not have file named: %s" % fname)
        sol_kwargs['solution_code'] = sol_code
        sol_kwargs['solution_tree'] = state.parse_int(sol_code) if parse else None

    return State(student_code = code,
                 full_student_code = code,
                 pre_exercise_code = state.pre_exercise_code,
                 student_process = state.student_process,
                 solution_process = state.solution_process,
                 raw_student_output = state.raw_student_output,
                 student_tree  = state.parse_ext(code) if parse else None,
                 **sol_kwargs
                 )

def _get_fname(state, attr, fname):
    code_dict = getattr(state, attr)
    if not isinstance(code_dict, Mapping):
        raise TypeError("Can't get {} from state.{}, which must be a "
                        "dictionary or Mapping.")

    return code_dict.get(fname)


def test_dir(fname, msg = "Did you create a directory named `{}`?", state = None):
    """Test whether a directory exists."""

    rep = Reporter.active_reporter

    if not Path(fname).is_dir():
        rep.do_test(msg.format(fname))

    return state

