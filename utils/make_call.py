import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta



def make_call(users, courses):
    utc_dt = datetime.utcnow()
    ist_dt = utc_dt + timedelta(hours=5.5)
    current_time = ist_dt.strftime("%H:%M:%S")


    a_c = ["CSE 463", "CSE 511", "CSE 512", "CSE 535", "CSE 543", "CSE 546",
             "CSE 551", "CSE 573", "CSE 575", "CSE 576", "CSE 578", "CSE 579", "CSE 598"]
    b_c = ["CSE 598", "CSE 576", "CSE 575", "CSE 572", "CSE 571", "CSE 569", "CSE 564", "CSE 551", "CSE 546", 
            "CSE 539", "CSE 534", "CSE 512", "CSE 511", "CSE 509", "CSE 475", "CSE 472", "CSE 471", 
            "CSE 445", "CSE 408"]
    
    set_available = set([d['title'] for d in courses])

    set_desired = set(b_c)
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