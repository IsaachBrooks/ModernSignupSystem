from app.Scripts.loadFacultyCSV import facultyFileValidator, facultyFileLoader

filename = 'testdata/faculty-test.csv'
facultyFileValidator(filename)


filename = input('Faculty file CSV: ')

if (facultyFileValidator(filename)):
    facultyFileLoader(filename)