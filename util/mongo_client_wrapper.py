from pymongo import MongoClient
from bson import ObjectId
import datetime
import pdb

print("connecting database...")
client = MongoClient("mongodb://localhost:27017")
print("connection established with Mongo")


class MongoAPI:
    def __init__(self, data_base, document):
        self.data_base = data_base
        cursor = client[data_base]
        self.collection = cursor[document]

    def read(self):
        documents = self.collection.find()
        output = [{item: str(data[item]) for item in data}
                  for data in documents]
        return output

    def find_byid(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def write(self, data):
        new_document = data
        new_document["CreatedDate"] = datetime.datetime.today()
        result = self.collection.insert_one(new_document)
        return str(result.inserted_id)

    def write_bulk(self, data):
        result = self.collection.insert_many(data)
        return str(result.inserted_ids)

    def delete_many(self, query):
        result = self.collection.delete_many(query)
        return str(result.deleted_count)

    def read_polls(self):
        cursor = client[self.data_base]
        collection = cursor["polls"]
        documents = collection.aggregate([
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "question": 1,
                    "CreatedDate": 1
                }
            },
            {
                "$lookup": {
                    "from": "answers",
                            "localField": "_id",
                            "foreignField": "poll_id",
                            "as": "answers"
                }
            },
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "question": 1,
                    "CreatedDate": 1,
                    "answers": {
                        "answer": 1,
                        "_id": {"$toString": "$_id"},
                        "poll_id": 1
                    }
                }
            }
        ])

        output = [data for data in documents]
        return output
