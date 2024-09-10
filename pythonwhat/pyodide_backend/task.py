from typing import Iterable, Optional

from contextlib import redirect_stdout, redirect_stderr

import io


def stdout_and_stderr_to_output(stdout: str, stderr: str, result: Optional[str]):
    output = []

    if stdout != "":
        if stdout.endswith("\n"):
            stdout = stdout[:-1]
        output.append({"type": "output", "payload": stdout})

    if stderr != "":
        if stderr.endswith("\n"):
            stderr = stderr[:-1]
        output.append({"type": "error", "payload": stderr})

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

        with redirect_stdout(stdout_stream), redirect_stderr(stderr_stream):
            for code in self.code_iterable:
                shell.run_cell(code, **self.kwargs)

        result = None
        if shell.displayhook.has_result():
            result = shell.displayhook.fetch_result()

        stdout = stdout_stream.getvalue()
        stderr = stderr_stream.getvalue()

        return stdout_and_stderr_to_output(stdout, stderr, result)


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
