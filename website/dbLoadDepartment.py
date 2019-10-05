from app.Scripts.loadDepartmentCSV import departmentFileValidator, departmentFileLoader

filename = input('Department file CSV: ')

if (departmentFileValidator(filename)):
    departmentFileLoader(filename)
