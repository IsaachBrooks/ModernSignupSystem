from app.Scripts.tableLoaderCSVFaculty import facultyFileValidator, facultyFileLoader

filename = 'testdata/faculty-test.csv'

#filename = input('Faculty file CSV: ')

if (facultyFileValidator(filename)):
    facultyFileLoader(filename)