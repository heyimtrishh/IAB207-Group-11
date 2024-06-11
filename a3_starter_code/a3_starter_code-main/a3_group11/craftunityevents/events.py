from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

destbp = Blueprint('event', __name__, url_prefix='/events')

@destbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    form = CommentForm()    
    return render_template('events/show.html', event=event, form=form)

# Create Event
@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
      
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(
        event_name=form.name.data,
        category=form.category.data,
        start_time=form.start_time.data,
        end_time=form.end_time.data,
        start_date=form.start_date.data,
        end_date=form.end_date.data,
        location=form.location.data,
        image=db_file_path,
        description=form.description.data,
        price=form.price.data,
        num_tickets=form.num_tickets.data,
        created_by=current_user.id
    )
      
    # add the object to the db session
    db.session.add(event)
      
    # commit to the database
    db.session.commit()
    flash(f'Successfully created new event for {event.event_name}!', 'success')
      
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)

# Update Event as Event Creator
@destbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def update_event(id):
    event = Event.query.get_or_404(id)

# Only allow the event creator to edit this event
if event.created_by != current_user.id:
    flash('Sorry, you do not have permission to edit this event.')
    return redirect(url_for('event.show', id=id)

form = UpdateEventForm(obj=event)
if form.validate_on_submit():
    event_name=form.name.data,
    category=form.category.data,
    start_time=form.start_time.data,
    end_time=form.end_time.data,
    start_date=form.start_date.data,
    end_date=form.end_date.data,
    location=form.location.data,
    image=db_file_path,
    description=form.description.data,
    price=form.price.data,
    num_tickets=form.num_tickets.data,
    created_by=current_user.id

db.session.commit()
flash('Your event has been updated!', 'success')
return redirect(url_for('event.show', id=id))

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
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path
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

    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            event_id=event.id,
            quantity=form.quantity.data,
            order_date=datetime.now()
        )
        db.session.add(order)
        db.session.commit()
        flash(f'Tickets booked successfully! Your Order ID is: {order.id}', 'success')
        return redirect(url_for('event.show', id=id))
    return render_template('events/book.html', form=form, event=event)

# Comment on Event Details Page
@destbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, event=event,
                        user=current_user) 
      #here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added!', 'success')  
      # print('Your comment has been added!', 'success') 
    # using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=id))

# Error Handlers
@destbp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@destbp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500