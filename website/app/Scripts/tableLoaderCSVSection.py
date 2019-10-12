import csv
import sys
from app import db
from app.database.models import Classes, Department, Degree, Section, Faculty
import re
import datetime

timeMatchString = '^([\d]{1,2}):([\d]{2}):([\d]{2})$'
dateMatchString = '^([\d]{1,2})/([\d]{1,2})/([\d]{4})$'

def constructTime(timeString):
    match = re.match(timeMatchString, timeString)
    if match is not None:
        hrs = int(match.group(1))
        mins = int(match.group(2))
        secs = int(match.group(3))
        return datetime.time(hrs, mins, secs)
    return None
    
def constructDate(dateString):
    match = re.match(dateMatchString, dateString)
    if match is not None:
        yrs = int(match.group(3))
        mnth = int(match.group(1))
        day = int(match.group(2))
        return datetime.date(yrs, mnth, day)
    return None

def sectionExists(cID, iID, mon, tue, wed, thu, fri, tStart, tEnd, dateStart, dateEnd, capacity):
    section = Section.query \
            .filter(Section.cID==cID) \
            .filter(Section.iID==iID) \
            .filter(Section.mon==mon) \
            .filter(Section.tue==tue) \
            .filter(Section.wed==wed) \
            .filter(Section.thu==thu) \
            .filter(Section.fri==fri) \
            .filter(Section.tStart==tStart) \
            .filter(Section.tEnd==tEnd) \
            .filter(Section.dateStart==dateStart) \
            .filter(Section.dateEnd==dateEnd).first()
    return section

#file validation
def sectionFileValidator(filename):
    if filename[-4:] != '.csv':
        print('File is not a csv.')
        return False
    try:
        with open(filename, newline='') as csvfile:
            print(f'Opened file {filename}.')
            print(f'Beginning validation...')
            reader = csv.DictReader(csvfile)
            csvfile.seek(0)
            linenum = 2
            for row in reader:
                cID = row['cID (classes ID)']
                if cID != '':
                    cID = int(cID)
                    if not Classes.query.filter(Classes.cID==cID).first():
                        print(f'Error at line {linenum}. Class ID = {cID} does not exist.')
                        print('Stopping...')
                        return False
                else:
                    print(f'Error at line {linenum}. Class ID cannot be null.')
                    print('Stopping...')
                    return False
                sec = row['sec']
                if sec != '':
                    pass
                else:
                    print(f'Error at line {linenum}. Section Number cannot be null.')
                    print('Stopping...')
                    return False
                iID = row['iID (instructor ID)']
                if iID != '':
                    iID = int(iID)
                    if not Faculty.query.filter(Faculty.fID==iID).first():
                        print(f'Error at line {linenum}. Instructor ID = {iID} does not exist.')
                        print('Stopping...')
                        return False
                else:
                    print(f'Error at line {linenum}. Instructor ID cannot be null.')
                    print('Stopping...')
                    return False
                tStart = row['tStart(00:00:00)24hr']
                if tStart != '':
                    timeStart = constructTime(tStart)
                    if timeStart is None:
                        print(f'Error at line {linenum}. Could not construct datetime.time object with from Time Start')
                        print('Stopping...')
                        return False 
                else:
                    print(f'Error at line {linenum}. Time Start cannot be null.')
                    print('Stopping...')
                    return False
                tEnd = row['tEnd(00:00:00)24hr']
                if tEnd != '':
                    timeEnd = constructTime(tEnd)
                    if timeEnd is None:
                        print(f'Error at line {linenum}. Could not construct datetime.time object with from Time End')
                        print('Stopping...')
                        return False 
                else:
                    print(f'Error at line {linenum}. Time End cannot be null.')
                    print('Stopping...')
                    return False
                if timeEnd < timeStart:
                    print(f'Error at line {linenum}. Time End cannot be before Time Start.')
                    print('Stopping...')
                    return False
                dStart = row['dateStart(mm/dd/yyyy)']
                if dStart != '':
                    dateStart = constructDate(dStart)
                    if dateStart is None :
                        print(f'Error at line {linenum}. Could not construct datetime.date object with from Date Start')
                        print('Stopping...')
                        return False 
                else:
                    print(f'Error at line {linenum}. Date Start cannot be null.')
                    print('Stopping...')
                    return False
                dEnd = row['dateEnd(mm/dd/yyyy)']
                if dEnd != '':
                    dateEnd = constructDate(dEnd)
                    if dateEnd is None:
                        print(f'Error at line {linenum}. Could not construct datetime.date object with from Date End')
                        print('Stopping...')
                        return False 
                else:
                    print(f'Error at line {linenum}. Date End cannot be null.')
                    print('Stopping...')
                    return False
                if dateEnd < dateStart:
                    print(f'Error at line {linenum}. Date End cannot be before Date Start.')
                    print('Stopping...')
                    return False
                capacity = row['capacity']
                if capacity != '':
                    if not re.match('^[\d]+$', capacity):
                        print(f'Error at line {linenum}. Capacity can only contain 0-9.')
                        print('Stopping...')
                        return False
                else:
                    print(f'Error at line {linenum}. Capacity cannot be null.')
                    print('Stopping...')
                    return False
                print(f'Line {linenum} validated.')
                mon = bool(row['mon'])
                tue = bool(row['tue'])
                wed = bool(row['wed'])
                thu = bool(row['thu'])
                fri = bool(row['fri'])
                sect = sectionExists(cID, iID, mon, tue, wed, thu, fri, tStart, tEnd, dateStart, dateEnd, capacity)
                if sect:
                    print(f'Error at line {linenum}. {sect} already exists with CRN = {sect.crn}.')
                    print('Stopping...')
                    return False
                linenum += 1    
    except FileNotFoundError:
        print('File not found. Check your spelling and try again.')
        return False
    print("File validated!")
    return True

def sectionFileLoader(filename):
    #create new entries in database
    with open(filename, newline='') as csvfile:
        print('Beginning file load into database...')
        reader = csv.DictReader(csvfile)
        csvfile.seek(0)
        for row in reader:
            cID = int(row['cID (classes ID)'])
            sec = int(row['sec'])
            iID = int(row['iID (instructor ID)'])
            mon = bool(row['mon'])
            tue = bool(row['tue'])
            wed = bool(row['wed'])
            thu = bool(row['thu'])
            fri = bool(row['fri'])
            tStart = constructTime(row['tStart(00:00:00)24hr'])
            tEnd = constructTime(row['tEnd(00:00:00)24hr'])
            dStart = constructDate(row['dateStart(mm/dd/yyyy)'])
            dEnd = constructDate(row['dateEnd(mm/dd/yyyy)'])
            capacity = int(row['capacity'])
            
            entry = Section(
                cID=cID,
                sec=sec, 
                iID=iID,
                mon = mon,
                tue = tue,
                wed = wed,
                thu = thu,
                fri = fri,
                tStart = tStart,
                tEnd = tEnd,
                dateStart = dStart,
                dateEnd = dEnd,
                capacity = capacity   
            )
            db.session.add(entry)
            db.session.commit()
            print(f'Loaded {entry}.')
    print('Finished loading section data.')
