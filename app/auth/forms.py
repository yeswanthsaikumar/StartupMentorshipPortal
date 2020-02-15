from flask_wtf import FlaskForm
from wtforms import PasswordField , SubmitField , TextField , BooleanField , TextAreaField , SelectField
from wtforms.validators import DataRequired , Email , EqualTo , ValidationError , Length
from app.models import User

class LoginForm(FlaskForm):
	username = TextField('Username' , validators=[DataRequired()] )
	password = PasswordField( 'Password' , validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')



class RegistrationForm(FlaskForm):
	username = TextField('username' , validators=[DataRequired()])
	email = TextField('gmail', validators=[DataRequired() , Email()])
	user_category = SelectField('select who you are' ,choices=[('entreprenuer','entreprenuer') , ('mentor','mentor') , ('investor','investor')])
	password = PasswordField( 'Password', validators=[DataRequired() , EqualTo('password1')])
	password1= PasswordField('Repeat Password' , validators=[DataRequired()])
	submit = SubmitField('Register')

	def validate_username(self , username):
		user = User.query.filter_by(username=username.data).first()

		if user is not None :
			raise ValidationError("Please use a different username")

	def validate_email(self , email):
		user = User.query.filter_by(email=email.data).first()

		if user is not None :
			raise ValidationError("Please use a different email")


class ResetPasswordRequestForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
