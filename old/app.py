# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:06:01 2016

@author: betienne
"""

import os
import json
import sqlite3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
                       DATABASE = os.path.join(app.root_path, 'Bucketlist.sqlite'),
                       SECRET_KEY = 'development key',
                       USERNAME = 'admin',
                       PASSWORD = 'default'))

app.config.from_envvar('FLASKR_SETTINGS', silent = True)

#def connect_db():
#    """
#    Connects ti the specific database
#    """
#    conn = sqlite3.connect(app.config['DATABASE'])
#    rv.row_factory = sqlite3.Row
#    return(rv)

conn = sqlite3.connect('Bucketlist.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT * FROM login')


@app.route('/')
@app.route('/index')
def main():
#    return 'Hello World!'
    posts = [
             {'user':'ben1', 'message':'Salut c\'est mon premier message'},
             {'user':'ben2', 'message':'Salut c\'est mon deuxième message message'},
             {'user':'ben3', 'message':'Salut c\'est mon troisième message'},
             {'user':'ben4', 'message':'Salut c\'est mon quatrième message'}
             ]
    return(render_template('index.html', user="Johnny", posts=posts))
    
@app.route('/showSignUp')
def showSignUp():
    return(render_template('signup.html'))
    
@app.route('/signUp', methods=['POST'])
def signUp():
    
    _name = request.form['inputName']
    _mail = request.form['inputEmail']
    _pwd = request.form['inputPassword']

    if _name and _pwd and _mail:
        return(json.dumps({'html':'<span>All fields good !!</span>'}))
    else:
        return(json.dumps({'html':'<span>Please fill in all the fields</span>'}))


if __name__ == '__main__':
    app.run()
    
