import re

class Feedback(object):

    def __init__(self, message, astobj = None):
        self.message = message
        self.line_info = {}
        try:
            if astobj is not None and \
                hasattr(astobj, "first_token") and \
                hasattr(astobj, "last_token"):
                self.line_info["line_start"] = astobj.first_token.start[0]
                self.line_info["column_start"] = astobj.first_token.start[1]
                self.line_info["line_end"] = astobj.last_token.end[0]
                self.line_info["column_end"] = astobj.last_token.end[1]
        except:
            pass

