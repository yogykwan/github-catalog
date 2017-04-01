from flask import render_template, request, redirect, url_for

from utils import app, session
from models import Category, Item


@app.route('/catalog/<int:category_id>/newitem/', methods=['GET', 'POST'])
def new_item(category_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template('newitem.html', category=category)
    elif request.method == 'POST':
        category = session.query(Category).filter_by(id=category_id).one()
        name = request.form['name']
        highlight = request.form['highlight']
        url = request.form['url']
        if name and url:
            user_id = 1  # fake
            item = Item(name=name, highlight=highlight, url=url, user_id=user_id, category_id=category_id)
            session.add(item)
            session.commit()
            return redirect(url_for('show_item', category_id=category_id, item_id=item.id))
        else:
            error = "Complete info please!"
            return render_template('newitem.html', category=category, name=name, highlight=highlight, url=url,
                                   error=error)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/edititem/', methods=['GET', 'POST'])
def edit_item(category_id, item_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id=category_id).one()
        item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
        return render_template('edititem.html', category=category, item=item, name=item.name, highlight=item.highlight,
                               url=item.url)
    elif request.method == 'POST':
        category = session.query(Category).filter_by(id=category_id).one()
        item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
        name = request.form['name']
        highlight = request.form['highlight']
        url = request.form['url']
        if name and url:
            item.name = name
            item.highlight = highlight
            item.url = url
            session.commit()
            return redirect(url_for('show_item', category_id=category_id, item_id=item.id))
        else:
            error = "Complete info please!"
            return render_template('edititem.html', category=category, item=item, name=name, highlight=highlight,
                                   url=url, error=error)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/deleteitem/', methods=['GET', 'POST'])
def delete_item(category_id, item_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id=category_id).one()
        item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
        return render_template('deleteitem.html', category=category, item=item)
    elif request.method == 'POST':
        item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
        session.delete(item)
        session.commit()
        return redirect(url_for('show_items', category_id=category_id))


@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def show_item(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
    return render_template('showitem.html', category=category, item=item)
