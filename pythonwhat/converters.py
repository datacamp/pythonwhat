import inspect
import pythonwhat

def get_manual_converters():

    converters = {
        'pandas.io.excel.ExcelFile': lambda x: x.io,
        'dict_keys': lambda x: list(x),
        'bs4.BeautifulSoup': lambda x: str(x),
        'bs4.element.Tag': lambda x: str(x),
        'bs4.element.NavigableString': lambda x: str(x),
        'bs4.element.ResultSet': lambda x: str(x)
    }

    return(converters)

