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

@app.route("/api/getDepartmentNamesIDs", methods=['GET'])
def getDepartmentNamesIDs():
    deps = Department.query.all()
    ret = []
    for dep in deps:
        ret.append({'name': dep.name, 'dpID': dep.dpID})
    return jsonify(ret)


"""
@app.route("/api/", methods=[''])
def api():
    result = {}
    return jsonify(result)

@app.route("/api/", methods=[''])
def api():
    result = {}
    return jsonify(result)

@app.route("/api/", methods=[''])
def api():
    result = {}
    return jsonify(result)
"""

