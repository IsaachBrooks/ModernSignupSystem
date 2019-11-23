import csv
import sys
from app import db
from app.database.department import Department
import re

#file validation
def departmentFileValidator(filename):
    if filename[-4:] != '.csv':
        print('File is not a csv.')
        return False
    try:
        with open(filename, newline='') as csvfile:
            print(f'Opened file {filename}.')
            print(f'Beginning validation...')
            reader = csv.DictReader(csvfile)
            csvfile.seek(0)
            knownDpID = []
            knownCode = []
            linenum = 2
            for row in reader:
                dpID = row['dpID (department ID)']
                if dpID != '':
                    dpID = int(dpID)
                    if Department.query.filter(Department.dpID==dpID).first() or dpID in knownDpID:
                        print(f'Error at line {linenum}. Department with ID = {dpID} already exists.')
                        print('Stopping...')
                        return False 
                    else:
                        knownDpID.append(dpID)
                else:
                    print(f'Error at line {linenum}. Department ID cannot be null.')
                    print('Stopping...')
                    return False
                name = row['name']
                if name != '':
                    pass
                else:
                    print(f'Error at line {linenum}. Department Name cannot be null.')
                    print('Stopping...')
                    return False
                code = row['code']
                if code != '':
                    if not re.match('^[a-zA-Z]{2,4}$', code):
                        print(f'Error at line {linenum}. Code can only contain between 2 and 4 alphabet characters.')
                        print('Stopping...')
                        return False
                    if Department.query.filter(Department.code==code).first() or code in knownCode:
                        print(f'Error at line {linenum}. There is already a department with code = {code}.')
                        print('Stopping...')
                        return False
                    else:
                        knownCode.append(code)
                else:
                    print(f'Error at line {linenum}. Department Code cannot be null.')
                    print('Stopping...')
                    return False
                
                print(f'Line {linenum} validated.')
                linenum += 1    
    except FileNotFoundError:
        print('File not found. Check your spelling and try again.')
        return False
    print("File validated!")
    return True

def departmentFileLoader(filename):
    #create new entries in database
    with open(filename, newline='') as csvfile:
        print('Beginning file load into database...')
        reader = csv.DictReader(csvfile)
        csvfile.seek(0)
        for row in reader:
            dpID = int(row['dpID (department ID)'])
            name = row['name']
            code = row['code']
            
            entry = Department( 
                dpID=dpID,
                name=name,
                code=code
            )
            db.session.add(entry)
            db.session.commit()
            print(f'Loaded {entry}.')
    print('Finished loading department data')
