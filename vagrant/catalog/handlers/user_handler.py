from flask import request, redirect, url_for, flash
from flask import session as login_session
from flask import make_response
import json
import random
import string

from utils import app, session, github
from models import User


@app.route('/login/')
def login():
    if 'user' in login_session:
        return redirect(url_for('show_home'))
    state = ''.join(random.choice(string.ascii_letters + string.digits) for x in xrange(32))
    login_session['state'] = state
    return github.authorize(state=state, scope='user,repo')


@github.access_token_getter
def get_token():
    return login_session['access_token']


@app.route('/ghcallback/')
@github.authorized_handler
def authorized(oauth_token):
    state = request.args.get('state')
    if state != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = oauth_token

    data = github.get('user')
    email = data['email']
    name = data['name']

    user = session.query(User).filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email)
        session.add(user)
    user.name = name
    session.commit()
    login_session['user_id'] = user.id

    flash("Logged in as %s!" % name)
    return redirect(url_for('show_home'))


@app.route('/logout/')
def logout():
    login_session.pop('user_id', None)
    login_session.pop('access_token', None)
    flash("Logged out!")
    return redirect(url_for('show_home'))
