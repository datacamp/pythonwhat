import re

class Feedback(object):

    def __init__(self, message, state = None):
        self.message = message
        self.line_info = {}
        try:
            if state is not None and hasattr(state.highlight, "first_token") and \
                    hasattr(state.highlight, "last_token") and not state.highlighting_disabled:
                self.line_info["line_start"] = state.highlight.first_token.start[0]
                self.line_info["column_start"] = state.highlight.first_token.start[1]
                self.line_info["line_end"] = state.highlight.last_token.end[0]
                self.line_info["column_end"] = state.highlight.last_token.end[1]

        except:
            pass

