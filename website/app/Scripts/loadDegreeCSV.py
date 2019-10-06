import csv
import sys
from app import db
from app.database.models import Classes, Department, Degree
import re

#file validation
def degreeFileValidator(filename):
    if filename[-4:] != '.csv':
        print('File is not a csv.')
        return False
    try:
        with open(filename, newline='') as csvfile:
            print(f'Opened file {filename}.')
            print(f'Beginning validation...')
            reader = csv.DictReader(csvfile)
            csvfile.seek(0)
            knowndegreeID = []
            linenum = 1
            for row in reader:
                degreeID = row['degreeID (degree ID)']
                if degreeID != '':
                    degreeID = int(degreeID)
                    if Degree.query.filter(Degree.degreeID==degreeID).first() or degreeID in knowndegreeID:
                        print(f'Error at line {linenum}. Degree ID = {degreeID} either already exists in database or exists in a previous entry.')
                        print('Stopping...')
                        return False
                    else:
                        knowndegreeID.append(degreeID)
                else:
                    print(f'Error at line {linenum}. Degree ID cannot be null.')
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
                name = row['name']
                if name != '':
                    if Degree.query.filter(Degree.name==name).first():
                        print(f'Error at line {linenum}. A degree with name = {name} already exists.')
                        print('Stopping...')
                        return False
                else:
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
                totalHours= row['totalHours']
                if totalHours != '':
                    if not re.match('^[\d]+$', totalHours):
                        print(f'Error at line {linenum}. Total Hours can only contain 0-9.')
                else:
                    print(f'Error at line {linenum}. Total Hours cannot be null.')
                    print('Stopping...')
                    return False
                print(f'Line {linenum} validated.')
                linenum += 1    
    except FileNotFoundError:
        print('File not found. Check your spelling and try again.')
        return False
    print("File validated!")
    return True

def degreeFileLoader(filename):
    #create new entries in database
    with open(filename, newline='') as csvfile:
        print('Beginning file load into database...')
        reader = csv.DictReader(csvfile)
        csvfile.seek(0)
        for row in reader:
            degreeID = int(row['degreeID (degree ID)'])
            dpID = int(row['dpID (department ID)'])
            name = row['name']
            totalHours= int(row['totalHours'])
            desc = row['description']
            
            entry = Degree(
                degreeID=degreeID,
                dpID=dpID, 
                name=name,
                totalHours=totalHours,
                description=desc
            )
            db.session.add(entry)
            db.session.commit()
            print(f'Loaded {entry}.')
    print('Finished')
