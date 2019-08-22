import datetime
import os

from flask import Flask, render_template, redirect, url_for, flash
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    # Only when posting
    if form.validate_on_submit():
        # Populate item for insertion
        item = Items(name=form.name.data, quantity=form.quantity.data,
                     description=form.description.data, date_added=datetime.datetime.now())
        try:
            db_session.add(item)
            db_session.commit()
            return redirect(url_for('success'))
        except:
            #When failed, pressing the back key will keep the input boxes filled
            return "Go back and check if quantity is a number or not."
    return render_template('index.html', form=form)

#print all the data
@app.route("/success")
def success():
    results = []

    qry = db_session.query(Items).order_by("id")
    results = qry.all()

    return render_template('get_all.html', inspect=results)

@app.route("/delete/<int:id>")
def delete(id):
    # Query based on the id passed
    to_delete = Items.query.filter_by(id=id).first()
    try:
        # Delete instead of add
        db_session.delete(to_delete)
        db_session.commit()
        # Show all again
        return redirect(url_for('success'))
    except:
        return "Failed to Delete"

@app.route("/update/<int:id>", methods=('GET', 'POST'))
def update(id):
    form = ItemForm()
    to_change = db_session.query(Items).filter_by(id=id).first()
    if form.validate_on_submit():
        try:
            for k in to_change.__dict__.keys():
                if k is 'date_added':
                    to_change.date_added = datetime.datetime.now()
                elif k is '_sa_instance_state':
                    pass
                elif k is 'id':
                    pass
                else:
                    # Appending keys to variables break syntax
                    setattr(to_change, k, getattr(form,k).data)
            db_session.commit()
            return redirect(url_for('success'))
        except:
            return "Update failed. Try again."
    return render_template('update.html', form=form)

if __name__ == '__main__':
    # Added port to make other configs work
    app.run(host='0.0.0.0', port=5001)
