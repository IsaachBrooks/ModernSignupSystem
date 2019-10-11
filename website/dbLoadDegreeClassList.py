from app.Scripts.tableLoaderCSVDegreeClassList import degreeClassesListFileValidator, degreeClassesListFileLoader

filename = 'testdata/Test_DegreeClassList.csv'

#filename = input('Class file CSV: ')
if (degreeClassesListFileValidator(filename)):
    degreeClassesListFileLoader(filename)