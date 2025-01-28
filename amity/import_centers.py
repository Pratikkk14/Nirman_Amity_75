import json
from pymongo import MongoClient

# Establish a connection to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Access the myDatabase database
db = client['myDatabase']

# Access the users collection
collection = db['users']

# Load the JSON data from the file
with open('centers.json') as file:
    data = json.load(file)

# Insert the data into the collection
if isinstance(data, list):
    collection.insert_many(data)
else:
    collection.insert_one(data)

print("Data has been successfully imported into the users collection.")
