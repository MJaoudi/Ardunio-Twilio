# Download the Python helper library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
auth_token=open("APIKEY").read().strip()
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC32a3c49700934481addd5ce1659f04d2"
client = TwilioRestClient(account_sid, auth_token)

print auth_token
 
message = client.sms.messages.create(body="Jenny please?! I love you <3",
    to="+14159352345",
    from_="+14158141829")
print message.sid