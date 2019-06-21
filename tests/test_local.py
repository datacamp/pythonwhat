import pytest

from protowhat.Test import TestFail as TF
from pythonwhat.test_exercise import setup_state
from tests.helper import verify_sct


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
        * 2,
    ],
)
def test_urlretrieve_in_process(sol_code, stu_code):
    # on mac an env var needs to be set:
    # OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
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
        * 2,
    ],
)
def test_urlopen_in_process(sol_code, stu_code):
    chain = setup_state("", "", pec="")

    chain._state.solution_code = sol_code
    chain._state.student_code = stu_code

    with verify_sct(True):
        chain.run()
