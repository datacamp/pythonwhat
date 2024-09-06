class OutputManager(object):
    @classmethod
    def _addCodeOutput(cls, return_output, execution_output, script_name=None):
        # old code where each line was a different entry in json
        # lines = output_stream.split("\n")
        # if lines[-1] == "":
        #     lines.pop()
        # for line in lines:
        #     output.append({"type": "output", "payload": line})

        output_stream = execution_output["output_stream"]

        if output_stream != "":
            if output_stream.endswith("\n"):
                output_stream = output_stream[:-1]
            if script_name is not None:
                return_output.append(
                    {
                        "type": "script-output",
                        "payload": {
                            "output": output_stream,
                            "script_name": script_name,
                        },
                    }
                )
            else:
                return_output.append({"type": "output", "payload": output_stream})

        if execution_output["result"] is not None:
            return_output.append(
                {"type": "result", "payload": str(execution_output["result"])}
            )

        error_stream = execution_output["error_stream"]

        if error_stream != "":
            if error_stream.endswith("\n"):
                error_stream = error_stream[:-1]
            return_output.append({"type": "error", "payload": error_stream})

        if execution_output["error"] is not None:
            return_output.append(
                {"type": "error", "payload": execution_output["error"]}
            )

    @classmethod
    def _addSctOutput(cls, return_output, result):
        return_output.append({"type": "sct", "payload": result})

    @classmethod
    def addlockConsoleOutput(cls, return_output, result):
        return_output.append({"type": "lock-console", "payload": result})

    @classmethod
    def addunlockConsoleOutput(cls, return_output, result):
        return_output.append({"type": "unlock-console", "payload": result})

    @classmethod
    def _addSpecialOutput(cls, return_output):
        pass
        ##### GRAPHS #####
        # for figure in FiguresManager.getFigures():
        #     return_output.append(figure.getPayload())
        #
        # for plot in HtmlManager.getPlots():
        #     return_output.append(plot.getPayload())
        #
        # FiguresManager.clearFigures()
        # HtmlManager.clearPlots()

    @classmethod
    def enableSpecialOutput(cls):
        pass
        # FiguresManager.ENABLED = True
        # HtmlManager.ENABLED = True

    @classmethod
    def disableSpecialOutput(cls):
        pass
        # FiguresManager.ENABLED = False
        # HtmlManager.ENABLED = False

    @classmethod
    def resizeSpecialOutput(cls, height, width):
        pass
        # FiguresManager.setPlotSizes(height, width)

