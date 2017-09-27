# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
	email=StringField(validators=[Required(),Length(1,64),Email()])
	password=PasswordField(validators=[Required()])
	submit=SubmitField()



