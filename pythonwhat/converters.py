import inspect
import pythonwhat

def get_manual_converters():

    converters = {
        'pandas.io.excel.ExcelFile': lambda x: x.io,
        'dict_keys': lambda x: list(x)
    }

    return(converters)

