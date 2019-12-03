from app import db
from app.database.models import BaseTable,asc_degree_classes
from app.database.classes import Classes

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
        