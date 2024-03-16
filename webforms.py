from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

# Create a Search Form
class SearchForm(FlaskForm):
  searched = StringField("Searched", validators=[DataRequired()])
  submit = SubmitField("Submit")

# Create a Login Form
class LoginForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField("Submit")

# Create a Posts Form
class PostForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired()])
  content = CKEditorField('Content', validators=[DataRequired()])
  # content = StringField("Content", widget=TextArea(), validators=[DataRequired()])
  slug = StringField("Slug", validators=[DataRequired()])
  submit = SubmitField("Submit")

# Create a Form Class
class UserForm(FlaskForm):
  username = StringField("Enter Username", validators=[DataRequired()])
  name = StringField("Enter your Name", validators=[DataRequired()])
  email = StringField("Enter your Email", validators=[DataRequired()])
  favorite_color = StringField("Enter Favorite Color")
  about_author = TextAreaField("About Author")
  password_hash = PasswordField('Enter Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must be matched')])
  password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
  profile_pic = FileField("Profile Pic")
  submit = SubmitField("Submit")

# Create a Form Class
class NameForm(FlaskForm):
  name = StringField("What's your name", validators=[DataRequired()])
  submit = SubmitField("Submit")

# Create a PassForm Class
class PasswordForm(FlaskForm):
  email = StringField("What's your email", validators=[DataRequired()])
  password_hash = PasswordField("What's your Password", validators=[DataRequired()])
  submit = SubmitField("Submit")