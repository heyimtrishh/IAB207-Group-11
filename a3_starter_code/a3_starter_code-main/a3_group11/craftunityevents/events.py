from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Booking, User
from .forms import LoginForm, RegisterForm, CommentForm, EventForm, UpdateEventForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime

destbp = Blueprint('event', __name__, url_prefix='/events')

# Event Details Page 
@destbp.route('/<int:id>')
def event_details(id):
    event = Event.query.get_or_404(id)
    comment_form = CommentForm()
    return render_template('event_details.html', event=event)

# Create Event
@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        event = Event(
            event_name=form.event_name.data,
            category=form.event_category.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            location=form.event_location.data,
            image=db_file_path,
            description=form.event_description.data,
            price=form.ticket_price.data,
            num_tickets=form.ticket_quantity.data,
            created_by=current_user.id
        )
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        flash(f'Successfully created new event for {event.event_name}!', 'success')
        # Always end with redirect when form is valid
        return redirect(url_for('event.create'))
    return render_template('events/create_event.html', form=form)

# Update Event as Event Creator
@destbp.route('/<id>/update', methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = Event.query.get_or_404(id)
    # Only allow the event creator to edit this event
    if event.created_by != current_user.id:
        flash('Sorry, you do not have permission to edit this event.')
        return redirect(url_for('event.show', id=id))

    form = UpdateEventForm(obj=event)
    if form.validate_on_submit():
        event.event_name = form.event_name.data
        event.category = form.event_category.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        event.location = form.event_location.data
        if form.image.data:
            db_file_path = check_upload_file(form)
            event.image = db_file_path
        event.description = form.event_description.data
        event.price = form.ticket_price.data
        event.num_tickets = form.ticket_quantity.data
        db.session.commit()
        flash('Your event has been updated!', 'success')
        return redirect(url_for('event.show', id=id))

    return render_template('events/update.html', form=form, event=event)

# Cancel Event
@destbp.route('/cancel/<int:id>', methods=['POST'])
@login_required
def cancel_event(id):
    event = Event.query.get_or_404(id)
    # Only Event Creator Can Cancel Event
    if event.created_by != current_user.id:
        flash('Sorry, you do not have permission to cancel this event.')
        return redirect(url_for('event.show', id=id))
    event.status = 'Cancelled'
    db.session.commit()
    flash(f'The event {event.event_name} has been cancelled.', 'info')
    return redirect(url_for('event.show', id=id))

# File Upload
def check_upload_file(form):
    # get file data from form  
    fp = form.image.data
    filename = secure_filename(fp.filename)
    # get the current path of the module file… store image file relative to this path  
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(BASE_PATH, 'static/image', filename)
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/image/' + filename
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

# Book Event
@destbp.route('/<int:id>/book', methods=['GET', 'POST'])
@login_required
def book_event(id):
    event = Event.query.get_or_404(id)
    # No Tickets Available 
    if event.status != 'Open':
        flash('Sorry, this event is not available for booking.', 'info')
        return redirect(url_for('event.show', id=id))
    
# Booking History
@destbp.route('/userbookinghistory')
@login_required
def userbookinghistory():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('userbookinghistory.html', bookings=bookings)

    #form = OrderForm()
    #if form.validate_on_submit():
     #   order = Order(
      #      user_id=current_user.id,
       #     event_id=event.id,
        #    quantity=form.quantity.data,
         #   order_date=datetime.now()
        #)
        #db.session.add(order)
        #db.session.commit()
        #flash(f'Tickets booked successfully! Your Order ID is: {order.id}', 'success')
        #return redirect(url_for('event.show', id=id))
    #return render_template('events/book.html', form=form, event=event)

# Comment on Event Details Page
@destbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    # get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(text=form.text.data, event=event, user=current_user)
        # here the back-referencing works - comment.event is set
        # and the link is created
        db.session.add(comment)
        db.session.commit()
        # flashing a message which needs to be handled by the html
        flash('Your comment has been added!', 'success')
        # using redirect sends a GET request to event.show
        return redirect(url_for('event.show', id=id))
    return render_template('events/show.html', event=event, form=form)

# Error Handlers
@destbp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@destbp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
