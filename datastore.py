import pymongo
import json
import random

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'


class Datastore(object):
    def __init__(self, host='localhost', port=27017):
        """Create new datastore."""
        self.conn = pymongo.Connection(host, port)
        self.db = self.conn.tahoe
        self.files = self.db.petnames

    @staticmethod
    def _random_id(size=5):
        """Generates a random ID with no guarantee of uniqueness."""
        id = ''
        for i in range(size):
            id += CHARS[random.randint(0, len(CHARS) - 1)]
        return id

    def _new_id(self):
        """Generate a random ID that is guaranteed to be unique."""
        while True:
            id = self._random_id()
            if not self.get(id):
                break
        return id

    def get(self, id):
        """Retrieve an object by ID."""
        return self.files.find_one(id)

    def insert(self, data):
        """Insert an object into the database."""
        # check for existing petname
        existing = self.files.find_one(data)
        if existing:
            return existing['_id']
        # create new one if none exists
        data['_id'] = self._new_id()
        self.files.insert(data)
        return data['_id']
