from protowhat.Feedback import Feedback as ProtoFeedback


class Feedback(ProtoFeedback):
    def _line_info(self):
        if hasattr(self.highlight, "first_token") and hasattr(
            self.highlight, "last_token"
        ):
            return {
                "line_start": self.highlight.first_token.start[0],
                "column_start": self.highlight.first_token.start[1],
                "line_end": self.highlight.last_token.end[0],
                "column_end": self.highlight.last_token.end[1],
            }

    def get_formatted_line_info(self):
        formatted_info = self.get_line_info()
        for k in ["column_start"]:
            if k in formatted_info:
                formatted_info[k] += 1
        return formatted_info
