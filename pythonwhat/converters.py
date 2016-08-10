import inspect
import pythonwhat

def get_manual_converters():

    converters = {
        'pandas.io.excel.ExcelFile': lambda x: x.io
    }

    return(converters)

