import unittest

if __name__ == "__main__":
  from urllib.request import urlretrieve
  fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/moby_opens.txt'
  urlretrieve(fn, 'moby_dick.txt')
  urlretrieve(fn, 'not_moby_dick.txt')
  fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/sales.sas7bdat'
  urlretrieve(fn, 'sales.sas7bdat')
  fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/data.p'
  urlretrieve(fn, 'data.p')
  fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/ja_data2.mat'
  urlretrieve(fn, 'albeck_gene_expression.mat')
  fn = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/battledeath.xlsx'
  urlretrieve(fn, 'battledeath.xlsx')
  fn1 = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_998/datasets/Chinook.sqlite'
  urlretrieve(fn1, 'Chinook.sqlite')
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
