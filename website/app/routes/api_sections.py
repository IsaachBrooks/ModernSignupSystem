from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bc
from app.database.student import Student
from app.database.degree import Degree
from app.database.classes import Classes
from app.database.section import Section
from app.database.department import Department
from app.Scripts.validator import verifyCanEnroll, filterSection 
from app.Scripts.inputConversion import strToBool
from flask_login import current_user

def processSections(sects):
    times = [
        (
            sect.tStart, 
            sect.tEnd, 
            sect.mon, 
            sect.tue, 
            sect.wed, 
            sect.thu, 
            sect.fri
        ) 
        for sect in sects
    ]
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
        d['cNumbers'] = []
        fullTimes.append(d)
    for time in fullTimes:
        for sect in sects:
            if (sect.tStart == time['tStart'] and sect.tEnd == time['tEnd'] and sect.getDaysArray() == time['days']):
                time['count'] += 1
                if sect.cID not in time['cID']:
                    time['cID'].append(sect.cID)
                if sect.crn not in time['crn']:
                    time['crn'].append(sect.crn)
                if sect.sectFor.cNumber not in time['cNumbers']:
                   time['cNumbers'].append(sect.sectFor.cNumber)
    for time in fullTimes:
        time['tStart'] = time['tStart'].hour * 100 + time['tStart'].minute
        time['tEnd'] = time['tEnd'].hour * 100 + time['tEnd'].minute

    return fullTimes

@app.route("/api/getSectionTimesDaysFull", methods=['GET'])
def getSectionTimesDaysFull():
    sects = Section.query.all()
    times = [
        (
            sect.tStart, 
            sect.tEnd, 
            sect.mon, 
            sect.tue, 
            sect.wed, 
            sect.thu, 
            sect.fri, 
            sect.cID, 
            sect.crn
        ) 
        for sect in sects
    ]
    times = set(times)
    fullTimes = processSections(sects)
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

@app.route("/api/getSectionsInfoMinimal/[<string:sCRNs>]", methods=['GET'])
def getSectionsInfoMinimal(sCRNs):
    crns = [int(crn) for crn in sCRNs.split(',')]
    sections = [Section.query.filter(Section.crn == crn).first() for crn in crns]

    response = []
    for sect in sections:
        response.append(
            {
                'cID': sect.cID,
                'crn': sect.crn,
                'sec': sect.sec,
                'dCode': sect.sectFor.department.code,
                'cNumber': sect.sectFor.cNumber,
                'cName': sect.sectFor.name,
                'shortName': sect.sectFor.getShortName()
            }
        )
    return jsonify(response)
@app.route("/api/getSectionInfo/<string:sCRN>", methods=['GET'])
def getSectionInfo(sCRN):
    return jsonify(Section.query.filter(Section.crn == sCRN).first().serialize())
    
@app.route("/api/getSectionsByDepartment/dpID=<int:dpID>&noOverlaps=<string:noOverlaps>&showCanTake=<string:showCanTake>&hideCompleted=<string:hideCompleted>&hideCurrent=<string:hideCurrent>", methods=['GET'])
def getSectionsByDepartment(dpID, noOverlaps, showCanTake, hideCompleted, hideCurrent):
    deptClassList = Department.query.filter(Department.dpID == dpID).first().classesMember
    allSects = [Section.query.filter(Section.sectFor == c).all() for c in deptClassList]
    sects = []
    for sublist in allSects:
        if type(sublist) == list:
            for s in sublist:
                sects.append(s)
        else:
            sects.append(sublist)
    filterSection(sects, strToBool(noOverlaps), strToBool(showCanTake), strToBool(hideCompleted), strToBool(hideCurrent))
    fullTimes = processSections(sects)
    return jsonify(fullTimes)

@app.route("/api/searchForSections", methods=['POST'])
def searchForSections():
    json = request.get_json()
    query = json['query']

    # match query to section CRN or instructor
    sects = Section.query.filter(Section.crn.like(query)).all()

    # match query to classes cNumber or name
    if not sects:
        classes = Classes.query.filter((Classes.name.like(f'%{query}%') | Classes.cNumber.like(query))).all()

        if classes:
            sects = []
            for c in classes:
                for sect in c.sections:
                    sects.append(sect)
    if sects:
        sections = processSections(sects)
        return jsonify(sections)
    else: 
        return jsonify([])

