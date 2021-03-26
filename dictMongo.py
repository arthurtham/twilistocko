import ssl
from pymongo import MongoClient

user = "python"
password = "java"
uri = f"mongodb+srv://{user}:{password}@lahack2021.fevm8.mongodb.net/stockapp"
client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)
db = client['stockinfo']
collection = db['start']


post = {
    "phone": "000002222",
    "stocks": {
        "symbol": "AAPL",
        "target": 60.00,
        "mode":   "less"
    }
}
posts = db.start
post_id = posts.insert_one(post).inserted_id
