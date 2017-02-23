# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 16:58:46 2017

@author: betienne
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('app/tmp/flaskr.log','a', 1*1024*1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('flaskr startup')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models

