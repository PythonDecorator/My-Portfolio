from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from flask_ckeditor import CKEditorField
from wtforms.widgets import TextArea
from wtforms.validators import Length, Email, DataRequired, URL


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Sign-In")


class CreateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Sign-Up")


class ContactUsForm(FlaskForm):
    name = StringField('Name', [DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', [DataRequired(), Email()])
    message = StringField(label='Message', widget=TextArea(), validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Send Message")


class AddPortfolioForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=64)])
    category = StringField('Category', [DataRequired(), Length(max=64)])
    img_url = StringField('Image URL', validators=[DataRequired()])
    github_url = StringField('GitHub Repository URL', validators=[DataRequired(), URL()])
    client = StringField('Client', validators=[DataRequired()])
    date = StringField('Date Released', validators=[DataRequired(), Length(max=20)])
    final_project = StringField('Final Project', validators=[DataRequired()])
    download = StringField('Download', validators=[DataRequired()])
    body = CKEditorField("Project Description")
    submit = SubmitField("Submit")
