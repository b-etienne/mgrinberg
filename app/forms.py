# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 17:00:46 2017

@author: betienne
"""

from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    name = StringField('name', validators=[DataRequired()])
    remember = BooleanField('remember', default=False)


class SignUpForm(Form):
    name = StringField('name', validators=[DataRequired()])
    mail = StringField('mail', validators=[DataRequired()])
    remember = BooleanField('remember', default=False)  
    

class EditForm(Form):
	pseudo = HiddenField('pseudo', validators=[DataRequired()])
	about_me = TextAreaField('about_me', validators=[Length(min=0, max=256)])


class PostForm(Form):
	post = TextAreaField('post', validators = [DataRequired()])
	