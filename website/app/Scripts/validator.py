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
    if eStart >= nEnd:
        overlap = False
    #eEnd is before nStart
    elif eEnd <= nStart:
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


def verifyCanEnroll(student, sections):
    studentEnrolled = student.classesEnrolled
    studentTaken = student.getClassesTaken()
    if (type(sections) != list):
        sections = [sections]
    for sect in sections:
        cID = sect.cID
        sectClass = Classes.query.filter(Classes.cID == cID).first()

        #check student is not enrolled in section
        if (sect in studentEnrolled):
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
            if verifyDayTimeNoOverlap(eSect, sect):
                return f'This section overlaps with your existing section for {eSect.sectFor.getShortName()}', False

        #check for lab sections and prompt response on webpage
        #if sectClass.linkedClass or sectClass.linkedTo:
        #   print('evil')
        #  return 'Couldn\'t Enroll', False

        #check section at capacity and prompt response if section is full
        if sect.capacity == sect.numCurEnrolled:
            #prompt for additional sections here
            return 'This section is at capacity', False
    if len(sections) == 1:
        return f'Enrolled successfully in {sections[0].sectFor.name}', True
    else:
        return f'Enrolled successfully in {sections[0].sectFor.name} and {sections[1].sectFor.name}', True


def filterSection(sectList, noOverlaps, showOnlyCanTake, hideCompleted, hideCurrent):
    cur = Student.query.filter(Student.sID == current_user.get_id()).first()
    numFiltered = 0
    if noOverlaps:
        toRemove = []
        curSects = cur.classesEnrolled
        if curSects:
            for sect in sectList:
                for curSect in curSects:
                    if verifyDayTimeNoOverlap(sect, curSect):
                        toRemove.append(sect)
                        break
            numFiltered += len(toRemove)
            for sect in toRemove:
                sectList.remove(sect)
    
    if showOnlyCanTake:
        toRemove = []
        taken = cur.getClassesTaken()
        for sect in sectList:
            if not cur.canTake(sect.sectFor):
                toRemove.append(sect)
        numFiltered += len(toRemove)        
        for sect in toRemove:
            sectList.remove(sect)

    if hideCompleted:
        complete = cur.getClassesTaken()
        toRemove = []
        for sect in sectList:
            if sect.sectFor in complete:
                toRemove.append(sect)
                if sect.sectFor.hasLinkedClass():
                    cID = sect.sectFor.getLinkedClass().cID
                    links = Section.query.filter(Section.cID == cID).all()
                    for link in links:
                        if (link not in toRemove and link in sectList):
                            toRemove.append(link)
        numFiltered += len(toRemove)
        for sect in toRemove:
            sectList.remove(sect)
            
    if hideCurrent:
        curSects = cur.classesEnrolled
        if curSects:
            for sect in curSects:
                if sect in sectList:
                    numFiltered += 1
                    sectList.remove(sect)
    return numFiltered
