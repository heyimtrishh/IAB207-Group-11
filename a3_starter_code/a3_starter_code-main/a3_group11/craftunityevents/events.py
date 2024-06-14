from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .models import Event, Comment, Booking, User
from .forms import LoginForm, RegisterForm, CommentForm, EventForm, UpdateEventForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime

destbp = Blueprint('event', __name__, url_prefix='/events')

# Event Details Page 
@destbp.route('/<id>')
def details(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    comment_form = CommentForm()
    return render_template('events/event_details.html', event=event, comment_form=comment_form)

# Comment on Event Details Page
@destbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(
            text=comment_form.text.data, 
            event_id=id, 
            user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('event.details', id=id))
    return render_template('events/event_details.html', form=comment_form, event=event)

# Create Event
@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    
    if form.validate_on_submit():
        db_file_path = check_upload_file(form.event_thumbnail.data)
        print(f"File path: {db_file_path}")

        try:
            # Instantiate an Event object with the following form fields
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
            # Add the object to the db session
            db.session.add(event)
            # Commit to the database
            db.session.commit()
            flash(f'Successfully created new event for {event.event_name}!', 'success')
            return redirect(url_for('event.event_details', id=event.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Event creation failed.', 'danger')
            print(f"Exception: {e}")
    else:
        print("Form not validated")
        print(form.errors) # Print form errors to the console
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"Error in {fieldName}: {err}")

    return render_template('events/create_event.html', form=form)

# Update Event as Event Creator
@destbp.route('/<id>/update', methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = Event.query.get_or_404(id)
    # Only allow the event creator to edit this event
    if event.created_by != current_user.id:
        flash('Sorry, you do not have permission to edit this event.')
        return redirect(url_for('event.details', id=id))

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
        return redirect(url_for('event.details', id=id))

    return render_template('events/update.html', form=form, event=event)

# Cancel Event
@destbp.route('/cancel/<int:id>', methods=['POST'])
@login_required
def cancel_event(id):
    event = Event.query.get_or_404(id)
    # Only Event Creator Can Cancel Event
    if event.created_by != current_user.id:
        flash('Sorry, you do not have permission to cancel this event.')
        return redirect(url_for('event.details', id=id))
    event.status = 'Cancelled'
    db.session.commit()
    flash(f'The event {event.event_name} has been cancelled.', 'info')
    return redirect(url_for('event.details', id=id))

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
        return redirect(url_for('event.details', id=id))
    
# Booking History
@destbp.route('/userbookinghistory', methods=['GET'])
@login_required
def userbookinghistory():
    # Fetch events booked by the current user
    bookings = db.session.query(bookings).filter_by(user_id=current_user.id).all()
    return render_template('events/userbookinghistory.html', bookings=bookings)

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

# Error Handlers
@destbp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@destbp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
