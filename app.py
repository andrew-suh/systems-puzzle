import datetime
import os
import logging

from flask import Flask, render_template, redirect, url_for, flash
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    #when posting
    if form.validate_on_submit():
        #populate item for insertion
        item = Items(name=form.name.data, quantity=form.quantity.data,
                     description=form.description.data, date_added=datetime.datetime.now())
        try:
            db_session.add(item)
            db_session.commit()
            return redirect(url_for('success'))
        except:
            #When failed, presing the back key will keep the input boxes filled
            return "Go back and check if quantity is a number or not."
    return render_template('index.html', form=form)

#print all the data
@app.route("/success")
def success():
    results = []

    qry = db_session.query(Items)
    results = qry.all()

    return render_template('get_all.html', inspect=results)

@app.route("/delete/<int:id>")
def delete(id):
    #Query based on the id passed
    to_delete = Items.query.filter_by(id=id).first()
    try:
        #delete instead of add
        db_session.delete(to_delete)
        db_session.commit()
        #show all again
        return redirect(url_for('success'))
    except:
        return "Failed to Delete"

@app.route("/update/<int:id>", methods=('GET', 'POST'))
def update(id):
    form = ItemForm()
    to_change = db_session.query(Items).filter_by(id=id).first()
    if form.validate_on_submit():
        try:
            with open("test1.txt", 'w') as fo:
                fo.write(str(form.__dict__.keys()))
            for k in to_change.__dict__.keys():
                if k is 'date_added':
                    to_change.date_added = datetime.datetime.now()
                elif k is '_sa_instance_state':
                    pass
                elif k is 'id':
                    pass
                else:
                    setattr(to_change,k, getattr(form,k).data)
            # to_change.name = form.name.data,
            # to_change.quantity = form.quantity.data,
            # to_change.description = form.description.data,
            # to_change.date_added = datetime.datetime.now(),
            db_session.commit()
            return redirect(url_for('success'))
        except:
            return "Update failed. Try again."
    return render_template('update.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
