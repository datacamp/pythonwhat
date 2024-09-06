from IPython.core.interactiveshell import InteractiveShell


class WasmProcess:
    def __init__(self):
        self.shell = InteractiveShell(user_ns={}, colors="NoColor")

    def run(self):
        print("Mock run - this doesn't do anything for the wasm program")

    def executeTask(self, task):
        result = task(self.shell)
        # print(f"Executed task, result {result}")
        return result

    def kill(self):
        self.reset()

    def reset(self):
        self.shell.reset()
