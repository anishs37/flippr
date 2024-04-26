import serial
import time
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import imaplib
import email
from email.header import decode_header
import ssl

if __name__ == '__main__':
    load_dotenv()
    ssl._create_default_https_context = ssl._create_unverified_context

    last_three_vals = [None, None, None]
    last_used = 0
    # Configure the serial connection to the Arduino
    ser = serial.Serial('/dev/cu.usbmodem101', 9600)  # Update this to match your device
    ser.flushInput()
    IMAP_SERVER = 'imap.outlook.com'
    EMAIL = os.environ["FROM_EMAIL"]
    PASSWORD = os.environ["FROM_PWD"]
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('INBOX')

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if "no" in line.lower(): last_three_vals[last_used % 3] = 0
            else: last_three_vals[last_used % 3] = 1
            last_used += 1
            if last_three_vals[0] == 0 and last_three_vals[1] == 0 and last_three_vals[2] == 0:
                message = Mail(
                    from_email='flipprlights@outlook.com',
                    to_emails='indrasena.pr@gmail.com',
                    subject='Flippr Notification',
                    html_content='<strong>Energy usage too high. Please turn off your lights. Please include yes in the subject line if you would like us to turn off the lights for you, and no otherwise.</strong>')
                try:
                    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
                    response = sg.send(message)
                except Exception as e:
                    print("An error occurred:", e)
                print("sent email")

                for i in range(60):
                    status, data = mail.search(None, 'ALL')
                    break_again = False
                    # Loop through the list of email IDs
                    for num in data[0].split():
                        # Fetch the email data based on its ID
                        status, raw_email = mail.fetch(num, '(RFC822)')
                        # Parse the raw email data
                        email_message = email.message_from_bytes(raw_email[0][1])
                        # Extract email details
                        subject = decode_header(email_message['Subject'])[0][0]
                        sender = email.utils.parseaddr(email_message['From'])[1]
                        date_sent = email_message['Date']
                        
                        # Print email details
                        if "Flippr Notification" in subject and "yes" in subject.lower():
                            ser.write(b'L')
                            time.sleep(30)
                            break_again = True
                            break
                    if break_again == True: break     
                    time.sleep(1)
