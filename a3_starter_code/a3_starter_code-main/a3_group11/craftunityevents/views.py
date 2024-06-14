# Importing necessary modules and functions
from flask import Blueprint, render_template, request, redirect, url_for  # Flask modules for creating a blueprint, rendering templates, handling requests, and redirection
from .models import Event  # Import the Event model from the models module
from datetime import datetime  # Import datetime module for handling date and time
from . import db  # Import the database instance from the current package

# Create a Blueprint named 'main'
mainbp = Blueprint('main', __name__)

# Route for search functionality
@mainbp.route('/search')
def search():
    # Check if the search query parameter exists and is not empty
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])  # Print the search query for debugging
        query = "%" + request.args['search'] + "%"  # Create a SQL LIKE query pattern
        # Query the database for events matching the search description
        event = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        # Render the 'index.html' template with the search results
        return render_template('index.html', events=event)
    else:
        # Redirect to the index page if the search query is empty
        return redirect(url_for('main.index'))

# Route for the index page
@mainbp.route('/')
def index():
    # Query for upcoming events starting from the current date, ordered by the start date, limited to 3 results
    upcoming_events = Event.query.filter(Event.start_date >= datetime.now()).order_by(Event.start_date.asc()).limit(3).all()
    # Query for events categorized as 'Exhibition'
    events_exhibition = Event.query.filter(Event.event_category == 'Exhibition').all()
    # Query for events categorized as 'Workshop'
    events_workshop = Event.query.filter(Event.event_category == 'Workshop').all()
    # Query for events categorized as 'Live Demo'
    events_demo = Event.query.filter(Event.event_category == 'Live Demo').all()
    
    # Render the 'index.html' template with the queried events
    return render_template('index.html', 
        events_upcoming=upcoming_events, events_exhibition=events_exhibition, events_workshop=events_workshop, events_demo=events_demo)
