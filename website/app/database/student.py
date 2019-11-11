from app import db, loginManager
from app.database.models import BaseTable, student_cur_enroll, serializeRelation, asc_student_classes_taken
from app.database.section import Section
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
    
    def getClassesTaken(self):
        return [s.classTaken for s in self.classesTaken]

    def hasTaken(self, cla):
        if not cla.lab:
            return cla in self.getClassesTaken()
        else:
            return cla.linkedTo in self.getClassesTaken()

    def passed(self, classTaken):
        if classTaken in self.getClassesTaken():
            entry = [e for e in self.classesTaken if e.classTaken == classTaken][0]
            return entry.passed
        else:
            return False

    def enroll(self, section):
        self.classesEnrolled.append(section)
        section.numCurEnrolled += 1
        db.session.commit()
        return 'Successfully enrolled student in section!'

    def unenroll(self, section):
        self.classesEnrolled.remove(section)
        if section.sectFor.hasLinkedClass():
            lID = section.sectFor.getLinkedClass().cID
            sects = Section.query.filter(Section.cID == lID)
            link = [sec for sec in sects if sec in self.classesEnrolled]
            if len(link) == 1:
                link = link[0]
            self.classesEnrolled.remove(link)
            link.numCurEnrolled -= 1
        section.numCurEnrolled -= 1
        db.session.commit()
        reply = 'Successfully unregistered student for section'
        return reply

    def completeCurrent(self):
        for sect in self.classesEnrolled:
            cla = sect.sectFor
            if cla.lab:
                continue
            completedClass = asc_student_classes_taken()
            completedClass.classTaken = cla
            completedClass.grade = 'A'
            completedClass.passed = True
            self.classesTaken.append(completedClass)

        for sect in self.classesEnrolled:   
            sect.numCurEnrolled -= 1
        self.classesEnrolled.clear()
        db.session.commit()

    def __repr__(self):
        return f"Student('{self.fname + ' ' + self.lname}', id={self.sID})"
