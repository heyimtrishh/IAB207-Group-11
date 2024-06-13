from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from datetime import datetime
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        event = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        return render_template('index.html', events=event)
    else:
        return redirect(url_for('main.index'))

# Index / Home Page 
@mainbp.route('/')
def index():
    upcoming_events = Event.query.filter(Event.start_date >= datetime.now()).order_by(Event.start_date.asc()).limit(3).all()
    events_exhibition = Event.query.filter(Event.event_category == 'Exhibition').all()
    events_workshop = Event.query.filter(Event.event_category == 'Workshop').all()
    events_demo = Event.query.filter(Event.event_category == 'Live Demo').all()
    return render_template('index.html', 
    events_upcoming=upcoming_events, events_exhibition=events_exhibition, events_workshop=events_workshop, events_demo=events_demo)