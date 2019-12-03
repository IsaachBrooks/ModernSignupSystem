from app import db
from app.database.models import BaseTable, classes_prereq, classes_coreq, classes_linked, serializeRelation
from app.database.department import Department

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
        shortName = f"{self.department.code}{self.cNumber}"
        return shortName

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
            'dCode': self.department.code,
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
