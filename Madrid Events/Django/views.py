from django.shortcuts import render

import pymongo

# Connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ProjectDB"]  # Your MongoDB database name
collection = db["events"]  # Your MongoDB collection name



# Retrieve a review from the 'ratings' collection
query = {"name": "Viernes Fitz"}
random = collection.find_one(query)
if collection.find_one(query) is not None:
    print("Retrieved document:", random)
else:
    print("No document found.")