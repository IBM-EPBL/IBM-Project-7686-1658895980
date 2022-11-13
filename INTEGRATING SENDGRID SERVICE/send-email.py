 
import os
import response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='rjai8401@gmailcom',
    to_emails='rjai8401@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(api_key=os.environ.get('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'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)
 