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

class Student(BaseTable, UserMixin):
    sID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(30), nullable=False)
    mname = db.Column(db.String(30))
    lname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    dID = db.Column(db.Integer, db.ForeignKey('degree.dID'))
    gpa = db.Column(db.Float, nullable=False, default=0.0)

    def get_id(self):
        return self.sID

    def __repr__(self):
        return f"Student '{self.fname} {self.lname}', id={self.sID}"

class Classes(BaseTable):
    cID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dpID = db.Column(db.Integer, db.ForeignKey('department.dpID'))
    cNumber = db.Column(db.Integer, nullable=False)
    sections = db.relationship('Section', backref='sectFor', lazy=True)
    description = db.Column(db.String(1000), nullable=False, default='')

    def __repr__(self):
        return f"cID={self.cID} dpID={self.dpID} cNumber={self.cNumber}"

class Section(BaseTable):
    crn = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instructorfname = db.Column(db.String(50), nullable=False)
    instructormname = db.Column(db.String(50))
    instructorlname = db.Column(db.String(50), nullable=False)
    cID = db.Column(db.Integer, db.ForeignKey('classes.cID'), nullable=False)
    days = db.Column(db.String(5), nullable=False, default='MTWRF')
    tStart = db.Column(db.Time, nullable=False, default=datetime.now().time())
    tEnd = db.Column(db.Time, nullable=False, default=datetime.now().time())
    dateStart = db.Column(db.Date, nullable=False, default=datetime.now().date())
    dateEnd = db.Column(db.Date, nullable=False, default=datetime.now().date())

    def __repr__(self):
        return f"crn={self.crn} sectFor={self.sectFor}"

class Degree(BaseTable):
    dID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dpID = db.Column(db.Integer, db.ForeignKey('department.dpID'))
    name = db.Column(db.String(100), nullable=False)
    totalHours = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(1000), nullable=False, default='')
    students = db.relationship('Student', backref='enrolledDegree', lazy=True)

    def __repr__(self):
        return f"dID={self.dID} name={self.name}"

class Department(BaseTable):
    dpID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(4), nullable=False)

    def __repr__(self):
        return f"dpID={self.dpID} name={self.name} code={self.code}"

class StudentClasses(BaseTable):
    cID = db.Column(db.Integer, db.ForeignKey('classes.cID'), primary_key=True)
    sID = db.Column(db.Integer, db.ForeignKey('student.sID'), primary_key=True)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    passed = db.Column(db.Boolean, nullable=False, default=False)
    grade = db.Column(db.String(1), nullable=False, default='F')

    def __repr__(self):
        return f"sID={self.sID} classID={cID} complete={self.complete} grade={self.grade}"

class StudentCurEnroll(BaseTable):
    sID = db.Column(db.Integer, db.ForeignKey('student.sID'), primary_key=True)
    sectcrn = db.Column(db.Integer, db.ForeignKey('section.crn'), primary_key=True)

    def __repr__(self):
        return f"sID={self.sID} sectcrn={self.sectcrn}"

class DegreeClasses(BaseTable):
    dID = db.Column(db.Integer, db.ForeignKey('degree.dID'), primary_key=True)
    cID = db.Column(db.Integer, db.ForeignKey('classes.cID'), primary_key=True)

    def __repr__(self):
        return f"dID={self.dID} classID={self.cID}"