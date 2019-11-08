from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bc
from app.database.student import Student
from app.database.degree import Degree
from app.database.classes import Classes
from app.database.section import Section
from app.database.department import Department
from app.Scripts.validator import verifyCanEnroll 
from flask_login import current_user


@app.route("/api/getSectionDataFull", methods=['GET'])
def getSectionDataFull():
    sections = Section.query.all()
    sections_serial = [item.serialize() for item in sections]
    return jsonify(sections_serial)

@app.route("/api/getCurrentUserData", methods=['GET'])
def getCurrentUserData():
    user = Student.query.filter(Student.sID == current_user.get_id()).first()
    user_serial = user.serialize()
    return jsonify(user_serial)

@app.route("/api/getClassesDataFull", methods=['GET'])
def getClassesDataFull():
    classes = Classes.query.all()
    classes_serial = [item.serialize() for item in classes]
    return jsonify(classes_serial)

@app.route("/api/getDegreeDataFull", methods=['GET'])
def getDegreeDataFull():
    degrees = Degree.query.all()
    degrees_serial = [item.serialize() for item in degrees]
    return jsonify(degrees_serial)

@app.route("/api/getSectionTimesDaysFull", methods=['GET'])
def getSectionTimesDaysFull():
    sects = Section.query.all()
    times = [(sect.tStart, sect.tEnd, sect.mon, sect.tue, sect.wed, sect.thu, sect.fri) for sect in sects]
    times = set(times)
    fullTimes = []

    for time in times:
        d = {}
        d['tStart'] = time[0]
        d['tEnd'] = time[1]
        d['days'] = [time[2], time[3], time[4], time[5], time[6]]
        d['count'] = 0
        d['cID'] = []
        d['crn'] = []
        fullTimes.append(d)
    
    for time in fullTimes:
        for sect in sects:
            if (sect.tStart == time['tStart'] and sect.tEnd == time['tEnd'] and sect.getDaysArray() == time['days']):
                time['count'] += 1
                if sect.cID not in time['cID']:
                    time['cID'].append(sect.cID)
                if sect.crn not in time['crn']:
                    time['crn'].append(sect.crn)
    for time in fullTimes:
        time['tStart'] = time['tStart'].hour * 100 + time['tStart'].minute
        time['tEnd'] = time['tEnd'].hour * 100 + time['tEnd'].minute

    return jsonify(fullTimes)

@app.route("/api/getSectionTimesDays", methods=['GET'])
def getSectionTimesDays():
    sect = Section.query.first()
    time = [sect.tStart, sect.tEnd, sect.mon, sect.tue, sect.wed, sect.thu, sect.fri]
    
    section = {
    'tStart': time[0].hour * 100 + time[0].minute,
    'tEnd': time[1].hour * 100 + time[0].minute,
    'days': [time[2], time[3], time[4], time[5], time[6]],
    'count': 1,
    'cID': sect.cID
    }
    return jsonify(section)

@app.route("/api/getSectionsInfo/[<string:sCRNs>]", methods=['GET'])
def getSectionsInfo(sCRNs):
    sects = [int(crn) for crn in sCRNs.split(',')]
    sectionList = []
    for sect in sects:
        sectionList.append(Section.query.filter(Section.crn == sect).first().serialize())
    return jsonify(sectionList)

@app.route("/api/getClassInfo/<int:cID>", methods=['GET'])
def getClassInfo(cID):
    singleClass = Classes.query.filter(Classes.cID == cID).first()
    if singleClass:
        return jsonify(singleClass.serialize())

@app.route("/api/getClassInfoMinimal/<int:cID>", methods=['GET'])
def getClassInfoMinimal(cID):
    singleClass = Classes.query.filter(Classes.cID == cID).first()
    ret = {
        'name' : singleClass.name,
        'cNumber' : singleClass.cNumber,
        'deptCode' : singleClass.department.code
    }
    return jsonify(ret)


@app.route("/api/getSectionInfo/<string:sCRN>", methods=['GET'])
def getSectionInfo(sCRN):
    return jsonify(Section.query.filter(Section.crn == sCRN).first().serialize())
    
@app.route("/api/getCurStudentSections", methods=['GET'])
def getCurStudentSections():
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    sections = student.classesEnrolled
    ret = [sect.serialize() for sect in sections]
    return jsonify(ret)


