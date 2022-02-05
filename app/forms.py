from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, email_validator

class Register(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired()
        ])
    username = StringField("Username", validators=[
        DataRequired()
    ])
    email = EmailField("Email", validators=[
        DataRequired()
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    submit = SubmitField("Register")

class Login(FlaskForm):
    email = EmailField("Email", validators=[
        DataRequired()
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    submit = SubmitField("Login")

class Socialmidias_url(FlaskForm):
    facebook_url = StringField("Url facebook", validators=[
        
    ])
    linkedin_url = StringField('Url Linkedin', validators=[
        
    ])
    submit = SubmitField("Regsiter SocialMidias")


class DeleteSocialMidias(FlaskForm):
    url = StringField("Url")
    submit = SubmitField("Submit")

class UpdateSocialMidias(FlaskForm):
    new = StringField("New")
    submit = SubmitField("Submit")

class EmailToResetPassword(FlaskForm):
    emailresetpassword = StringField('Email', validators=[
        DataRequired(),
        Email("This field requires a valid email address")
    ])
    submit = SubmitField('Send Email')     