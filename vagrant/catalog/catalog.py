from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def HomePage():
    return redirect(url_for('CatalogPage'))


@app.route('/catalog/')
def CatalogPage():
    return "list all catagories"


@app.route('/catalog/newcat/', methods=['GET', 'POST'])
def NewCatagory():
    if request.method == 'GET':
        return "adding new catagory"
    elif request.method == 'POST':
        return "added new catagory"


@app.route('/catalog/<int:category_id>/editcat/', methods=['GET', 'POST'])
def EditCategory(category_id):
    if request.method == 'GET':
        return "editing category No.{id}".format(id=category_id)
    elif request.method == 'POST':
        return "edited category No.{id}".format(id=category_id)


@app.route('/catalog/<int:category_id>/deletecat/', methods=['GET', 'POST'])
def DeleteCategory(category_id):
    if request.method == 'GET':
        return "deleting category No.{id}".format(id=category_id)
    elif request.method == 'POST':
        return "deleted catagory"


@app.route('/catalog/<int:category_id>/items/')
def CategoryPage(category_id):
    return "list all items from category No.{id}".format(id=category_id)


@app.route('/catalog/<int:category_id>/newitem/', methods=['GET', 'POST'])
def NewItem(category_id):
    if request.method == 'GET':
        return "adding item page for category No.{id}".format(id=category_id)
    elif request.method == 'POST':
        return "added item"


@app.route('/catalog/<int:category_id>/items/<int:item_id>/edititem/', methods=['GET', 'POST'])
def EditItem(category_id, item_id):
    if request.method == 'GET':
        return "editing {item_id} from Category {category_id}".format(item_id=item_id, category_id=category_id)
    elif request.method == 'POST':
        return "edited {item_id} from Category {category_id}".format(item_id=item_id, category_id=category_id)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/deleteitem/', methods=['GET', 'POST'])
def DeleteItem(category_id, item_id):
    if request.method == 'GET':
        return "deleting {item_id} from Category {category_id}".format(item_id=item_id, category_id=category_id)
    elif request.method == 'POST':
        return "deleted {item_id} from Category {category_id}".format(item_id=item_id, category_id=category_id)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def ItemPage(category_id, item_id):
    return "show item {item_id} from Category {category_id}".format(item_id=item_id, category_id=category_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
