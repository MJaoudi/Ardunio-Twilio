# Download the Python helper library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = open("APISID").read().strip()
auth_token=open("APIKEY").read().strip()
client = TwilioRestClient(account_sid, auth_token)

message = client.sms.messages.create(body="fre$$$h",
    to="ToNum"
    from_="+12013512763")
print message.sid