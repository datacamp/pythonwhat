import inspect
import pythonwhat

def get_manual_converters():

    converters = {
        'pandas.io.excel.ExcelFile': lambda x: x.io,
        'builtins.dict_keys': lambda x: sorted(x),
        'builtins.dict_items': lambda x: sorted(x),
        'bs4.BeautifulSoup': lambda x: str(x),
        'bs4.element.Tag': lambda x: str(x),
        'bs4.element.NavigableString': lambda x: str(x),
        'bs4.element.ResultSet': lambda x: [str(res) for res in x],
        'h5py._hl.files.File': lambda x: x.file.filename,
        'h5py._hl.group.Group': lambda x: x.file.filename + '_' + str([x for x in x.keys()]),
        'sqlalchemy.engine.base.Engine': lambda x: x.url.database
    }

    return(converters)
