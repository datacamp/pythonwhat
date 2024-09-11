from typing import Iterable, Optional

from contextlib import redirect_stdout, redirect_stderr, contextmanager
from traceback import format_exception_only

import io


def stdout_and_stderr_to_output(stdout: str, stderr: str, result: Optional[str], exception: Optional[Exception]):
    output = []

    if stdout != "":
        if stdout.endswith("\n"):
            stdout = stdout[:-1]
        output.append({"type": "output", "payload": stdout})

    if stderr != "":
        if stderr.endswith("\n"):
            stderr = stderr[:-1]
        output.append({"type": "error", "payload": stderr})

    if exception is not None:
        exception_lines = format_exception_only(type(exception), exception)
        payload = "".join(exception_lines)
        output.append({ "type": "error", "payload": payload})

    if result is not None:
        output.append({"type": "result", "payload": result})

    return output


class TaskCaptureCodeExecutionOutput:
    def __init__(self, code_iterable, **kwargs):
        self.code_iterable = code_iterable
        self.kwargs = kwargs

    def __call__(self, shell):
        stdout_stream = io.StringIO()
        stderr_stream = io.StringIO()

        exception = None

        with redirect_stdout(stdout_stream), redirect_stderr(stderr_stream):
            for code in self.code_iterable:
                run_cell_result = shell.run_cell(code, **self.kwargs)
                if run_cell_result.error_in_exec is not None:
                    exception = run_cell_result.error_in_exec

        result = None
        if shell.displayhook.has_result():
            result = shell.displayhook.fetch_result()

        stdout = stdout_stream.getvalue()
        stderr = stderr_stream.getvalue()

        return stdout_and_stderr_to_output(stdout, stderr, result, exception)


class TaskNoOutput:
    def __init__(self, code_iterable: Iterable[str], **kwargs):
        self.code_iterable = code_iterable
        self.kwargs = kwargs

    def __call__(self, shell):
        stdout_output = io.StringIO()
        stderr_output = io.StringIO()

        with redirect_stdout(stdout_output), redirect_stderr(stderr_output):
            for code in self.code_iterable:
                shell.run_cell(code, **self.kwargs)
