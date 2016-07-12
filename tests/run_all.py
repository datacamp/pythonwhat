import unittest
from urllib.request import urlretrieve
import os.path


def download(fromfile, tofile):
    if not os.path.isfile(tofile):
        fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/' + fromfile
        urlretrieve(fn, tofile)    

if __name__ == "__main__":
    
    download('moby_opens.txt', 'moby_dick.txt')
    download('moby_opens.txt', 'not_moby_dick.txt')
    download('sales.sas7bdat', 'sales.sas7bdat')
    download('data.p', 'data.p')
    download('albeck_gene_expression.mat', 'albeck_gene_expression.mat')
    download('battledeath.xlsx', 'battledeath.xlsx')
    download('Chinook.sqlite', 'Chinook.sqlite')
    download('titanic_sub.csv', 'titanic.csv')
    download('tweets3.txt', 'tweets.txt')
    f = open('cars.csv', "w")
    f.write(""",cars_per_cap,country,drives_right
    US,809,United States,True
    AUS,731,Australia,False
    JAP,588,Japan,False
    IN,18,India,False
    RU,200,Russia,True
    MOR,70,Morocco,True
    EG,45,Egypt,True""")
    f.close()
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover("."))
