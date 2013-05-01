# Download the Python helper library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = open("APISID").read().strip()
auth_token=open("APIKEY").read().strip()
client = TwilioRestClient(account_sid, auth_token)

print account_sid

message = client.sms.messages.create(body="Jenny please?! I love you <3",
    to="+14159352345",
    from_="+14158141829")
print message.sid