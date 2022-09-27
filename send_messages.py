from datetime import datetime
import crud
from model import connect_to_db
import os
from twilio.rest import Client

def send_message(message):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                    body=f"{message}",
                                    from_='+17087873292',
                                    to='+17639130524'
                                    )

    print(message.sid)

def message_sender():
    now = datetime.now()
    now = datetime.strftime(now, "%I:%M %p")
    now = datetime.strptime(now, "%I:%M %p")

    events = crud.get_events_by_time(now)
    for event in events:
        if event.reminder:
            send_message(event.description)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)

    message_sender()




