from flask_wtf import FlaskForm
from wtforms.fields import (
    TextAreaField, SubmitField, StringField, 
    PasswordField, RadioField, SelectField, 
    DateTimeField, IntegerField
)
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

# Creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# This is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    contact = IntegerField("Contact Number", validators=[InputRequired('Please enter a valid contact number')])
    # Linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[
        InputRequired(),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password")
    # Submit button
    submit = SubmitField("Register")

# User comment
class CommentForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    text = TextAreaField('Comment', [InputRequired("Type your comment...")])
    submit = SubmitField('Post Comment')

# Allowed file types for event thumbnail
ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Create an event
class EventForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    event_name = StringField("Event Name", validators=[InputRequired('Type your event name')])
    event_category = RadioField('Event Category', choices=[
        ('Workshop', 'Workshop'),
        ('Exhibition', 'Exhibition'),
        ('Live Sketching', 'Live Sketching')
    ])
    event_thumbnail = FileField('Event Thumbnail', validators=[
        FileRequired(message='Image cannot be empty'), 
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])
    event_summary = StringField("Event Summary", validators=[InputRequired("Summarise your event to engage attendees")])
    event_location = StringField("Event Location", validators=[InputRequired("e.g. 1234 Main St, 4321")])
    event_type = SelectField("Event Type", choices=[
        ("Single Event", "Single Event"),
        ("Recurring Event", "Recurring Event")
    ])
    start_date = DateTimeField("Start Date", validators=[InputRequired()])
    end_date = DateTimeField("End Date", validators=[InputRequired()])
    event_description = StringField("Event Description", validators=[InputRequired("Include all the exciting & essential event details")])
    ticket_name = StringField("Ticket Name", validators=[InputRequired("e.g. General Admission")])
    ticket_quantity = IntegerField("Quantity", validators=[InputRequired("No. of Tickets")])
    ticket_price = IntegerField("Price", validators=[InputRequired("Cost")])
    submit = SubmitField("Create Event")

# Edit an event
class EditEventForm(FlaskForm):  # Changed class name to avoid duplication
    event_name = StringField("Event Name", validators=[InputRequired('Type your event name')])
    event_category = RadioField('Event Category', choices=[
        ('Workshop', 'Workshop'),
        ('Exhibition', 'Exhibition'),
        ('Live Sketching', 'Live Sketching')
    ])
    event_thumbnail = FileField('Event Thumbnail', validators=[
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])
    event_summary = StringField("Event Summary", validators=[InputRequired("Summarise your event to engage attendees")])
    event_location = StringField("Event Location", validators=[InputRequired("e.g. 1234 Main St, 4321")])
    event_type = SelectField("Event Type", choices=[
        ("Single Event", "Single Event"),
        ("Recurring Event", "Recurring Event")
    ])
    start_date = DateTimeField("Start Date", validators=[InputRequired()])
    end_date = DateTimeField("End Date", validators=[InputRequired()])
    event_description = StringField("Event Description", validators=[InputRequired("Include all the exciting & essential event details")])
    ticket_name = StringField("Ticket Name", validators=[InputRequired("e.g. General Admission")])
    ticket_quantity = IntegerField("Quantity", validators=[InputRequired("No. of Tickets")])
    ticket_price = IntegerField("Price", validators=[InputRequired("Cost")])
    submit = SubmitField("Update Event")

# Book an Event 
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20), unique=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_time = db.Column(db.DateTime, nullable=False)
    event_end_time = db.Column(db.DateTime, nullable=False)  # Add this field to show event end time
    event_location = db.Column(db.String(100), nullable=False)  # Add this field to show event location
    ticket_quantity = db.Column(db.Integer, nullable=False)
    ticket_name = db.Column(db.String(100), nullable=False)
    event_price = db.Column(db.Float, nullable=False)  # Add this field to show ticket price
    status = db.Column(db.String(50), nullable=False)

    event = db.relationship('Event', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<Event {self.name}>'
