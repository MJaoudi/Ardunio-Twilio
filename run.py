#A script that adds phone numbers to a queue
#Texting "add" adds the number to the queue
#Texting "remove" and then the number removes that number from the queue


from flask import Flask, request, redirect
import twilio.twiml
import socket
 
app = Flask(__name__)

numbers = [];
 
@app.route("/", methods=['GET', 'POST'])
def recieveMessage():
    """Respond to incoming calls with a simple text message."""
 

    f = open('numbers.txt', 'r')
    print f.read()
    numbers = f.read().split()
    f.close()

    resp = twilio.twiml.Response()

    body = str(request.values.get('Body', None)).lower()
    fromNum = str(request.values.get('From', None))

    words = body.split()

    print "Got a message from "+fromNum+" saying "+body
    print numbers

    if "add" in words[0]:
      if fromNum in numbers:
          message = "That number has already been added"
      else:
          numbers.append(fromNum)
          message = fromNum +" has been added to the queue"

    elif "remove" in words[0]:
      if fromNum in numbers:
          if len([numbers.remove(x) for x in numbers if fromNum in x]) > 0:
            message = words[1] + " has been removed from the queue"
          else:
            message = words[1] + " is not in the queue"
      else:
          message = "You cannot remove numbers from the queue"


    f = open('numbers.txt', 'w')
    f.write(' '.join(numbers))
    f.close()
    resp.sms(message)
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)


