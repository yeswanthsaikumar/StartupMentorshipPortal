from flask_wtf import FlaskForm
from wtforms import PasswordField , SubmitField , TextField , BooleanField , TextAreaField
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


class EditProfileForm(FlaskForm):
	username = TextField('Username' , validators=[DataRequired()])
	about_me = TextAreaField('About_me' , validators=[Length(min=0 , max=200)])
	submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Submit')




