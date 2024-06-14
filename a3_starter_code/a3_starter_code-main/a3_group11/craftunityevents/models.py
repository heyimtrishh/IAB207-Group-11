from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    contact_number = db.Column(db.Integer, index=True, nullable=False)
    email_id = db.Column(db.String(100), index=True, nullable=False)
    address = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(400), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)

    def __repr__(self):
        return f"Name: {self.full_name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_category = db.Column(db.String(20), nullable=False)
    event_thumbnail = db.Column(db.String(400))
    event_summary = db.Column(db.String(200))
    event_location = db.Column(db.String(200), nullable=False)
    event_type  = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    event_description = db.Column(db.String(400))
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    ticket_quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationship
    comments = db.relationship('Comment', backref='event', lazy=True)
    event_bookings = db.relationship('Booking', backref='event', lazy=True)

    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400), nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='comments', lazy=True)
    
    def __repr__(self):
        return f"Comment: {self.text}"

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_thumbnail = db.Column(db.String(400))
    event_price = db.Column(db.Float, nullable=False)
    event_quantity = db.Column(db.Integer, nullable=False)
    event_date = db.Column(db.Date, default=datetime.now, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    event_location = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('booking_statuses.id'), nullable=False)

    def __repr__(self):
        return f"Booking for event_id: {self.event_id}, user_id: {self.user_id}"

class BookingStatus(db.Model):
    __tablename__ = 'booking_statuses'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

    # Relationship
    booking = db.relationship('Booking', backref='status', lazy=True)

    def __repr__(self):
        return f"Status: {self.status}"

        return f"Comment: {self.text}"
