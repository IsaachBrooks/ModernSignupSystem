from datetime import datetime
from app import db, loginManager
from flask_login import UserMixin


@loginManager.user_loader
def loadUser(user_id):
    return Student.query.get(int(user_id))

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

class Faculty(BaseTable):
    fID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    mname = db.Column(db.String(50), default='')
    lname = db.Column(db.String(50), nullable=False)
    dpID = db.Column(db.Integer, db.ForeignKey('department.dpID'))
    sections = db.relationship('Section', backref='instructor', lazy=True)

    def serialize(self):
        return {
            'fID' : self.fID,
            'fname' : self.fname,
            'mname' : self.mname,
            'lname' : self.lname,
            'dpID' : self.dpID
        }

    def serializeInstructor(self):
        return {
            'fID' : self.fID,
            'fname' : self.fname,
            'mname' : self.mname,
            'lname' : self.lname,
            'dpID' : self.dpID
        }    
    def __repr__(self):
        return f"Faculty('{self.fname + ' ' + self.lname}', id={self.fID})"

class Classes(BaseTable):
    cID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dpID = db.Column(db.Integer, db.ForeignKey('department.dpID'))
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
    elective = db.Column(db.Boolean, nullable=False, default=False)
    lab = db.Column(db.Boolean, nullable=False, default=False)

    def getShortName(self):
        return f"{self.department.code}{self.cNumber}"

    def hasLinkedClass(self):
        return bool(self.linkedClass) or bool(self.linkedTo)
    
    def getLinkedClass(self):
        if self.hasLinkedClass():
            return self.linkedClass if self.linkedClass else self.linkedTo
        return None

    def addLinkedClass(self, cl):
        if not self.hasLinkedClass():
            self.linkedClass = cl
            db.session.add(self)
            db.session.commit()
            return True
        return False

    def serialize(self):
        return {
            'cID' : self.cID,
            'dpID' : self.dpID,
            'cNumber' : self.cNumber,
            'name' : self.name,
            'degree' : [item.serializeForClasses() for item in self.degree],
           #'sections' : serializeRelation(self.sections),
            'description' : self.description,
            'creditHours' : self.creditHours,
            'prereqs' : serializeRelation(self.prereqs),
            'coreqs' : serializeRelation(self.coreqs),
            'linkedClass' : self.linkedClass.cID if self.linkedClass 
                            else self.linkedTo.cID if self.linkedTo else None,
            'elective' : self.elective,
            'lab' : self.lab
        }

    def __repr__(self):
        return f"Classes(cID={self.cID} shortName={self.getShortName()} name='{self.name}')"

class Section(BaseTable):
    crn = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sec = db.Column(db.Integer)  
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
    __table_args__ = (db.UniqueConstraint('sec', 'cID', name='UniqueSectionClassNumber'),)

    def getDayString(self):
        days = ''
        days += 'M' if self.mon else ''
        days += 'T' if self.tue else ''
        days += 'W' if self.wed else ''
        days += 'R' if self.thu else ''
        days += 'F' if self.fri else ''
        return days

    def getDaysArray(self):
        return [self.mon, self.tue,self. wed, self.thu, self.fri]

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
 
    def serialize(self):
        return {
            'crn' : self.crn,
            'sec' : self.sec,
            'cID' : self.cID,
            'iID' : self.iID,
            'instructor' : self.instructor.serializeInstructor(),
            'mon' : self.mon,
            'tue' : self.tue,
            'wed' : self.wed,
            'thu' : self.thu,
            'fri' : self.fri,
            'days': self.getDayString(),
            'tStart' : self.tStart.strftime('%H:%M:%S'),
            'tEnd' : self.tEnd.strftime('%H:%M:%S'),
            'dateStart' : self.dateStart.strftime('%Y-%m-%d'),
            'dateEnd' : self.dateEnd.strftime('%Y-%m-%d'),
            'capacity' : self.capacity,
            'numCurEnrolled' : self.numCurEnrolled
        }

    def __repr__(self):
        return f"Section(crn={self.crn} sectFor={self.sectFor.department.code + str(self.sectFor.cNumber)} days={self.getDayString()} time={self.tStart} - {self.tEnd})"

class Degree(BaseTable):
    degreeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dpID = db.Column(db.Integer, db.ForeignKey('department.dpID'))
    name = db.Column(db.String(100), nullable=False)
    totalHours = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(1000), nullable=False, default='')
    students = db.relationship('Student', backref='enrolledDegree', lazy=True)
    dClasses = db.relationship('asc_degree_classes', back_populates='degree', lazy=True)

    def addClass(self, cl, priority):
        adc = asc_degree_classes(degree=self, dClass=cl, priority=priority)
        db.session.add(adc)
        db.session.commit()

    def serialize(self):
        return {
            'degreeID' : self.degreeID,
            'dpID' : self.dpID,
            'name' : self.name,
            'totalHours' : self.totalHours,
            'description' : self.description,
           #'students' : serializeRelation(self.students),
            'dClasses' : [item.serializeForDegree() for item in self.dClasses]            
        }

    def __repr__(self):
        return f"Degree(degreeID={self.degreeID} name='{self.name}')"

class Department(BaseTable):
    dpID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(4), nullable=False)
    classesMember = db.relationship('Classes', backref='department', lazy=True)
    degreeMember = db.relationship('Degree', backref='department', lazy=True)
    facultyMember = db.relationship('Faculty', backref='department', lazy=True)

    def serialize(self):
        return {
            'dpID' : self.dpID,
            'name' : self.name,
            'code' : self.code,
            'classesMember' : serializeRelation(self.classesMember),
            'degreeMember' : serializeRelation(self.degreeMember),
            'facultyMember' : serializeRelation(self.facultyMember),
        }

    def __repr__(self):
        return f"Department(dpID={self.dpID} name='{self.name}' code={self.code})"

