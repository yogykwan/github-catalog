from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import Flask, render_template, request, redirect, url_for

engine = create_engine('sqlite:///githubcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/')
def show_home():
    return redirect(url_for('show_categories'))


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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
