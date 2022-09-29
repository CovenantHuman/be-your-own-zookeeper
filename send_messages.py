from datetime import datetime
import crud
from model import connect_to_db
import os
from twilio.rest import Client
from flask_crontab import Crontab
from server import app

crontab = Crontab(app)

def send_message(message):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                    body=f"{message}",
                                    from_= os.environ['FROM_PHONE_NUMBER'],
                                    to= os.environ['TO_PHONE_NUMBER']
                                    )

    print(message.sid)

@crontab.job()
def message_sender():
    connect_to_db(app)
    now = datetime.now()
    now = datetime.strftime(now, "%I:%M %p")
    now = datetime.strptime(now, "%I:%M %p")

    events = crud.get_events_by_time(now)
    for event in events:
        if event.reminder:
            send_message(event.description)





