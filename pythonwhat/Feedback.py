from protowhat.Feedback import Feedback as ProtoFeedback


class Feedback(ProtoFeedback):
    def _highlight_data(self):
        if hasattr(self.highlight, "first_token") and hasattr(
            self.highlight, "last_token"
        ):
            return {
                "line_start": self.highlight.first_token.start[0],
                "column_start": self.highlight.first_token.start[1],
                "line_end": self.highlight.last_token.end[0],
                "column_end": self.highlight.last_token.end[1],
            }
