from app.Scripts.loadClassesCSV import classesFileValidator, classesFileLoader

filename = input('Class file CSV: ')

if (classesFileValidator(filename)):
    classesFileLoader(filename)