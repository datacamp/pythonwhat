import pytest
from pythonwhat.local import WorkerProcess


@pytest.fixture(scope="function", autouse=True)
def kill_processes():
    yield
    WorkerProcess.kill_all()
