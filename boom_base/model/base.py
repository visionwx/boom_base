import abc
import bson
import pymongo
import time
from boom_base.mongodb import getMongoInstance
from boom_base.exception import DocumentNotExistException, CollectionRequireFieldNotProvideException

def getCollectRef(collectionName):
    MDB = getMongoInstance()
    return MDB.db[collectionName]

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
        pass

    @classmethod
    def create(cls, **kwargs):
        # 获取集合引用
        DB = getCollectRef(cls.NAME)

        data = {}
        # check required fields
        for rf in cls.REQUIRED_FIELDS:
            if rf in kwargs.keys():
                continue
            raise CollectionRequireFieldNotProvideException(rf)
        
        # filter unnecessary fields
        for k,v in kwargs.items():
            if k not in (cls.FIELDS + cls.BASE_FIELDS):
                continue
            if k == "_id":
                v = bson.ObjectId(v)
            data[k] = v

        if data:
            curTime = time.time() * 1000
            data["metadata"] = {
                "createTime": curTime,
                "updateTime": curTime,
            }
            data["isDelete"] = False

        _insert_one_result = DB.insert_one(data)

        return str(_insert_one_result.inserted_id)

    @classmethod
    def update(cls, _id, **kwargs):
        # 获取集合引用
        DB = getCollectRef(cls.NAME)

        update_data = {}
        for k,v in kwargs.items():
            if k not in cls.FIELDS:
                raise Exception("updateFieldNotSupported")
            update_data[k] = v

        if update_data:
            update_data["metadata.updateTime"] = time.time() * 1000
            DB.update_one(
                { "_id": bson.ObjectId(_id) },
                { "$set": update_data }
            )

    @classmethod
    def delete(cls, id):
        # 获取集合引用
        DB = getCollectRef(cls.NAME)

        DB.delete_one(
            { "_id": bson.ObjectId(id) }
        )

    @classmethod
    def get(cls, id):
        # 获取集合引用
        DB = getCollectRef(cls.NAME)
        # 执行查询
        data = DB.find_one({"_id": bson.ObjectId(id)})
        if data is None:
            raise DocumentNotExistException()
        # 转换objectId对象 为 字符串
        data["_id"] = str(data["_id"])
        return data

    @classmethod
    def list(cls, condition = None, 
        after = None, limit = None, 
        filter = None):
        # 获取集合引用
        DB = getCollectRef(cls.NAME)

        datas = []

        # condition
        conditions = {}
        if condition is not None:
            conditions.update(condition)

        # limit
        if limit is None:
            limit = cls.LIMIT
        
        # after指定时间之后的tiems
        if after is not None:
            conditions.update({"metadata.createTime": { "$lt": after }})
        
        # print(conditions)
        for vd in DB.find(
                conditions, 
                filter
            ).sort(
                "metadata.createTime", 
                pymongo.DESCENDING
            ).limit(limit):
            vd["_id"] = str(vd["_id"])
            datas.append(vd)

        return datas
    
    @classmethod
    def aggregate(cls, aggregation = None, 
        condition = None, 
        after = None, limit = None, 
        filter = None):
        # 获取集合引用
        DB = getCollectRef(cls.NAME)

        datas = []

        # match condition
        conditions = {}
        if condition is not None:
            conditions.update(condition)
        
        # after指定时间之后的tiems
        if after is None:
            after = time.time() * 1000
        conditions.update({"metadata.createTime": { "$lt": after }})
        
        # limit
        if limit is None:
            limit = cls.LIMIT
        
        # compose aggregation
        aggregations = [
            {"$match": conditions},
            {"$sort": {"metadata.updateTime": -1}},
            {"$limit": limit},
        ]
        if aggregation is not None:
            aggregations = aggregations + aggregation
        
        # perform aggregation operation
        for data in DB.aggregate(aggregations):
            datas.append(data)

        return datas
