from IPython.core.displayhook import DisplayHook as IPythonDisplayHook


class DisplayHook(IPythonDisplayHook):
    def __init__(self, parent, shell, cache_size):
        super(DisplayHook, self).__init__(
            parent=parent, shell=shell, cache_size=cache_size
        )
        self.result = []

    def write_output_prompt(self):
        pass

    def write_format_data(self, format_dict, md_dict=None):
        if "text/plain" not in format_dict:
            return
        result_repr = format_dict["text/plain"]
        if "\n" in result_repr:
            result_repr = "\n" + result_repr

        self.result.append(result_repr)

    def finish_displayhook(self):
        pass

    def has_result(self):
        return len(self.result) > 0

    def fetch_result(self):
        return self.result.pop()
