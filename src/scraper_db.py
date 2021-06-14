import pymongo

class Database:

    def __init__(self, client, database, collection):

        self._client = pymongo.MongoClient(client)
        self._database = database
        self._collection = collection

    def connect(self):

        print("CONNECTING TO DB...")

        self._database = self._client[self._database]
        self._collection = self._database[self._collection]