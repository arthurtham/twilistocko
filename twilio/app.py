from flask import Flask, request
from flask_cors import CORS

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from urllib import request as requests
from urllib.parse import urlencode

import json
import ast

from dotenv import load_dotenv
load_dotenv()

import os

app=Flask(__name__)
CORS(app)

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

### START Twilio Functions ###
def send_message(to_number, msg):
    message = client.messages.create(
        to=to_number, 
        from_=TWILIO_PHONE_NUMBER,
        body=msg)

    return message.sid

def send_media_message(to_number, msg, media):
    message = client.messages.create(
        to=to_number, 
        from_=TWILIO_PHONE_NUMBER,
        media_url=[media],
        body=msg)

    return message.sid

### END Twilio Functions ###


@app.route("/", methods=["POST"])
def index():
    print(request.values)
    print(request.values.get('From', ''))

    incoming_number = str(request.values.get("From", ""))
    incoming_msg    = request.values.get('Body', '').lower()
    #resp = MessagingResponse()
    #msg = resp.message()
    processed_incoming_msg = str(incoming_msg).strip().lower()

    message_sid = send_message(incoming_number, "Hello world")

    return message_sid

if __name__ == "__main__":
    #from waitress import serve
    #serve(app, host='0.0.0.0', port=5000)
    app.run(host="localhost", port=5000)
    
