# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

message = Mail(
    from_email='flipprlights@outlook.com',
    to_emails='anish.susarla@gmail.com',
    subject='Flippr Notification',
    html_content='<strong>Energy usage too high. Please turn off your lights. Please include yes in the subject line if you would like us to turn off the lights for you, and no otherwise.</strong>')
try:
    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)
except Exception as e:
    print("error")
    print(e.message)