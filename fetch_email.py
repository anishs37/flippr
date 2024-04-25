import imaplib
import email
from email.header import decode_header
import os

load_dotenv()

# IMAP server settings
IMAP_SERVER = 'imap.outlook.com'
EMAIL = os.environ["FROM_EMAIL"]
PASSWORD = os.environ["EMAIL_PWD"]

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)

# Select the mailbox you want to fetch emails from (e.g., 'INBOX')
mail.select('INBOX')

# Search for emails
status, data = mail.search(None, 'ALL')

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
    if "Flippr Notification" in subject:
        # add if yes, if no logic and try arduino connection.
        print(f'Subject: {subject}')
        print(f'From: {sender}')
        print(f'Date: {date_sent}')

# Logout from the IMAP server
mail.logout()