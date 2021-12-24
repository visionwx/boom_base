import pymongo


class MongoDB():
    
    def __init__(self, host='localhost', port=27017, 
        db_name='eog'):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client.get_database(db_name)

    def auth(self, username, password):
        self.db.authenticate(username, password)
        return True

    @classmethod
    def create(cls, **kwargs):
        obj = cls(host=kwargs['host'], port=kwargs['port'], db_name=kwargs['db'])
        if kwargs.get('auth', False):
            obj.auth(kwargs['username'], kwargs['password'])
        return obj

# 数据库实例
MDB: MongoDB = None

def getMongoInstance(
    host, port, db, auth, username, password
):
    global MDB
    if MDB is not None:
        return MDB

    mongoConfig = {
        'host': host,
        'port': port,
        'db': db,
        'auth': auth,
        'username': username,
        'password': password,
    }
    MDB = MongoDB.create(**mongoConfig)
    
    return MDB
