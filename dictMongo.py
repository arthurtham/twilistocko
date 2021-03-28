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

# setOperator = "$set"
# newVal = {
#     setOperator: {
#         "stocks": [
#             {
#             "symbol": "yay",
#             "target": 2.00,
#             "mode":   "less"
#             }
#         ]
#     }
# }
# sec_new_values = {
#     setOperator: {
#         "stocks": [
#             {
#             "symbol": "TME",
#             "target": 59.00,
#             "mode":   "greater"
#             }
#         ]
#     }
# }
# query = {"phone_number": "+33333333"}
# updates the doc, creates new doc if can't find doc w/ specified id
# use $set for adding fields, $unset for removing fields
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

updateDict("set", "+999999999", "MSFT", 32, "less")
updateDict("set", "+324145679", "AMZ", 29, "greater")