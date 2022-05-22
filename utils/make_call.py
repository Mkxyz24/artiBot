import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta



def make_call(users, courses):
    utc_dt = datetime.utcnow()
    ist_dt = utc_dt + timedelta(hours=5.5)
    current_time = ist_dt.strftime("%H:%M:%S")

    #desired specific list
    desired_ab = ['92030', '70517', '81285', '81289', '90104', '97669',
                     '96730', '76770', '98070', '75623', '83713', '92173', '96290', '78322',
                     '86207', '96593', '76055', '86208', '77802', '83405', '96739', '78302',
                     '84856', '86209', '96727', '89746', '87271']
    
    set_available = set([d['id'] for d in courses])

    set_desired = set(desired_ab)
    open = set_available.intersection(set_desired)
    
    load_dotenv()
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    for user in users:
        num = os.getenv(user)
        print(num)
        #ab all day calling
        if user == 'NUM_1' or user == 'NUM_4':
            if(len(open) > 0):
                call = client.calls.create(
                    twiml='<Response><Say>Hello ' + user + ', your desired courses are open!</Say></Response>',
                    to = num,
                    from_ = '+19403737261'  
                )
                print(call.sid)
        #others only day time
        elif(current_time >= '07:00:00' and current_time <= '23:00:00'):
            if(len(open) > 0):
                call = client.calls.create(
                    twiml='<Response><Say>Hello ' + user + ', your desired courses are open!</Say></Response>',
                    to = num,
                    from_ = '+19403737261'  
                )
                print(call.sid)