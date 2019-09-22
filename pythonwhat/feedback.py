from typing import Dict

from protowhat.Feedback import Feedback as ProtoFeedback


class Feedback(ProtoFeedback):
    ast_highlight_offset = {"column_start": 1}

    @classmethod
    def get_highlight_position(cls, highlight) -> Dict[str, int]:
        if getattr(highlight, "first_token", None) and getattr(
            highlight, "last_token", None
        ):
            return {
                "line_start": highlight.first_token.start[0],
                "column_start": highlight.first_token.start[1],
                "line_end": highlight.last_token.end[0],
                "column_end": highlight.last_token.end[1],
            }
