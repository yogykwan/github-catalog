from flask import render_template, request, redirect, url_for

from utils import app, session
from models import Category

@app.route('/catalog/')
def show_categories():
    categories = session.query(Category).all()
    return render_template('showcategories.html', categories=categories)


@app.route('/catalog/newcat/', methods=['GET', 'POST'])
def new_category():
    if request.method == 'GET':
        return render_template('newcategory.html')

    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if name:
            user_id = 1  # fake
            category = Category(name=name, description=description, user_id=user_id)
            session.add(category)
            session.commit()
            return redirect(url_for("show_items", category_id=category.id))
        else:
            error = "Complete info please!"
            return render_template('newcategory.html', name=name, description=description, error=error)


@app.route('/catalog/<int:category_id>/editcat/', methods=['GET', 'POST'])
def edit_category(category_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template('editcategory.html', category=category, name=category.name,
                               description=category.description)
    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = session.query(Category).filter_by(id=category_id).one()
        if name:
            category.name = name
            category.description = description
            session.commit()
            return redirect(url_for("show_items", category_id=category.id))
        else:
            error = "Complete info please!"
            return render_template('editcategory.html', category=category, name=name, description=description,
                                   error=error)


@app.route('/catalog/<int:category_id>/deletecat/', methods=['GET', 'POST'])
def delete_category(category_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template('deletecategory.html', category=category)
    elif request.method == 'POST':
        category = session.query(Category).filter_by(id=category_id).one()
        items = category.items
        if items:
            session.delete(items)
        session.delete(category)
        session.commit()
        return redirect(url_for('show_categories'))


@app.route('/catalog/<int:category_id>/items/')
def show_items(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = category.items
    return render_template('showitems.html', category=category, items=items)
