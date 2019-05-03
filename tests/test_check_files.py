from tempfile import NamedTemporaryFile

import pytest
import tests.helper as helper
from protowhat.sct_syntax import F

from pythonwhat.local import setup_state
from protowhat.checks import check_files as cf


@pytest.fixture(scope="function")
def tf():
    with NamedTemporaryFile() as tmp:
        tmp.file.write(b"1 + 1")
        tmp.file.flush()
        yield tmp


def test_file_existence(tf):
    s = setup_state("", "", pec="")

    child = cf.check_file(s._state, tf.name)
    assert "1 + 1" in child.student_code

    file_chain = s.check_file(tf.name)
    assert "1 + 1" in file_chain._state.student_code

    with helper.verify_sct(True):
        s >> F(attr_scts={"check_file": cf.check_file}).check_file(tf.name)
