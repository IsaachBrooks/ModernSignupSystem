from app import db, loginManager
from app.database.models import BaseTable, student_cur_enroll
from flask_login import UserMixin


@loginManager.user_loader
def loadUser(user_id):
    return Student.query.get(int(user_id))
    
class Student(BaseTable, UserMixin):
    sID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(30), nullable=False)
    mname = db.Column(db.String(30))
    lname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    degreeID = db.Column(db.Integer, db.ForeignKey('degree.degreeID'))
    gpa = db.Column(db.Float, nullable=False, default=0.0)
    classesTaken = db.relationship('asc_student_classes_taken', back_populates='student', lazy=True)
    classesEnrolled = db.relationship('Section', secondary=student_cur_enroll, backref='students', lazy=True)

    def get_id(self):
        return self.sID

    def signUpFor(self, sect):
        return sect.enroll(self)

    def completeClass(self, cl):
        #TODO:
        #Remove section of class from currently enrolled
        #add class to classesTaken
        pass

    def updateGPA(self):
        #TODO:
        #updateGPA based off classes taken grades/credit hrs
        pass

    def serialize(self):
        return {
            'sID' : self.sID,
            'fname' : self.fname,
            'mname' : self.mname,
            'lname' : self.lname,
            'username' : self.username,
            'email' : self.email,
            'degreeID' : self.degreeID,
            'gpa' : self.gpa,
            'classesTaken' : serializeRelation(self.classesTaken),
            'classesEnrolled' : serializeRelation(self.classesEnrolled)
        }
    

    def __repr__(self):
        return f"Student('{self.fname + ' ' + self.lname}', id={self.sID})"
