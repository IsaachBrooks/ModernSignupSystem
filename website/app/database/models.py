from datetime import datetime
from app import db, loginManager
from flask_login import UserMixin

def serializeRelation(relation):
        return [item.serialize() for item in relation]


class BaseTable(db.Model):
    __abstract__ = True
    
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

student_cur_enroll = db.Table('student_cur_enroll',
    db.Column('sID', db.Integer, db.ForeignKey('student.sID'), primary_key=True),
    db.Column('sectcrn', db.Integer, db.ForeignKey('section.crn'), primary_key=True))

classes_prereq = db.Table('classes_prereq',
    db.Column('prereqCID', db.Integer, db.ForeignKey('classes.cID'), primary_key=True),
    db.Column('forClassCID', db.Integer, db.ForeignKey('classes.cID'), primary_key=True))

classes_coreq = db.Table('classes_coreq',
    db.Column('coreqCID', db.Integer, db.ForeignKey('classes.cID'), primary_key=True),
    db.Column('forClassCID', db.Integer, db.ForeignKey('classes.cID'), primary_key=True))

classes_linked = db.Table('classes_linked',
    db.Column('linkID', db.Integer, db.ForeignKey('classes.cID'), primary_key=True),
    db.Column('linkedToID', db.Integer, db.ForeignKey('classes.cID'), primary_key=True))

class asc_student_classes_taken(BaseTable):
    __tablename = 'asc_student_classes'
    cID = db.Column(db.Integer, db.ForeignKey('classes.cID'), primary_key=True)
    sID = db.Column(db.Integer, db.ForeignKey('student.sID'), primary_key=True)
    student = db.relationship('Student', back_populates='classesTaken')
    classTaken = db.relationship('Classes')
    passed = db.Column(db.Boolean, nullable=False, default=False)
    grade = db.Column(db.String(1), nullable=False, default='F')

    def serialize(self):
        return {
            'classTaken' : self.classTaken.serialize(),
            'passed' : self.passed,
            'grade' : self.grade,
        }
    
    def __repr__(self):
        return f"ClassTaken(class={self.classTaken.getShortName()} passed={self.passed} grade={self.grade})"

class asc_degree_classes(BaseTable):
    degreeID = db.Column(db.Integer, db.ForeignKey('degree.degreeID'), primary_key=True)
    cID = db.Column(db.Integer, db.ForeignKey('classes.cID'), primary_key=True)
    degree = db.relationship('Degree', back_populates='dClasses')
    dClass = db.relationship('Classes', backref='degree')
    priority = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('priority', 'degreeID', name='UniquePriorityInDegree'),)

    def serializeForClasses(self):
        return {
            'degree' : self.degree.degreeID,
            'priority' : self.priority
        }
    
    def serializeForDegree(self):
        return {
            'dClass' : self.dClass.serialize(),
            'priority' : self.priority
        }

    def __repr__(self):
        return f"DegreeClass(degree={self.degree} class={self.dClass.getShortName()} cID={self.cID} priority={self.priority})"
