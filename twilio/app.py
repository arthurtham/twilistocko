from flask import Flask, request
from flask_cors import CORS
import requests
import websocket
from threading import Thread

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

#from urllib import request as requests
#from urllib.parse import urlencode

import json
import ast

from dotenv import load_dotenv
import os

import random


import ssl
from pymongo import MongoClient
from bson import ObjectId

app=Flask(__name__)
CORS(app)

load_dotenv(verbose=True)
FINNHUB_AUTH_TOKEN = os.environ.get("FINNHUB_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
TWILIO_MESSAGING_SERVICE_SID = os.environ.get("TWILIO_MESSAGING_SERVICE_SID")
TEST_NUMBERS = os.environ.get("TEST_NUMBERS").split(";")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

ws = None

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
@app.route("/update-data", methods=["POST"])
def update_data():
    content = request.json
    return 'OK'

def on_message(ws, message):
    if (isinstance(message, str)):
        json_object = json.loads(message)
        r = requests.post('http://127.0.0.1:5000/update-data', json=json_object)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

@app.route('/subscribe')
def subscribe():
    ws.send(f"{{'type': 'subscribe', 'symbol': 'GME'}}")
    return 'OK'
    
user = "python"
password = "java"
uri = f"mongodb+srv://{user}:{password}@lahack2021.fevm8.mongodb.net/stockapp"
client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)
db = client['stockinfo']
collection = db['start']

def updateDict(setOperator, phone_number, stock, target, mode):
    query = {"phone_number": phone_number}
    updated_val = {
        f"${setOperator}": {
            "stocks": [
                {
                "symbol": stock,
                "target": target,
                "mode":   mode
                }
            ]
        }
    }
    db.collection.find_one(query)
    doc_test = collection.update(
        query,
        updated_val, 
        upsert=True
    )

@app.route("/addDict", methods=["POST"])
def addDict():
    content = request.json
    updateDict("set", content["phone"], content["stock"], content["target"], content["mode"])
    print("finished add")
    return 'OK'


if __name__ == "__main__":
    #from waitress import serve
    #serve(app, host='0.0.0.0', port=5000)

    # flask_thread = Thread(target=app.run, kwargs={'host': '127.0.0.1', 'port': 5000, 'debug': True})
    # flask_thread.start()
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=" + FINNHUB_AUTH_TOKEN,
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close)
    ws.on_open = on_open
    finnhub_thread = Thread(target=ws.run_forever, daemon=True)
    finnhub_thread.start()
    app.run()

    
    
