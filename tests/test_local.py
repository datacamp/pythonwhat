import os
from pathlib import Path

import pytest

from pythonwhat.local import ChDir
from pythonwhat.test_exercise import setup_state
from tests.helper import verify_sct, in_temp_dir

modify_sys = (
    """
import sys
sys.modules["foo"] = "bar"
""",
    """
import sys
bar = sys.modules.get("foo")
    """,
)

asset = "https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/L-L1_LOSC_4_V1-1126259446-32.hdf5"


@pytest.mark.parametrize("sol_code, stu_code", [modify_sys])
def test_running_code_isolation_stub(sol_code, stu_code):
    chain = setup_state(stu_code, sol_code, pec="", mode="stub")

    chain.has_equal_value(name="bar", override="bar")

    # clean up
    import sys

    del sys.modules["foo"]


@pytest.mark.parametrize("sol_code, stu_code", [modify_sys])
def test_running_code_isolation_run(sol_code, stu_code):
    # test that setup_state is isolated
    chain = setup_state(sol_code, stu_code, pec="")
    chain._state.solution_code = sol_code
    chain._state.student_code = stu_code

    with verify_sct(False):
        # test that run is isolated
        chain.run().has_equal_value(name="bar", override="bar")


@pytest.mark.parametrize(
    "sol_code, stu_code",
    [
        (
            """from urllib.request import urlretrieve;
urlretrieve('{}', 'LIGO_data.hdf5')""".format(
                asset
            ),
        )
        * 2
    ],
)
def test_urlretrieve_in_process(sol_code, stu_code):
    # on mac an env var needs to be set:
    # OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
    with in_temp_dir():
        chain = setup_state("", "", pec="")

        chain._state.solution_code = sol_code
        chain._state.student_code = stu_code

        with verify_sct(True):
            chain.run()


@pytest.mark.parametrize(
    "sol_code, stu_code",
    [
        (
            """import urllib.request; import shutil
with urllib.request.urlopen({}) as response, open('LIGO_data.hdf5', 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
        """.format(
                asset
            ),
        )
        * 2
    ],
)
def test_urlopen_in_process(sol_code, stu_code):
    with in_temp_dir():
        chain = setup_state("", "", pec="")

        chain._state.solution_code = sol_code
        chain._state.student_code = stu_code

        with verify_sct(True):
            chain.run()


def write_file(path, name, content):
    os.makedirs(path)
    with ChDir(path):
        with open(name, "w") as f:
            f.write(content)


def test_run_relative_working_dir():
    stu_code = 'from pathlib import Path; c = Path("c").read_text(encoding="utf-8")'
    sol_code = """c = 'c= Path("c").read_text(encoding="utf-8")'"""

    file_dir = "a/b"
    file_path = "a/b/c"

    with in_temp_dir():

        write_file(file_dir, "c", stu_code)

        chain = setup_state("", "", pec="")

        child = chain.check_file(file_path, solution_code=sol_code)

        child.run(file_dir).check_object("c")
        child.run().check_object("c")


def test_run_solution_dir():
    code = 'from pathlib import Path; c = Path("c").read_text(encoding="utf-8")'

    file_dir = "a/b"
    file_path = "a/b/c"
    workspace_location = "workspace"

    with in_temp_dir():
        write_file("solution/" + file_dir, "c", code)

        os.makedirs(workspace_location)
        with ChDir(workspace_location):
            write_file(file_dir, "c", code)

            chain = setup_state("", "", pec="")

            child = chain.check_file(file_path, solution_code=code)

            child.run(file_dir).check_object("c")
            child.run().check_object("c")


def test_run_with_absolute_dir():
    code = 'from pathlib import Path; c = Path("c").read_text(encoding="utf-8")'

    file_dir = "a/b"
    solution_location = "solution"
    workspace_location = "workspace"

    with in_temp_dir():
        os.makedirs(file_dir)
        with ChDir(file_dir):
            abs_dir = os.path.abspath(".")
            abs_file_path = Path(abs_dir, "c")
            with open("c", "w") as f:
                f.write(code)

        write_file(solution_location, "c", code)

        os.makedirs(workspace_location)
        with ChDir(workspace_location):
            chain = setup_state("", "", pec="")

            child = chain.check_file(abs_file_path, solution_code=code)

            child.run(abs_dir).check_object("c")
            child.run().check_object("c")


def test_run_custom_solution_dir():
    code = 'from pathlib import Path; c = Path("c").read_text(encoding="utf-8")'

    file_dir = "a/b"
    file_path = "a/b/c"
    custom_solution_location = "custom/solution/folder"

    with in_temp_dir():
        write_file(file_dir, "c", code)

        os.makedirs(custom_solution_location)
        with ChDir(custom_solution_location):
            write_file(file_dir, "c", code)

        chain = setup_state("", "", pec="")

        child = chain.check_file(file_path, solution_code=code)

        child.run(file_dir, solution_dir=custom_solution_location).check_object("c")
        child.run(solution_dir=custom_solution_location).check_object("c")
