from app import db
from app.database.section import Section
from app.database.student import Student
from app.database.classes import Classes
from flask_login import current_user

def inputNotNull(input):
    if input is None or input == '':
        return False
    else:
        return True

def verifyDayTimeNoOverlap(existing, new):
    eStart = existing.tStart
    eEnd = existing.tEnd
    nStart = new.tStart
    nEnd = new.tEnd

    overlap = False
    #eStart is after nEnd
    if eStart > nEnd:
        overlap = False
    #eEnd is before nStart
    elif eEnd < nStart:
        overlap = False
    #times overlap
    else:
        overlap = True

    #do times overlap

    if overlap and ((existing.mon and new.mon) or
                    (existing.tue and new.tue) or
                    (existing.wed and new.wed) or
                    (existing.thu and new.thu) or
                    (existing.fri and new.fri)):
        return True
    return False


def verifyCanEnroll(student, section):
    studentEnrolled = student.classesEnrolled
    studentTaken = student.getClassesTaken()
    cID = section.cID
    sectClass = Classes.query.filter(Classes.cID == cID).first()

    #check student is not enrolled in section
    if (section in studentEnrolled):
        return 'You are already enrolled in this section', False

    #check student is not enrolled in another section of same class
    #if they are, prompt if they want to switch if they can take this section
    
    curCIDs = [sect.cID for sect in studentEnrolled]
    if cID in curCIDs:
        return 'You are already enrolled for the class in another section', False

    #check student meets prereqs
    prereqs = sectClass.prereqs
    for prereq in prereqs:
        if prereq not in studentTaken:
            return f'You have not taken pre-requisite class {prereq.getShortName()}', False
    
    #check student has already taken class
    if student.hasTaken(sectClass) and student.passed(sectClass):
        return f'You have already taken and passed {sectClass.getShortName()}', False
    
    #check student schedule does not overlap
    for eSect in studentEnrolled:
        if verifyDayTimeNoOverlap(eSect, section):
            return f'This section overlaps with your existing section for {eSect.sectFor.getShortName()}', False

    #check for lab sections and prompt response on webpage
    #if sectClass.linkedClass or sectClass.linkedTo:
    #   print('evil')
    #  return 'Couldn\'t Enroll', False

    #check section at capacity and prompt response if section is full
    if section.capacity == section.numCurEnrolled:
        #prompt for additional sections here
        return 'This section is at capacity', False
    return 'Enrolled successfully', True

def filterSection(sectList, noOverlaps, showOnlyCanTake):
    cur = Student.query.filter(Student.sID == current_user.get_id()).first()
    if noOverlaps:
        overlapSections = []
        curSects = cur.classesEnrolled
        if curSects:
            for sect in sectList:
                for curSect in curSects:
                    if verifyDayTimeNoOverlap(sect, curSect):
                        overlapSections.append(sect)
                        break
            for sect in overlapSections:
                sectList.remove(sect)
    
    if showOnlyCanTake:
        cantTakeSections = []
        taken = cur.getClassesTaken()
        for sect in sectList:
            if not cur.canTake(sect.sectFor):
                cantTakeSections.append(sect)
                break
        for sect in cantTakeSections:
            sectList.remove(sect)
    return sectList
