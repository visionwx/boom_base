import pymongo
from boom_base.configParser import RelationDatabaseConfig

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
    host=None, 
    port=None, 
    db=None, 
    auth=None, 
    username=None, 
    password=None
):
    global MDB
    if MDB is not None:
        return MDB

    if host is None or port is None or db is None:
        # raise Exception("getMongoInstance error: host/port/db is None")
        rdc = RelationDatabaseConfig.fromConfig()
        mongoConfig = {
            'host': rdc.host,
            'port': rdc.port,
            'db': rdc.db,
            'auth': rdc.auth,
            'username': rdc.username,
            'password': rdc.password,
        }
    else:
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
