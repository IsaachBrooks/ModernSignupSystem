from flask import Flask
from flask import render_template
from flask import url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
template_dir = './templates'

app = Flask(__name__, template_folder=template_dir)

app.config.from_object(Config)
app.config['SECRET_KEY'] = 'jidhfisdlfidsf9d900ds90s0kk32009109dll299s9dd9s0a0l2pl3vmbnmv09'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class BaseTable(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Student(BaseTable):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    mname = db.Column(db.String(30))
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Student '{self.fname} {self.lname}', id={self.id}"

class Classes(BaseTable):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(4), primary_key=True)
    sections = db.relationship('Section', backref='sectFor', lazy=True)
    description = db.Column(db.String(1000))
    def __repr__(self):
        return f"{self.department}{self.id}"

class Section(BaseTable):
    id = db.Column(db.Integer, primary_key=True)
    instructor = db.Column(db.String(100))
    classID = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    #days = 
    tStart = db.Column(db.Time)
    tEnd = db.Column(db.Time)
    dateStart = db.column(db.Date)
    dateEnd = db.column(db.Date)

    def __repr__(self):
        return f"Section {self.id} for {self.sectFor}"


class ProgramOfStudy(BaseTable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    totalHours = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000))


from app import routes

