from .process import WasmProcess
from .task import TaskNoOutput, TaskCaptureCodeExecutionOutput


class PyodideExercise:
    def __init__(self, pec: str, solution: str, sct: str):
        self.pec = pec
        self.solution = solution
        self.sct = sct

        self.user_process = None
        self.submit_process = None
        self.solution_process = None

    def run_init(self):
        self.user_process = WasmProcess()
        self.submit_process = WasmProcess()
        self.solution_process = WasmProcess()

        result = self.user_process.executeTask(
            TaskCaptureCodeExecutionOutput([self.pec])
        )
        self.submit_process.executeTask(TaskNoOutput([self.pec]))
        self.solution_process.executeTask(TaskNoOutput([self.pec, self.solution]))

        return result

    def run_code(self, code: str):
        return self.user_process.executeTask(TaskCaptureCodeExecutionOutput([code]))
