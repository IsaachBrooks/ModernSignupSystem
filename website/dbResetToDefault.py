import sys
from getpass import getpass
from app import db, bc
from app.database.models import *
from app.Scripts.tableLoaderCSVDepartment import departmentFileValidator, departmentFileLoader
from app.Scripts.tableLoaderCSVDegree import degreeFileValidator, degreeFileLoader
from app.Scripts.tableLoaderCSVFaculty import facultyFileValidator, facultyFileLoader
from app.Scripts.tableLoaderCSVClasses import classesFileValidator, classesFileLoader
from app.Scripts.tableLoaderCSVSection import sectionFileValidator, sectionFileLoader


password = '$2b$12$He6gTRczz5WA/kndXOu47ehYHbRjQaNvHQAlRtw4tO4Qft1c29vpa'

print("Imported")
if not bc.check_password_hash(password, getpass('\nEnter password to reset database: ')):
    sys.exit('Incorrect password. Exiting.')
print('Password confirmed.')
print("Dropping all tables...")
db.drop_all()
print("Tables dropped.")
print("Creating all tables...")
db.create_all()
print("tables created:")
print(db.engine.table_names())

"""
To load the default dataset properly load order MUST be as follows:
1. Department
2. Degree
3. Faculty
4. Classes
5. Section
"""

defaultDepartment_path = 'defaultdata/defaultDataset_Department.csv'
defaultDegree_path = 'defaultdata/defaultDataset_Degree.csv'
defaultFaculty_path = 'defaultdata/defaultDataset_Faculty.csv'
defaultClasses_path = 'defaultdata/defaultDataset_Classes.csv'
defaultSection_path = 'defaultdata/defaultDataset_Section.csv'

print('Validating default Department dataset at path = {default_path} .')
if departmentFileValidator(defaultDepartment_path):
    departmentFileLoader(defaultDepartment_path)
else:
    sys.exit('Failed to validate default Department.\nNo existing tables to drop. exiting.')

print('Validating default Degree dataset at path = {defaultDegree_path} .')
if degreeFileValidator(defaultDegree_path):
    degreeFileLoader(defaultDegree_path)
else:
    db.drop_all()
    sys.exit('Failed to validate default Degree.\nDropping existing tables and exiting.')

print('Validating default Faculty dataset at path = {defaultFaculty_path} .')
if facultyFileValidator(defaultFaculty_path):
    facultyFileLoader(defaultFaculty_path)
else:
    db.drop_all()
    sys.exit('Failed to validate default Faculty.\nDropping existing tables and exiting.')

print('Validating default Classes dataset at path = {defaultClasses_path} .')
if classesFileValidator(defaultClasses_path):
    classesFileLoader(defaultClasses_path)
else:
    db.drop_all()
    sys.exit('Failed to validate default Classes.\nDropping existing tables and exiting.')

print('Validating default Section dataset at path = {defaultSection_path} .')
if sectionFileValidator(defaultSection_path):
    sectionFileLoader(defaultSection_path)
else:
    db.drop_all()
    sys.exit('Failed to validate default Section.\nDropping existing tables and exiting.')

print('Default Dataset loaded successfully into database!')