from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, RadioField, DateTimeLocalField
from wtforms.validators import DataRequired,Email,Length,EqualTo,Regexp,ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
 
class JoinForm(FlaskForm):
    fullname = StringField('fullname', validators=[DataRequired(),Length(min=5,max=100,message='Make sure that your fullname is well captured'), Regexp("^[A-Za-z][-]*",0,'Your fullname must contain only letters and can only allow - as a special character')], render_kw={'placeholder': "Enter your full name"})

    email = StringField('email',validators=[ DataRequired(),Email(message="your email address is needed in order to join")], render_kw={'placeholder': "Enter your email address"})
 
    password = PasswordField('password', validators=[DataRequired(),Length(min=6,max=15,message='your passwrod must be at least 6 digits'),Regexp("^[A-Za-z][A-Za-z0-9.]*",0,'Your password must contain an upper case, lower case and a number')], render_kw={'placeholder': "Enter your password"})

    confirm_password = PasswordField('confirm_password', validators=[DataRequired(),Length(min=6,max=15)], render_kw={'placeholder': "confirm your password"})
    EqualTo('password',message='The passwords must match')


    gender = StringField('gender',validators=[DataRequired('Please select your gender to proceed')])
    submit = SubmitField('Join')

    def validate_email(self,email):
        user_email = Users.query.filter_by(user_email=email.data).first()
        if user_email:
            raise ValidationError('An account is already eisting with this email, please choose a different email')