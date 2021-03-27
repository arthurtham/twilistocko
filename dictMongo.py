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
#     "phone": "000002222",
#     "stocks": [
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


# total number of documents
total_docs = collection.count_documents({})
print(f"Collection Name: {collection.name}, has {total_docs} documents")

# prints the current data of certain id
try:
    find_result = collection.find_one(ObjectId("605f8e88fb585f8ab99369ea"))
    
except NameError as error:
    find_result = None
    print(error, "-- need to use pip3 to install bson. Consider importing 'ObjectId' class from the 'bson' library")

if find_result != None and type(find_result) == dict:
    print ("found doc:", find_result)

# updates the doc, creates new doc if can't find doc w/ specified id
# use $set for adding fields, $unset for removing fields
doc = collection.find_one_and_update(
        {"_id" : ObjectId("605f8e88fb585f8ab99369ea")},
        {"$set":
            {"phone": "1234567890"}
        }, upsert=True
    )
new_result = collection.find_one(ObjectId("605f8e88fb585f8ab99369ea"))
print ("UPDATED doc:", new_result)
print("end")