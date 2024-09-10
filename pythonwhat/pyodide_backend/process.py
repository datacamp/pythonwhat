from IPython.core.interactiveshell import InteractiveShell

from .display_hook import DisplayHook


class WasmProcess:
    def __init__(self):
        InteractiveShell.displayhook_class = DisplayHook
        self.shell = InteractiveShell(user_ns={}, colors="NoColor")

    def run(self):
        pass

    def executeTask(self, task):
        return task(self.shell)

    def kill(self):
        self.reset()

    def reset(self):
        self.shell.reset()
