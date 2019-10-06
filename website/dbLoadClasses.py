from app.Scripts.loadClassesCSV import classesFileValidator, classesFileLoader

filename = 'testdata/classes-test.csv'

#filename = input('Class file CSV: ')

if (classesFileValidator(filename)):
    classesFileLoader(filename)