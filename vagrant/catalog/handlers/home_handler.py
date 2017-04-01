from flask import render_template, request, redirect, url_for
from flask import session as login_session

from utils import app


@app.route('/')
def show_home():
    return redirect(url_for('show_categories'))
