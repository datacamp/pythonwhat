from protowhat.Feedback import Feedback as ProtoFeedback


class Feedback(ProtoFeedback):
    def __init__(self, message, state=None):
        self.message = message
        self.highlight = None
        self.highlighting_disabled = False
        if state is not None:
            self.highlight = state.highlight
            self.highlighting_disabled = state.highlighting_disabled

    def get_line_info(self):
        try:
            if (
                self.highlight is not None
                and hasattr(self.highlight, "first_token")
                and hasattr(self.highlight, "last_token")
                and not self.highlighting_disabled
            ):
                return {
                    "line_start": self.highlight.first_token.start[0],
                    "column_start": self.highlight.first_token.start[1],
                    "line_end": self.highlight.last_token.end[0],
                    "column_end": self.highlight.last_token.end[1],
                }
            else:
                return {}
        except:
            return {}

    def get_formatted_line_info(self):
        formatted_info = self.get_line_info()
        for k in ["column_start"]:
            if k in formatted_info:
                formatted_info[k] += 1
        return formatted_info
