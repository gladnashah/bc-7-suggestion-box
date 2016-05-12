from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User
from flask.ext.bootstrap import Bootstrap
from flask.ext.pagedown.fields import PageDownField


class LoginForm(Form):
	email = StringField('Email', validators=[Required(),Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('keep me logged in')
	submit = SubmitField('Log In')

class RegistrationForm(Form):
	email = StringField('Email', validators=[Required(),Email()])

	username = StringField('Username', validators=[Required()])

	password = PasswordField('Password', validators=[
		Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password')
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

class PostForm(Form):
	title = PageDownField('Your suggestion title here', validators=[Required()])
	body = PageDownField("What's your suggestion?", validators=[Required()])
	submit = SubmitField('Submit')

