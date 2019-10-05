from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z]+$', message='Contains non-alpha characters or whitespace')
        ])
    middleName = StringField('Middle Name', validators=[
        Regexp(r'^[a-zA-Z]*$', message='Contains non-alpha characters or whitespace')
        ])
    lastName = StringField('Last Name', validators=[
        DataRequired(),
         Regexp(r'^[a-zA-Z]+$', message='Contains non-alpha characters or whitespace')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')])

    submit = SubmitField('Secret Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log in')
    
