import csv
import sys
from app import db
from app.database.models import Department, Faculty


#file validation
def facultyFileValidator(filename):
    if filename[-4:] != '.csv':
        print('File is not a csv.')
        return False
    try:
        with open(filename, newline='') as csvfile:
            print(f'Opened file {filename}.')
            print(f'Beginning validation...')
            reader = csv.DictReader(csvfile)
            csvfile.seek(0)
            knownFID = []
            knownCNumbers = []
            knownPriorities = []
            linenum = 1
            for row in reader:
                fID = row['fID (faculty ID)']
                if fID != '':
                    fID = int(fID)
                    if Faculty.query.filter(Faculty.fID==fID).first() or fID in knownFID:
                        print(f'Error at line {linenum}. Faculty ID = {fID} either already exists in database or exists in a previous entry.')
                        print('Stopping...')
                        return False
                    else:
                        knownFID.append(fID)
                else:
                    print(f'Error at line {linenum}. Faculty ID cannot be null.')
                    print('Stopping...')
                    return False
                fname = row['fname (first name)']
                if fname == '':
                    print(f'Error at line {linenum}. Faculty first name cannot be null.')
                    print('Stopping...')
                    return False
                lname = row['lname (last name)']
                if fname == '':
                    print(f'Error at line {linenum}. Faculty last name cannot be null.')
                    print('Stopping...')
                    return False
                dpID = int(row['dpID (department ID)'])
                if not Department.query.filter(Department.dpID==dpID).first():
                    print(f'Error at line {linenum}. There is no department with ID = {dpID}.')
                    print('Stopping...')
                    return False
                print(f'Line {linenum} validated.')
                linenum += 1    
    except FileNotFoundError:
        print('File not found. Check your spelling and try again.')
        return False
    print("File validated!")
    return True

def facultyFileLoader(filename):
    #create new entries in database
    with open(filename, newline='') as csvfile:
        print('Beginning file load into database...')
        reader = csv.DictReader(csvfile)
        csvfile.seek(0)
        for row in reader:
            fID = int(row['fID (faculty ID)'])
            fname = row['fname (first name)']
            mname = row['mname (middle name)'] 
            lname = row['lname (last name)']
            dpID = int(row['dpID (department ID)'])
            
            entry = Faculty(
                fID=fID,
                fname=fname,
                mname=mname,
                lname=lname,
                dpID=dpID
            )
            db.session.add(entry)
            db.session.commit()
            print(f'Loaded {entry}.')
    print('Finished')
