__version__ = "2.24.4"

from .test_exercise import test_exercise, allow_errors
from .process import WasmProcess
from .tasks import TaskCaptureStdoutAndStdin, TaskNoOutput
