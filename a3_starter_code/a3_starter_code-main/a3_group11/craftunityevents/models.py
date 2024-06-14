# Importing necessary modules
from . import db  # Import the database instance from the current package
from datetime import datetime  # Import datetime module for handling date and time
from flask_login import UserMixin  # Import UserMixin for user session management

# Define the User model with UserMixin for session management
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    full_name = db.Column(db.String(100), index=True, unique=True, nullable=False)  # User's full name
    contact_number = db.Column(db.Integer, index=True, nullable=False)  # Contact number
    email_id = db.Column(db.String(100), index=True, nullable=False)  # Email address
    address = db.Column(db.String(100), index=True, nullable=False)  # Address
    password_hash = db.Column(db.String(400), nullable=False)  # Hashed password

    # Relationships
    comments = db.relationship('Comment', backref='user', lazy=True)  # One-to-many relationship with comments
    bookings = db.relationship('Booking', backref='user', lazy=True)  # One-to-many relationship with bookings
    created_event = db.relationship('Event', backref='user', lazy=True)  # One-to-many relationship with events created

    # Representation of the User object
    def __repr__(self):
        return f"Name: {self.full_name}"

# Define the Event model
class Event(db.Model):
    __tablename__ = 'events'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    event_name = db.Column(db.String(100), nullable=False)  # Event name
    event_category = db.Column(db.String(20), nullable=False)  # Event category
    event_thumbnail = db.Column(db.String(400))  # Event thumbnail URL
    event_summary = db.Column(db.String(200))  # Event summary
    event_location = db.Column(db.String(200), nullable=False)  # Event location
    event_type  = db.Column(db.String(200), nullable=False)  # Event type
    start_date = db.Column(db.Date, nullable=False)  # Event start date
    end_date = db.Column(db.Date, nullable=False)  # Event end date
    event_description = db.Column(db.String(400))  # Event description
    start_time = db.Column(db.Time, nullable=False)  # Event start time
    end_time = db.Column(db.Time, nullable=False)  # Event end time
    ticket_price = db.Column(db.Float, nullable=False)  # Ticket price
    ticket_quantity = db.Column(db.Integer, nullable=False)  # Number of tickets available
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key to the user who created the event

    # Relationships
    comments = db.relationship('Comment', backref='event', lazy=True)  # One-to-many relationship with comments
    event_bookings = db.relationship('Booking', backref='event', lazy=True)  # One-to-many relationship with bookings

    # Representation of the Event object
    def __repr__(self):
        return f"Name: {self.name}"

# Define the Comment model
class Comment(db.Model):
    __tablename__ = 'comments'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    text = db.Column(db.String(400), nullable=False)  # Comment text
    posted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)  # Date and time when the comment was posted
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)  # Foreign key to the event
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to the user who posted the comment

    # Representation of the Comment object
    def __repr__(self):
        return f"Comment: {self.text}"

# Define the Booking model
class Booking(db.Model):
    __tablename__ = 'bookings'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    event_name = db.Column(db.String(100), nullable=False)  # Name of the event
    event_price = db.Column(db.Float, nullable=False)  # Price of the event ticket
    event_quantity = db.Column(db.Integer, nullable=False)  # Number of tickets booked
    event_date = db.Column(db.Date, default=datetime.now, nullable=False)  # Date of the event
    start_time = db.Column(db.Time, nullable=False)  # Event start time
    end_time = db.Column(db.Time, nullable=False)  # Event end time
    event_location = db.Column(db.String(200), nullable=False)  # Location of the event
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to the user who made the booking
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)  # Foreign key to the event
    status_id = db.Column(db.Integer, db.ForeignKey('booking_statuses.id'), nullable=False)  # Foreign key to the booking status

    # Representation of the Booking object
    def __repr__(self):
        return f"Booking for event_id: {self.event_id}, user_id: {self.user_id}"

# Define the BookingStatus model
class BookingStatus(db.Model):
    __tablename__ = 'booking_statuses'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    status = db.Column(db.String(50), nullable=False)  # Booking status

    # Relationships
    booking = db.relationship('Booking', backref='status', lazy=True)  # One-to-many relationship with bookings

    # Representation of the BookingStatus object
    def __repr__(self):
        return f"Status: {self.status}"
