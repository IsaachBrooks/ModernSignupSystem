import csv
import sys
from app import db
from app.database.models import Classes, Department, Degree
from app.Scripts.validator import inputNotNull

#file validation
def degreeClassesListFileValidator(filename):
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
            degree = None
            linenum = 2
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
                dpID = row['dpID (department ID)']
                if dpID != '':
                    dpID = int(dpID)
                    if not Department.query.filter(Department.dpID==dpID).first():
                        print(f'Error at line {linenum}. There is no department with ID = {dpID}.')
                        print('Stopping...')
                        return False
                else:
                    print(f'Error at line {linenum}. Department ID cannot be null.')
                    print('Stopping...')
                    return False
                degreeID = row['degreeID (degree ID)']
                if degreeID != '':
                    degreeID = int(degreeID)
                    if not Degree.query.filter(Degree.degreeID==degreeID).first():
                        print(f'Error at line {linenum}. There is no degree with ID = {degreeID}.')
                        print('Stopping...')           
                        return False
                    else:
                        if degree is None:
                            degree = degreeID
                        else:
                            if degreeID != degree:
                                print(f'Error at line {linenum}. All classes must be part of degree = {degreeID}.')
                                print('Stopping...')           
                                return False
                else:
                    print(f'Error at line {linenum}. Degree ID cannot be null.')
                    print('Stopping...')
                    return False
                
                name = row['name']
                if name == '':
                    print(f'Error at line {linenum}. Class name cannot be null.')
                    print('Stopping...')
                    return False
                desc = row['description']
                if desc != '':
                    if len(desc) > 1000:
                        print(f'Error at line {linenum}. Description is longer than 1000 characters.')
                        print('Stopping...')
                        return False
                else:
                    print(f'Error at line {linenum}. Description Number cannot be null.')
                    print('Stopping...')
                    return False
                prereqs = list(int(cid) for cid in row['prereqs (class IDs comma-space separated)'].split(", ") if cid != '')
                for prereqid in prereqs:
                    if not Classes.query.filter(Classes.cID==prereqid).first() and not prereqid in knownCID:
                        print(f'Error at line {linenum}. prereqid {prereqid} either does not exist in database or does not exist in a previous entry.')
                        print('Stopping...')
                        return False
                coreqs = list(int(cid) for cid in row['coreqs (class IDs comma-space separated)'].split(", ") if cid != '')
                for coreqid in coreqs:
                    if not Classes.query.filter(Classes.cID==coreqid).first() and not coreqid in knownCID:
                        print(f'Error at line {linenum}. coreqid {coreqid} either does not exist in database or does not exist in a previous entry.')
                        print('Stopping...')
                        return False
                linkID = row['linkedTo (Only in second class)']
                if linkID != '':
                    linkID = int(linkID)
                    if not linkID in knownCID:
                        print(f'Error at line {linenum}. linkID {linkID} does not link to a previous entry.')
                        print('Stopping...')
                        return False
                cNumber = row['cNumber (class number)']
                if cNumber != '':
                    cNumber = int(cNumber)
                    if Classes.query.filter(Classes.cNumber==cNumber).filter(Classes.dpID==dpID).first() or (cNumber, dpID) in knownCNumbers:
                        if Classes.query.filter(Classes.cID==linkID).first() or linkID in knownCID:
                            pass
                        else:
                            print(f'Error at line {linenum}. Cnumber {cNumber} already exists within department ID = {dpID}.')
                            print('Stopping...')
                            return False
                    else:
                        knownCNumbers.append((cNumber, dpID))
                else:
                    print(f'Error at line {linenum}. Class Number cannot be null.')
                    print('Stopping...')
                    return False
                priority = row['priority']
                if priority != '':
                    priority = int(priority)                
                    if priority in knownPriorities:
                        print(f'Error at line {linenum}. There is already a class with priority {priority} in the degree with ID = {degreeID}')
                        print('Stopping...')
                        return False
                    else:
                        knownPriorities.append((priority, dpID))
                else:
                    print(f'Error at line {linenum}. Priority cannot be null.')
                    print('Stopping...')
                    return False
                print(f'Line {linenum} validated.')
                linenum += 1    
    except FileNotFoundError:
        print('File not found. Check your spelling and try again.')
        return False
    print("File validated!")
    return True

def degreeClassesListFileLoader(filename):
    #create new entries in database
    with open(filename, newline='') as csvfile:
        print('Beginning file load into database...')
        reader = csv.DictReader(csvfile)
        csvfile.seek(0)
        parentDegree = None
        for row in reader:
            if parentDegree is None:
                degreeID = int(row['degreeID (degree ID)'])
                parentDegree = Degree.query.filter(Degree.degreeID==degreeID).first()
            cID = int(row['cID (classes ID)'])
            dpID = int(row['dpID (department ID)'])
            cNumber = int(row['cNumber (class number)'])
            name = row['name']
            desc = row['description']
            prereqs = list(int(cid) for cid in row['prereqs (class IDs comma-space separated)'].split(", ") if cid != '')
            coreqs = list(int(cid) for cid in row['coreqs (class IDs comma-space separated)'].split(", ") if cid != '')
            priority = int(row['priority'])
            elective = bool(row['elective'])
            lab = bool(row['lab'])
            
            linkID = int(row['linkedTo (Only in second class)']) if row['linkedTo (Only in second class)'] != '' else None

            entry = Classes(
                cID=cID, 
                dpID=dpID, 
                cNumber=cNumber,
                name=name, 
                description=desc,
                elective=elective,
                lab=lab
            )
            if len(prereqs) > 0:
                for cid in prereqs:
                    prereqClass = Classes.query.filter(Classes.cID==cid).first()
                    entry.prereqs.append(prereqClass)
            if len(coreqs) > 0:
                for cid in coreqs:
                    prereqClass = Classes.query.filter(Classes.cID==cid).first()
                    entry.coreqs.append(prereqClass)
            
            parentDegree.addClass(entry, priority)
            if linkID:
                linkIDClass = Classes.query.filter(Classes.cID==linkID).first()
                linkIDClass.addLinkedClass(entry)
            print(f'Loaded {entry}.')
    print('Finished')
