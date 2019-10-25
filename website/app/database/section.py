from app import db
from app.database.models import BaseTable
from app.database.faculty import Faculty
from datetime import datetime

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
