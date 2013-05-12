#A script that adds phone numbers to a queue
#Texting "add" adds the number to the queue
#Texting "remove" and then the number removes that number from the queue


from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
import socket
 
app = Flask(__name__)

account_sid = open("APISID").read().strip()
auth_token=open("APIKEY").read().strip()

numbers = [];
index = 0
 
@app.route("/", methods=['GET', 'POST'])
def recieveMessage():
    """Respond to incoming calls with a simple text message."""
 
    f = open('numbers.txt', 'r')
    numbers = f.read().split()
    print numbers
    f.close()
    resp = twilio.twiml.Response()

    body = str(request.values.get('Body', None)).lower()
    fromNum = str(request.values.get('From', None))

    words = body.split()

    print "Got a message from "+fromNum+" saying "+body
    print numbers
    message = ""


    if "add" in words[0]:
      if fromNum in numbers:
          message = "That number has already been added"
      else:
          numbers.append(fromNum)
          message = fromNum +" has been added to the queue"

    elif "remove" in words[0]:
      if len(numbers) == 1:
          message = "Please text \"Remove + <number to remove>\""
      elif fromNum in numbers:
          if len([numbers.remove(x) for x in numbers if fromNum in x]) > 0:
            message = words[1] + " has been removed from the queue"
          else:
            message = words[1] + " is not in the queue"
      else:
          message = "You are not authorized to remove numbers from the queue"
 


    f = open('numbers.txt', 'w')
    f.write(' '.join(numbers))
    f.close()
    resp.sms(message)
    return str(resp)

@app.route("/next", methods=['GET', 'POST'])
def nextInQueue():
    """Respond to incoming calls with a simple text message."""
    global index

    print "next"

    f = open('numbers.txt', 'r')
    numbers = f.read().split()
    f.close()



    if len(numbers) == 0:
      return "No numbers exist"

    index+=1

    if index >= len(numbers):
      index=0

    send()

    return "Sent to "+numbers[index]


@app.route("/resend", methods=['GET', 'POST'])
def send():
    """Respond to incoming calls with a simple text message."""
    global index

    print "resend"
    client = TwilioRestClient(account_sid, auth_token)

    f = open('numbers.txt', 'r')
    numbers = f.read().split()
    print numbers
    f.close()


    print numbers[index]

    smsMessage = client.sms.messages.create(body="The baby is crying! It's your turn!",
      to=numbers[index],
      from_="+12013512763")



    return "Sent to "+numbers[index]


 
if __name__ == "__main__":
    app.run(debug=True)





