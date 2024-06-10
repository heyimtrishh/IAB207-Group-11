from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    event = db.session.scalars(db.select(Event)).all()    
    return render_template('index.html', events=events)

@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        event = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
