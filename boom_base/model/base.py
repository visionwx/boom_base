import abc
from boom_base.mongodb import getMongoInstance

class COLLECTIONS:
    USERS       = "users"
    VIDEOS      = "videos"
    COMMENTS    = "comments"
    VIDEO_INBOX = "videoInbox"

class Collection:
    # 共有字段
    # metadata = { createTime, updateTime, deleteTime,} 10位时间戳
    BASE_FIELDS = [
        "_id",
        "metadata",
        "isDelete"
    ]
    # 集合名称
    NAME:str = None

    # 数据库实例
    DB = None

    # 所有字段
    FIELDS = []

    # 必须字段，create的时候，必须带入
    REQUIRED_FIELDS = []

    # 隐藏字段集合，定义当调用toJson函数时，不含含的字段
    HIDDEN_FIELDS = []

    # limit 最大查询返回items数量
    LIMIT = 50
    
    # 构建函数
    def __init__(self):
        self.DB = getMongoInstance()
        
    @abc.abstractmethod
    def create(self, data, id=None):
        pass
    @abc.abstractmethod
    def update(self, data, id):
        pass
    @abc.abstractmethod
    def delete(self, id):
        pass
    @abc.abstractmethod
    def get(self, id):
        pass
    @abc.abstractmethod
    def list(self, condition = None, 
        after = None, limit = None, 
        filter = None):
        pass