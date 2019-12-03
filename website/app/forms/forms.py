from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z]+$', message='Contains non-alpha characters or whitespace')
        ], render_kw={"placeholder": "First name"})
    middleName = StringField('Middle Name', validators=[
        Regexp(r'^[a-zA-Z]*$', message='Contains non-alpha characters or whitespace')
        ], render_kw={"placeholder": "Middle name or Initial"})
    lastName = StringField('Last Name', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z]+$', message='Contains non-alpha characters or whitespace')], render_kw={"placeholder": "Last name"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    confirmPassword = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')], render_kw={"placeholder": "confirm password"})

    submit = SubmitField('Secret Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "login or email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})

    submit = SubmitField('Sign in')
