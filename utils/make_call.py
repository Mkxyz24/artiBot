import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta



def make_call(users):
    utc_dt = datetime.utcnow()
    ist_dt = utc_dt + timedelta(hours=5.5)
    current_time = ist_dt.strftime("%H:%M:%S")
    if(current_time >= '07:00:00' and current_time <= '23:00:00'):
        load_dotenv()
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        for user in users:
            num = os.getenv(user)
            print(num)
            call = client.calls.create(
                twiml='<Response><Say>Hello ' + user + ', your desired courses are open!</Say></Response>',
                to = num,
                from_ = '+19403737261'  
            )
            print(call.sid)