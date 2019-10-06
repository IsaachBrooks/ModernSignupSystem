from app.Scripts.loadSectionCSV import sectionFileValidator, sectionFileLoader

filename = input('Section file CSV: ')

if (sectionFileValidator(filename)):
    sectionFileLoader(filename)
