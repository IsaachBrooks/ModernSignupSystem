from app.Scripts.tableLoaderCSVDepartment import departmentFileValidator, departmentFileLoader

filename = 'testdata/department-test.csv' #input('Department file CSV: ')

if (departmentFileValidator(filename)):
    departmentFileLoader(filename)
