from app.Scripts.tableLoaderCSVSection import sectionFileValidator, sectionFileLoader

filename = 'testdata/section-test.csv'

#filename = input('Section file CSV: ')

if (sectionFileValidator(filename)):
    sectionFileLoader(filename)
