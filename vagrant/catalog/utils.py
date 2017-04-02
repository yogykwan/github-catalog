from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template
from flask.ext.github import GitHub
from flask import session as login_session
from flask import redirect
import os
from functools import wraps

from models import *


# db session

def init_database():
    engine = create_engine('sqlite:///githubcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


# flask app

def init_app():
    app = Flask(__name__)
    app.secret_key = 'http://Jennica.Space'

    if os.environ.has_key('GITHUB_CLIENT_ID') and os.environ.has_key('GITHUB_CLIENT_SECRET'):
        app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
        app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']
    else:
        app.config['GITHUB_CLIENT_ID'] = None
        app.config['GITHUB_CLIENT_SECRET'] = None

    return app


session = init_database()
app = init_app()
github = GitHub(app)


# render html with user_id

def render(template, **kw):
    if 'user_id' in login_session:
        kw['user_id'] = login_session['user_id']
    return render_template(template, **kw)


# validation decorators

def user_logged_in(function):
    @wraps(function)
    def wrapper(**kw):
        if 'user_id' in login_session:
            return function(**kw)
        else:
            return redirect('/login/')

    return wrapper


@app.errorhandler(404)
def not_found(error):
    return error404()


@app.errorhandler(401)
def unauthorized(error):
    return error401()


def error404():
    return render_template('404.html'), 404


def error401():
    return render_template('401.html'), 401


def category_exists(function):
    @wraps(function)
    def wrapper(category_id):
        category = session.query(Category).filter_by(id=category_id).first()
        if category:
            return function(category)
        else:
            return error404()

    return wrapper


def item_exists(function):
    @wraps(function)
    def wrapper(category_id, item_id):
        category = session.query(Category).filter_by(id=category_id).first()
        item = session.query(Item).filter_by(category_id=category_id, id=item_id).first()
        if category:
            return function(category, item)
        else:
            return error404()

    return wrapper


def user_owns_category(function):
    @wraps(function)
    def wrapper(category):
        if category.user_id == login_session['user_id']:
            return function(category)
        else:
            return error401()

    return wrapper


def user_owns_item(function):
    @wraps(function)
    def wrapper(category, item):
        if item.user_id == login_session['user_id'] or category.user_id == login_session['user_id']:
            return function(category, item)
        else:
            return error401()

    return wrapper


# valid form

def valid_category(name, description):
    if name:
        return True
    else:
        return False


def valid_item(name, url, highlight):
    if name and url:
        return True
    else:
        return False
