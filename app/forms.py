from flask_wtf import FlaskForm
from wtforms import PasswordField , SubmitField , TextField , BooleanField , TextAreaField , SelectField , IntegerField
from wtforms.validators import DataRequired , Email , EqualTo , ValidationError , Length
from app.models import User

class EditProfileForm(FlaskForm):
	username = TextField('Username' , validators=[DataRequired()])
	facebook = TextField('facebook profile' )
	linkedin = TextField('linkedIn profile' )
	twitter = TextField('twitter profile' )
	phone_no = TextField('Phone no' )
	about_me = TextAreaField('About_me' , validators=[Length(min=0 , max=200)])
	submit = SubmitField('Submit')


class PostForm(FlaskForm):
	post = TextAreaField('Say something', validators=[
		DataRequired(), Length(min=1, max=50000000000)])
	submit = SubmitField('Submit')

class StoryForm(FlaskForm):
	story = TextAreaField('summernote', validators=[
		DataRequired(), Length(min=1, max=500000000000)])
	submit = SubmitField('Submit')

class MessageForm(FlaskForm):
	message = TextAreaField('Message', validators=[
		DataRequired(), Length(min=0, max=1400000000)])
	submit = SubmitField('Submit')


