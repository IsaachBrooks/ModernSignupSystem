from app.Scripts.tableLoaderCSVClasses import classesFileValidator, classesFileLoader

filename = 'testdata/classes-test.csv'

#filename = input('Class file CSV: ')

if (classesFileValidator(filename)):
    classesFileLoader(filename)