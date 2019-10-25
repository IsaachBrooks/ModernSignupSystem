from app import db, bc
from app.database.student import Student

def registerStudent(form):
    hashed_password = bc.generate_password_hash(form.password.data).decode('utf-8')
    username = (form.lastName.data + form.firstName.data[0] + (form.middleName.data[0] if len(form.middleName.data) > 0 else '')).lower()
    sListLen = len(db.session.query(Student).filter(Student.username.like(username + '%')).all())
    if sListLen > 0: username = username + str(sListLen + (1 if sListLen != 1 else 0))
    email = username+'@notapp.edu'
    student = Student(
        fname=form.firstName.data,
        mname=form.middleName.data,
        lname=form.lastName.data,
        username=username,
        email=email,
        password=hashed_password
    )
    db.session.add(student)
    db.session.commit()
    return username