from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bc
from app.database.student import Student
from app.database.degree import Degree
from app.database.classes import Classes
from app.database.section import Section
from app.database.department import Department
from app.Scripts.validator import verifyCanEnroll 
from flask_login import current_user

@app.route("/api/getClassInfo/cid=<int:cID>", methods=['GET'])
def getClassInfo(cID):
    singleClass = Classes.query.filter(Classes.cID == cID).first()
    if singleClass:
        return jsonify(singleClass.serialize())

@app.route("/api/getClassInfoMinimal/cid=<int:cID>", methods=['GET'])
def getClassInfoMinimal(cID):
    singleClass = Classes.query.filter(Classes.cID == cID).first()
    ret = {
        'name' : singleClass.name,
        'cNumber' : singleClass.cNumber,
        'deptCode' : singleClass.department.code
    }
    return jsonify(ret)

@app.route("/api/getClassesByDepartment/dpID=<int:dpID>", methods=['GET'])
def getClassesByDepartmentMinimal(dpID):
    dp = Department.query.filter(Department.dpID == dpID).first()
    classesMember = dp.classesMember
    classList = []
    for cla in classesMember:
        if not cla.lab:
            classList.append({
                'cID': cla.cID,
                'cNum': cla.cNumber,
                'name': cla.name,
                'shortName': cla.getShortName()
            })
    
    return jsonify(classList)