from app import db
from app.database.models import BaseTable

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