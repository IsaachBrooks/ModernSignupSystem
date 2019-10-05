from app.Scripts.loadDegreeCSV import degreeFileValidator, degreeFileLoader

filename = input('Degree file CSV: ')

if (degreeFileValidator(filename)):
    degreeFileLoader(filename)