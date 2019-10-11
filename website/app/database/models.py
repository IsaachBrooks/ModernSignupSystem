from datetime import datetime
from app import db, loginManager
from flask_login import UserMixin


@loginManager.user_loader
def loadUser(user_id):
    return Student.query.get(int(user_id))

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
    classTaken = db.relationship('Classes')#, back_populates='studentsTaken')
    passed = db.Column(db.Boolean, nullable=False, default=False)
    grade = db.Column(db.String(1), nullable=False, default='F')

    def __repr__(self):
        return f"ClassTaken({self.classTaken.getShortName()} passed={self.passed} grade={self.grade})"

class asc_degree_classes(BaseTable):
    degreeID = db.Column(db.Integer, db.ForeignKey('degree.degreeID'), primary_key=True)
    cID = db.Column(db.Integer, db.ForeignKey('classes.cID'), primary_key=True)
    priority = db.Column(db.Integer, nullable=False, default=0, autoincrement=True)
    __table_args__ = (db.UniqueConstraint('priority', 'degreeID', name='UniquePriorityInDegree'),)

    def __repr__(self):
        return f"DegreeClass(degreeID={self.degreeID} cID={self.cID} priority={self.priority})"



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
    #classesTaken = db.relationship('Classes', secondary='asc_student_classes', lazy=True)
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

    def __repr__(self):
        return f"Student('{self.fname + ' ' + self.lname}', id={self.sID})"

class Faculty(BaseTable):
    fID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    mname = db.Column(db.String(50), default='')
    lname = db.Column(db.String(50), nullable=False)
    dpID = db.Column(db.Integer, db.ForeignKey('department.dpID'))
    sections = db.relationship('Section', backref='instructor', lazy=True)

    def __repr__(self):
        return f"Faculty('{self.fname + ' ' + self.lname}', id={self.fID})"

class Classes(BaseTable):
    cID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dpID = db.Column(db.Integer, db.ForeignKey('department.dpID'))
    degreeID = db.Column(db.Integer, db.ForeignKey('degree.degreeID'))
    cNumber = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    sections = db.relationship('Section', backref='sectFor', lazy=True)
    description = db.Column(db.String(1000), nullable=False, default='')
    creditHours = db.Column(db.Integer, nullable=False, default=0)
    prereqs = db.relationship('Classes', secondary=classes_prereq, 
                            primaryjoin="classes.c.cID==classes_prereq.c.prereqCID",
                            secondaryjoin="classes.c.cID==classes_prereq.c.forClassCID",
                            backref='prereqFor', lazy=True)
    coreqs = db.relationship('Classes', secondary=classes_coreq, 
                            primaryjoin="classes.c.cID==classes_coreq.c.coreqCID",
                            secondaryjoin="classes.c.cID==classes_coreq.c.forClassCID",
                            backref='coreqFor', lazy=True)
    linkedClass = db.relationship('Classes', secondary=classes_linked, 
                            primaryjoin="classes.c.cID==classes_linked.c.linkID",
                            secondaryjoin="classes.c.cID==classes_linked.c.linkedToID",
                            uselist=False,
                            backref=db.backref('linkedTo', uselist=False), lazy=True)
    #studentsTaken = db.relationship('asc_student_classes_taken', back_populates='classTaken', lazy=True)

    def getShortName(self):
        return f"{self.department.code}{self.cNumber}"

    def hasLinkedClass(self):
        return bool(self.linkedClass) or bool(self.linkedTo)
    
    def getLinkedClass(self):
        if hasLinkedClass(self):
            return self.linkedClass if self.linkedClass else self.linkedTo
        return None

    def __repr__(self):
        return f"Classes(cID={self.cID} depCode={self.department.code} cNumber={self.cNumber} name='{self.name}')"

class Section(BaseTable):
    crn = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    cID = db.Column(db.Integer, db.ForeignKey('classes.cID'), nullable=False)
    iID = db.Column(db.Integer, db.ForeignKey('faculty.fID'))
    mon = db.Column(db.Boolean, nullable=False, default=False)
    tue = db.Column(db.Boolean, nullable=False, default=False)
    wed = db.Column(db.Boolean, nullable=False, default=False)
    thu = db.Column(db.Boolean, nullable=False, default=False)
    fri = db.Column(db.Boolean, nullable=False, default=False)
    tStart = db.Column(db.Time, nullable=False, default=datetime.now().time())
    tEnd = db.Column(db.Time, nullable=False, default=datetime.now().time())
    dateStart = db.Column(db.Date, nullable=False, default=datetime.now().date())
    dateEnd = db.Column(db.Date, nullable=False, default=datetime.now().date())
    capacity = db.Column(db.Integer, nullable=False, default=30)
    numCurEnrolled = db.Column(db.Integer, nullable=False, default=0)

    def getDayString(self):
        days = ''
        days += 'M' if self.mon else ''
        days += 'T' if self.tue else ''
        days += 'W' if self.wed else ''
        days += 'R' if self.thu else ''
        days += 'F' if self.fri else ''
        return days

    def getDaysArray(self):
        return [mon, tue, wed, thu, fri]

    def overlapsWith(self, sect):
        if self.overlapsDaysWith(sect):
            return self.overlapsTimesWith(sect)
        else:
            return False

    def overlapsDaysWith(self, sect):
        #TODO:
        #check if two lists of days overlap
        pass
    
    def overlapsTimesWith(self, sect):
        #TODO:
        #check if two sections times overlap
        pass

    def enroll(self, student):
        #TODO:
        #Check student current schulde, compare against section times/days
        #Check student credit hours
        #check self.capacity > self.numCurEnrolled
        pass

    def __repr__(self):
        return f"Section(crn={self.crn} sectFor={self.sectFor.department.code + str(self.sectFor.cNumber)} days={self.getDayString()} time={self.tStart} - {self.tEnd})"

class Degree(BaseTable):
    degreeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dpID = db.Column(db.Integer, db.ForeignKey('department.dpID'))
    name = db.Column(db.String(100), nullable=False)
    totalHours = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(1000), nullable=False, default='')
    students = db.relationship('Student', backref='enrolledDegree', lazy=True)
    dClasses = db.relationship('Classes', backref='degree', lazy=True)

    def __repr__(self):
        return f"Degree(degreeID={self.degreeID} name='{self.name}')"

class Department(BaseTable):
    dpID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(4), nullable=False)
    classesMember = db.relationship('Classes', backref='department', lazy=True)
    degreeMember = db.relationship('Degree', backref='department', lazy=True)
    facultyMember = db.relationship('Faculty', backref='department', lazy=True)

    def __repr__(self):
        return f"Department(dpID={self.dpID} name='{self.name}' code={self.code})"

