from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm

@app.route("/")
@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.username.data == 'brooksih' and form.password.data == 'happycloud'):
            flash('Logged in.','success')
            redirect(url_for('login'))
        else:
            flash('Bad login', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/main")
def signup():
    return render_template('classSignup.html', title='Main')

@app.route("/degree")
def degree():
    return render_template('degreeViewer.html', title='Degree')

@app.route("/hiddenRegister", methods=['GET', 'POST'])
def hiddenRegister():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registered {form.firstName.data} {form.lastName.data}', 'success')
        return redirect(url_for('login'))
    return render_template('secretRegister.html', title='Hidden Register', form=form)
