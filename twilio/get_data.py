from dotenv import load_dotenv
import os
import requests
import websocket
import json

load_dotenv(verbose=True)
FINNHUB_AUTH_TOKEN = os.environ.get("FINNHUB_AUTH_TOKEN")

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

if __name__ == '__main__':
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=" + FINNHUB_AUTH_TOKEN,
									on_message = on_message,
									on_error = on_error,
									on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()