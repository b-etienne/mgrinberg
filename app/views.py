# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 17:13:37 2017

@author: betienne
"""
from datetime import datetime

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, EditForm, SignUpForm
from .models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    # auth = g.user.is_authenticated
    return(render_template('index.html', user=user))
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if g.user is not None and g.user.is_authenticated:
		return(redirect(url_for('index')))

	form = SignUpForm()
	if form.validate_on_submit():
		pseudo = form.name.data
		email = form.mail.data
		if User.pseudo_exists(pseudo):
			flash('This pseudo is already taken')
			return(render_template('signup.html', title='Sign up', form=form))
		user = User(pseudo=pseudo, email=email)
		db.session.add(user)
		db.session.commit()		
		login_user(user)
		flash('Profile created with success')
		return(redirect(url_for('index')))
	return(render_template('signup.html', title='Sign up', form=form))
	

# Taken from https://flask-login.readthedocs.io/en/latest/
@app.route('/login', methods=['GET', 'POST'])
def login():
	# Redirects to index if user is already logged in
    if g.user is not None and g.user.is_authenticated:
        return(redirect(url_for('index')))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(pseudo=form.name.data).first()
        if user is not None:
            login_user(user)
            flash('Logged in successfully.')
            # next_ = request.args.get('next')
        	# is_safe_url should check if the url is safe for redirects.
        	# See http://flask.pocoo.org/snippets/62/ for an example.
        	# if not is_safe_url(next):
         #    	return flask.abort(400)
            return(redirect(url_for('index')))
    return(render_template('login.html', title='Sign in', form=form))


@app.route('/edit', methods=['GET','POST'])
@login_required
def edit():
	form = EditForm()
	if form.validate_on_submit():
		g.user.pseudo = form.pseudo.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved')
		return(redirect(url_for('userprofile', nickname=g.user.pseudo)))
	else:
		form.pseudo.data = g.user.pseudo
		form.about_me.data = g.user.about_me
		return(render_template('edit.html', form=form))


@lm.user_loader
def load_user(id):
    return(User.query.get(int(id)))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
    	g.user.last_seen = datetime.utcnow()
    	db.session.add(g.user)
    	db.session.commit()	


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def userprofile(nickname):
    user = User.query.filter_by(pseudo=nickname).first()
    if user is None:
        flash('User {} not found'.format(nickname))
        return(redirect(url_for('index')))
        
    posts = [{'author' : user, 'body' : 'Premier message du jour 1'},
             {'author' : user, 'body' : 'Second message du jour 2'}]
    return(render_template('user.html', user=user, posts=posts))


@app.errorhandler(404)
def not_found_error(error):
	return(render_template('404.html'), 404)


@app.errorhandler(500)
def internal_error(error):
	db.session.rollback
	return(render_template('500.html'), 500)

