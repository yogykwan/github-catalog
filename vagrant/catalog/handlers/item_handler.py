from flask import request, redirect, url_for
from flask import session as login_session

from utils import app, session, render, user_logged_in, category_exists, item_exists, user_owns_item, valid_item
from models import Item


@app.route('/catalog/<int:category_id>/newitem/', methods=['GET', 'POST'])
@user_logged_in
@category_exists
def new_item(category):
    if request.method == 'GET':
        return render('newitem.html', category=category)
    elif request.method == 'POST':
        name = request.form['name']
        highlight = request.form['highlight']
        url = request.form['url']
        if valid_item(name, url, highlight):
            user_id = login_session['user_id']
            item = Item(name=name, highlight=highlight, url=url, user_id=user_id, category_id=category.id)
            session.add(item)
            session.commit()
            return redirect(url_for('show_item', category_id=category.id, item_id=item.id))
        else:
            error = "Complete info please!"
            return render('newitem.html', category=category, name=name, highlight=highlight, url=url,
                          error=error)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/edititem/', methods=['GET', 'POST'])
@user_logged_in
@item_exists
@user_owns_item
def edit_item(category, item):
    if request.method == 'GET':
        return render('edititem.html', category=category, item=item, name=item.name, highlight=item.highlight,
                      url=item.url)
    elif request.method == 'POST':
        name = request.form['name']
        highlight = request.form['highlight']
        url = request.form['url']
        if valid_item(name, url, highlight):
            item.name = name
            item.highlight = highlight
            item.url = url
            session.commit()
            return redirect(url_for('show_item', category_id=category.id, item_id=item.id))
        else:
            error = "Complete info please!"
            return render('edititem.html', category=category, item=item, name=name, highlight=highlight,
                          url=url, error=error)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/deleteitem/', methods=['GET', 'POST'])
@user_logged_in
@item_exists
@user_owns_item
def delete_item(category, item):
    if request.method == 'GET':
        return render('deleteitem.html', category=category, item=item)
    elif request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('show_items', category_id=category.id))


@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
@item_exists
def show_item(category, item):
    return render('showitem.html', category=category, item=item)
