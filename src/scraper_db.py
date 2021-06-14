import pymongo

#
#
#

class Database:

    #   client:     MongoDB client information loaded from settings.json
    #   database:   MongoDB database information loaded from settings.json
    #   collection: MongoDB collection information loaded from settings.json
    def __init__(self, client, database, collection):

        self._client = pymongo.MongoClient(client)
        self._database = database
        self._collection = collection

    #Connects to the MongoDB database/collection based on saved information
    def connect(self):

        print("CONNECTING TO DB...")

        self._database = self._client[self._database]
        self._collection = self._database[self._collection]