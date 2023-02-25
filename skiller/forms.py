from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, RadioField, DateTimeLocalField
from wtforms.validators import DataRequired,Email,Length,EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed

class JoinForm(FlaskForm):
    email = StringField('Your Email:',validators=[Email(message="Hello, please enter a valid email"), DataRequired(message="your email address is needed in order to join")])
    password = PasswordField('password:', validators=[DataRequired(Length(min=6,message='your passowrod must be at least 6 digits'))])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='kindly re-enter password to match')])
    gender = RadioField('Gender:',validators=[DataRequired('Kindly select your gender to proceed')])
    submit = SubmitField('Join')