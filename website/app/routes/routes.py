from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bc
from app.database.student import Student
from app.forms.forms import RegistrationForm, LoginForm
from app.Scripts.databaseAdd import registerStudent
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/", methods=['GET','POST'])
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('signup'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).first()
        if student and bc.check_password_hash(student.password, form.password.data):
            login_user(student)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('signup'))
        else:
            flash('Bad login. Check username and/or password.', 'danger')
    return render_template('login.html', title='Login', form=form, debug=app.debug)

@app.route("/main")
@app.route("/classSignup")
@login_required
def signup():
    return render_template('classSignup.html', title='Registration', debug=app.debug)

@app.route("/degree")
@login_required
def degree():
    return render_template('degreeViewer.html', title='Degree', debug=app.debug)

@app.route("/hiddenRegister", methods=['GET', 'POST'])
def hiddenRegister():
    if current_user.is_authenticated:
        return redirect(url_for('signup'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = registerStudent(form)
        flash(f'Registered {form.firstName.data} {form.lastName.data} with username {username}. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('secretRegister.html', title='Hidden Register', form=form, debug=app.debug)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/testing", methods=['GET', 'POST'])
def testing():
    return render_template('testing.html', title='Testing page')
    