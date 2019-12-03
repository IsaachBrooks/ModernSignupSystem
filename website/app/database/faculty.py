from app import db
from app.database.models import BaseTable

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
        