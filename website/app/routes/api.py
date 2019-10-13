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
