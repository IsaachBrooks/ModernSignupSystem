from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bc
from app.database.student import Student
from app.database.degree import Degree
from app.database.classes import Classes
from app.database.section import Section
from app.database.department import Department
from app.Scripts.validator import verifyCanEnroll 
from flask_login import current_user


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
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    section = Section.query.filter(Section.crn == crn).first()
    reply = student.unenroll(section)
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

    times = [(sect.tStart, sect.tEnd, sect.mon, sect.tue, sect.wed, sect.thu, sect.fri, sect.cID, sect.crn, sect.sectFor.cNumber, sect.sectFor.getShortName()) for sect in sects]
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
        d['cNumbers'] = [time[9]]
        d['cShort'] = [time[10]]
        fullTimes.append(d)
    
    for time in fullTimes:
        time['tStart'] = time['tStart'].hour * 100 + time['tStart'].minute
        time['tEnd'] = time['tEnd'].hour * 100 + time['tEnd'].minute

    return jsonify(fullTimes)

@app.route("/api/completeCurSections", methods=['POST'])
def completeCurSections():
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    result = {'success': student.completeCurrent()}
    return jsonify(result)

@app.route("/api/getStudentCompleted", methods=['GET'])
def getStudentCompleted():
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    studentTaken = student.classesTaken

    result = [s.serialize() for s in studentTaken]
    return jsonify(result)

@app.route("/api/getCurStudentSections", methods=['GET'])
def getCurStudentSections():
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    sections = student.classesEnrolled
    ret = [sect.serialize() for sect in sections]
    return jsonify(ret)

@app.route("/api/getCurStudentSectionsMinimal", methods=['GET'])
def getCurStudentSectionsMinimal():
    student = Student.query.filter(Student.sID == current_user.get_id()).first()
    sections = student.classesEnrolled
    result = []
    for sect in sections:
        result.append({
            'crn': sect.crn,
            'sec': sect.sec,
            'cNumber': sect.sectFor.cNumber,
            'name': sect.sectFor.name,
            'shortName': sect.sectFor.getShortName()
        })
    return jsonify(result)

