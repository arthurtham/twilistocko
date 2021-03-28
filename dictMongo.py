import ssl
from pymongo import MongoClient
from bson import ObjectId
user = "python"
password = "java"
uri = f"mongodb+srv://{user}:{password}@lahack2021.fevm8.mongodb.net/stockapp"
client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)
db = client['stockinfo']
collection = db['start']

# adding a doc to the database
# post = {
#     "123452222": [
#         {
#         "symbol": "AMZN",
#         "target": 80.00,
#         "mode":   "less"
#         },
#         {
#         "symbol": "GOOG",
#         "target": 60.00,
#         "mode":   "greater"
#         }
#     ]
# }
# posts = db.start
# post_id = posts.insert_one(post).inserted_id


# figure out how to add to/remove from the dictionary of stock notifications

# updates the doc, creates new doc if can't find doc w/ specified id
# use $set for adding fields, $unset for removing fields

new_values = {
    "$set": {
        "+333333333": [
            {
            "symbol": "yay",
            "target": 2.00,
            "mode":   "less"
            }
        ]
    }
}

query = {"phone_number": "+33333333"}
db.cursor.find_one(query)
doc_test = collection.update(
        query,
        new_values, 
        upsert=True
    )

print("end")