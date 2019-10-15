from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bc
from app.database.models import Section, Student, Classes, Degree
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
        fullTimes.append(d)
    
    for time in fullTimes:
        for sect in sects:
            if (sect.tStart == time['tStart'] and sect.tEnd == time['tEnd'] and sect.getDaysArray() == time['days']):
                time['count'] += 1
                if sect.cID not in time['cID']:
                    time['cID'].append(sect.cID)
    for time in fullTimes:
        time['tStart'] = time['tStart'].hour * 100 + time['tStart'].minute
        time['tEnd'] = time['tEnd'].hour * 100 + time['tEnd'].minute

    return jsonify(fullTimes)

    
"""
@app.route("/api/get", methods=['GET'])
def get():
    pass

@app.route("/api/name", methods=['GET'])
def name():
    pass

@app.route("/api/name", methods=['GET'])
def name():
    pass

@app.route("/api/name", methods=['GET'])
def name():
    pass

@app.route("/api/name", methods=['GET'])
def name():
    pass

@app.route("/api/name", methods=['GET'])
def name():
    pass

    @app.route("/api/name", methods=['GET'])
def name():
    pass
"""
