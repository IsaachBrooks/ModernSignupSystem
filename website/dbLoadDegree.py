from app.Scripts.tableLoaderCSVDegree import degreeFileValidator, degreeFileLoader

filename = 'testdata/degree-test.csv'

#filename = input('Degree file CSV: ')

if (degreeFileValidator(filename)):
    degreeFileLoader(filename)