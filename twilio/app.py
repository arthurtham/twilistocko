from flask import Flask, request
from flask_cors import CORS
import requests

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

#from urllib import request as requests
#from urllib.parse import urlencode

import json
import ast

from dotenv import load_dotenv
load_dotenv()

import os

import random

app=Flask(__name__)
CORS(app)


FINNHUB_AUTH_TOKEN = os.environ.get("FINNHUB_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
TWILIO_MESSAGING_SERVICE_SID = os.environ.get("TWILIO_MESSAGING_SERVICE_SID")
TEST_NUMBERS = os.environ.get("TEST_NUMBERS").split(";")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

### START Twilio Functions ###
def send_message(to_number, msg):
    message = client.messages.create(
        to=to_number, 
        from_=TWILIO_MESSAGING_SERVICE_SID,
        body=msg)

    return message.sid

def send_media_message(to_number, msg, media):
    message = client.messages.create(
        to=to_number, 
        from_=TWILIO_MESSAGING_SERVICE_SID,
        media_url=[media],
        body=msg)

    return message.sid

### END Twilio Functions ###

### START Twilio Webhook Functions ###
@app.route("/hello-world", methods=["POST"])
def hello_world():
    print(request.values)
    print(request.values.get('From', ''))

    incoming_number = str(request.values.get("From", ""))
    incoming_msg    = request.values.get('Body', '').lower()
    #resp = MessagingResponse()
    #msg = resp.message()
    processed_incoming_msg = str(incoming_msg).strip().lower()

    message_sid = send_message(incoming_number, "Hello world")

    return message_sid



@app.route("/test-notification", methods=["GET","POST"])
def test_notification():
    print(request.values if request is not None else "null")


    stock_symbol = random.choice(["AAPL", "MSFT", "GE", "SBUX", "NKE"])
    stock_request = requests.get(f'https://finnhub.io/api/v1/quote?symbol={stock_symbol}&token={FINNHUB_AUTH_TOKEN}')
    stock_request = stock_request.json()

    message_body = f"{stock_symbol} currently has {stock_request['c']} points. Buy now!"
    
    message_sid = send_message(TEST_NUMBERS[random.randint(0,len(TEST_NUMBERS)-1)], message_body)
    return message_sid



### END Twilio Webhook Functions ###

# TODO: Add/remove/manage requests to mongo functions?


if __name__ == "__main__":
    #from waitress import serve
    #serve(app, host='0.0.0.0', port=5000)
    app.run(host="localhost", port=5000)
    
