from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, FormField, RadioField, SelectField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired("Type your comment...")])
  submit = SubmitField('Post Comment')

#allowed filetypes for event thumbnail
ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Create an event
class EventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[InputRequired('Type your event name')])
    event_category =  RadioField('Event Category', choices=[('Workshop','Workshop'),('Exhibition','Exhibition'),('Live Sketching','Live Sketching')])
    event_thumbnail = FileField('Event Thumbnail', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    event_summary = StringField("Event Summary", validators=[InputRequired("Summarise your event to engage attendees")])
    event_location = StringField("Event Location", validators=[InputRequired("e.g. 1234 Main St, 4321")])
    event_type = SelectField("Event Type", choices=[("Single Event"),("Recurring Event")])
    start_date = DateTimeField("Start Date", validators=InputRequired())
    end_date = DateTimeField("End Date", validators=InputRequired())
    event_description = StringField("Event Description", validators=[InputRequired("Include all the exciting & essential event details")])
    ticket_name = StringField("Ticket Name", validators=[InputRequired("e.g. General Admission")])
    ticket_quantity = IntegerField("Quantity",[InputRequired("No. of Tickets")])
    ticket_price = IntegerField("Price", validators=[InputRequired("Cost")])
    submit = SubmitField("Create Event")