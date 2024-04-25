# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

message = Mail(
    from_email='indrasena.pr@gmail.com',
    to_emails='anish.susarla@gmail.com',
    subject='Flippr Notification',
    html_content='<strong>Energy usage too high. Please turn off your lights.</strong>')
try:
    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print("error")
    print(e.message)