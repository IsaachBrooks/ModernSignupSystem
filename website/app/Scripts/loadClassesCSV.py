import csv
import sys
from app import db
from app.database.models import Classes, Department, Degree


#file validation
def classesFileValidator(filename):
    if filename[-4:] != '.csv':
        print('File is not a csv.')
        return False
    try:
        with open(filename, newline='') as csvfile:
            print(f'Opened file {filename}.')
            print(f'Beginning validation...')
            reader = csv.DictReader(csvfile)
            csvfile.seek(0)
            knownCID = []
            knownCNumbers = []
            knownPriorities = []
            linenum = 1
            for row in reader:
                cID = row['cID (classes ID)']
                if cID != '':
                    cID = int(cID)
                    if Classes.query.filter(Classes.cID==cID).first() or cID in knownCID:
                        print(f'Error at line {linenum}. Class ID = {cID} either already exists in database or exists in a previous entry.')
                        print('Stopping...')
                        return False
                    else:
                        knownCID.append(cID)
                else:
                    print(f'Error at line {linenum}. Class ID cannot be null.')
                    print('Stopping...')
                    return False
                dpID = int(row['dpID (department ID)'])
                if not Department.query.filter(Department.dpID==dpID).first():
                    print(f'Error at line {linenum}. There is no department with ID = {dpID}.')
                    print('Stopping...')
                    return False
                degreeID = int(row['degreeID (degree ID)'])
                if not Degree.query.filter(Degree.degreeID==degreeID).first():
                    print(f'Error at line {linenum}. There is no degree with ID = {degreeID}.')
                    print('Stopping...')           
                    return False
                cNumber = int(row['cNumber (class number)'])
                if Classes.query.filter(Classes.cNumber==cNumber).filter(Classes.dpID==dpID).filter(Classes.degreeID==degreeID).first() or (cNumber, dpID, degreeID) in knownCNumbers:
                    print(f'Error at line {linenum}. Cnumber {cNumber} already exists within department ID = {dpID} and Degree = {degreeID}.')
                    print('Stopping...')
                    return False
                else:
                    knownCNumbers.append((cNumber, dpID, degreeID))
                name = row['name']
                if name == '':
                    print(f'Error at line {linenum}. Class name cannot be null.')
                    print('Stopping...')
                    return False
                desc = row['description']
                if len(desc) > 1000:
                    print(f'Error at line {linenum}. Description is longer than 1000 characters.')
                    print('Stopping...')
                    return False
                prereqs = list(int(cid) for cid in row['prereqs (class IDs comma-space separated)'].split(", ") if cid != '')
                for prereqid in prereqs:
                    if not Classes.query.filter(Classes.cID==prereqid).first() and not prereqid in knownCID:
                        print(f'Error at line {linenum}. prereqid {prereqid} either does not exist in database or does not exist in a previous entry.')
                        print('Stopping...')
                        return False
                priority = int(row['priority'])
                if Classes.query.filter(Classes.degreeID==degreeID).filter(Classes.priority==priority).first() or (priority, degreeID) in knownPriorities:
                    print(f'Error at line {linenum}. There is already a class with priority {priority} in the degree with ID = {degreeID}')
                    print('Stopping...')
                    return False
                else:
                    knownPriorities.append((priority, dpID))
                print(f'Line {linenum} validated.')
                linenum += 1    
    except FileNotFoundError:
        print('File not found. Check your spelling and try again.')
        return False
    print("File validated!")
    return True

def classesFileLoader(filename):
    #create new entries in database
    with open(filename, newline='') as csvfile:
        print('Beginning file load into database...')
        reader = csv.DictReader(csvfile)
        csvfile.seek(0)
        for row in reader:
            cID = int(row['cID (classes ID)'])
            dpID = int(row['dpID (department ID)'])
            degreeID = int(row['degreeID (degree ID)'])
            cNumber = int(row['cNumber (class number)'])
            name = row['name']
            desc = row['description']
            prereqs = list(int(cid) for cid in row['prereqs (class IDs)'].split(" "))
            priority = int(row['priority'])
            
            entry = Classes(
                cID=cID, 
                dpID=dpID, 
                degreeID=degreeID, 
                cNumber=cNumber,
                name=name, 
                description=desc, 
                priority=priority
            )
            if len(prereqs) > 0:
                for cid in prereqs:
                    prereqClass = Classes.query.filter(Classes.cID==cid).first()
                    entry.prereqs.append(prereqClass)
            db.session.add(entry)
            db.session.commit()
            print(f'Loaded {entry}.')
    print('Finished')
