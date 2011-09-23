import pymongo
import random

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

class Datastore(object):
    def __init__(self):
        self.conn = pymongo.Connection()
        self.db = self.conn.tahoe
        self.files = self.db.files

    @staticmethod
    def _random_id(size=5):
        id = ''
        for i in range(size):
            id += CHARS[random.randint(0, len(CHARS) - 1)]
        return id

    def _new_id(self):
        while True:
            id = self._random_id()
            if not self.get(id):
                break
        return id

    def get(self, id):
        return self.files.find_one(id)

    def insert(self, uri):
        id = self._new_id()
        self.files.insert({
            '_id' : id,
            'uri' : uri,
        })
        return id