@app.route("/api/enrollStudent", methods=['POST'])
def enrollStudent():
    #Need to add lots of error checking
    #Section at capacity
    #Prereqs not met
    #Overlapping schedule
    #prompt to register for lab section, maybe do this in javascript?
    #already registered for same class in another section
    #maybe some warnings about not needed certain classes
    #if a section is full, suggest another
    json = request.get_json()
    crn = json['crn']
    reply = ''
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    section = Section.query.filter(Section.crn == crn).first()
    reply, success = verifyCanEnroll(student, section)
    if success: 
        student.enroll(section)
    return jsonify({'reply': reply, 'success': success})

@app.route("/api/removeEnrolledClass", methods=['POST'])
def removeEnrolledClass():
    #Need to add lots of error checking
    #Check for linked sections, and remove those as well
    json = request.get_json()
    crn = json['crn']
    print(crn)
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    section = Section.query.filter(Section.crn == crn).first()
    reply = ''
    if section in student.classesEnrolled:
        student.classesEnrolled.remove(section)
        print(student.classesEnrolled)
        section.numCurEnrolled -= 1
        db.session.commit()
        reply = 'Successfully unregister for section!'
    else:
        reply = 'Could not unregister for section.'
    return jsonify({'reply': reply})
    
@app.route("/api/isCurStudentRegisteredFor/<int:crn>", methods=['GET'])
def isCurStudentRegisteredFor(crn):
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    sections = student.classesEnrolled
    if sections:
        crns = [sect.crn for sect in sections]
        if crn in crns:
            return jsonify(result=True)
    return jsonify(result=False)

@app.route("/api/getStudentSectionListFull", methods=['GET'])
def getStudentSectionListFull():
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    sections = student.classesEnrolled
    return jsonify([sect.serialize() for sect in sections])

@app.route("/api/getStudentSectionsDraw", methods=['GET'])
def getStudentSectionsDraw():
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    sects = student.classesEnrolled

    times = [(sect.tStart, sect.tEnd, sect.mon, sect.tue, sect.wed, sect.thu, sect.fri, sect.cID, sect.crn) for sect in sects]
    times = set(times)
    fullTimes = []

    for time in times:
        d = {}
        d['tStart'] = time[0]
        d['tEnd'] = time[1]
        d['days'] = [time[2], time[3], time[4], time[5], time[6]]
        d['count'] = 1
        d['cID'] = [time[7]]
        d['crn'] = [time[8]]
        fullTimes.append(d)
    
    for time in fullTimes:
        time['tStart'] = time['tStart'].hour * 100 + time['tStart'].minute
        time['tEnd'] = time['tEnd'].hour * 100 + time['tEnd'].minute

    return jsonify(fullTimes)

@app.route("/api/getDepartmentNamesIDs", methods=['GET'])
def getDepartmentNamesIDs():
    deps = Department.query.all()
    ret = []
    for dep in deps:
        ret.append({'name': dep.name, 'dpID': dep.dpID})
    return jsonify(ret)

"""
@app.route("/api/getSectionsByDepartment/<int:dpID>", methods=['GET'])
def getSectionsByDepartment():
    sects = Section.query.all()
    times = [(sect.tStart, sect.tEnd, sect.mon, sect.tue, sect.wed, sect.thu, sect.fri) for sect in sects]
    times = set(times)
    fullTimes = []

    for time in times:
        d = {}
        d['tStart'] = time[0]
        d['tEnd'] = time[1]
        d['days'] = [time[2], time[3], time[4], time[5], time[6]]
        d['count'] = 0
        d['cID'] = []
        d['crn'] = []
        fullTimes.append(d)
    
    for time in fullTimes:
        for sect in sects:
            if (sect.tStart == time['tStart'] and sect.tEnd == time['tEnd'] and sect.getDaysArray() == time['days']):
                time['count'] += 1
                if sect.cID not in time['cID']:
                    time['cID'].append(sect.cID)
                if sect.crn not in time['crn']:
                    time['crn'].append(sect.crn)
    for time in fullTimes:
        time['tStart'] = time['tStart'].hour * 100 + time['tStart'].minute
        time['tEnd'] = time['tEnd'].hour * 100 + time['tEnd'].minute

    return jsonify(fullTimes)

@app.route("/api/", methods=[])
def api():
    return jsonify(result)

"""

