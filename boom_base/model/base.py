import abc
import bson
import pymongo
import time
from boom_base.mongodb import getMongoInstance
from boom_base.exception import (
    DocumentNotExistException, 
    CollectionRequireFieldNotProvideException,
    CollectionFieldTypeException,
    FieldNotSupportException)
from boom_base.model import fields

def getCollectRef(collectionName):
    MDB = getMongoInstance()
    return MDB.db[collectionName]

class CollectionUpdateType:
    SET        = "set"
    INC        = "inc"
    PUSH       = "push"
    PULL       = "pull"
    ADD_TO_SET = "addToSet"


class DataModel:
    FIELDS = []
    
    # 转换成dict: {fieldName: FieldObject}
    @classmethod
    def toDict(cls):
        result = {}
        perField:fields.Field = None
        for perField in cls.FIELDS:
            result[perField.name] = perField
        return result
    
    # 转换成列表
    @classmethod
    def toNameList(cls):
        return [perField.name for perField in cls.FIELDS]

    @classmethod
    def project(cls, extraProject=None):
        result = {
            "_id": {"$toString":"$_id"},
            "metadata": 1,
        }
        perField:fields.Field = None
        for perField in cls.FIELDS:
            if perField.isHidden:
                continue
            result.update({
                perField.name: { "$ifNull": [ "$" + perField.name, perField.default ] },
            })
        
        if extraProject is not None:
            result.update(extraProject)

        return result

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
    LIMIT = 200
    
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
    def update_v2(cls, _id, type="set", **kwargs):
        # 支持三种类型的update
        # set, inc, push, addToSet
        # 获取集合引用
        DB = getCollectRef(cls.NAME)

        update_data = {}
        for k,v in kwargs.items():
            if k not in cls.FIELDS:
                raise Exception("updateFieldNotSupported")
            update_data[k] = v

        if type == CollectionUpdateType.SET:
            update_data["metadata.updateTime"] = time.time() * 1000
            update_data = {"$set": update_data}
        elif type == CollectionUpdateType.INC:
            update_data = {"$inc": update_data}
        elif type == CollectionUpdateType.PUSH:
            update_data = {"$push": update_data}
        elif type == CollectionUpdateType.PULL:
            update_data = {"$pull": update_data}
        elif type == CollectionUpdateType.ADD_TO_SET:
            update_data = {"$addToSet": update_data}
        else:
            update_data["metadata.updateTime"] = time.time() * 1000
            update_data = {"$set": update_data}

        if update_data:
            DB.update_one(
                { "_id": bson.ObjectId(_id) },
                update_data
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
        after = None, limit = None, sort = -1,
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
                sort
            ).limit(limit):
            vd["_id"] = str(vd["_id"])
            datas.append(vd)

        return datas
    
    @classmethod
    def aggregate(cls, aggregation = None, 
        condition = None, 
        after = None, limit = None, sort = -1,
        filter = None):
        # 获取集合引用
        DB = getCollectRef(cls.NAME)

        datas = []

        # match condition
        conditions = {}
        if condition is not None:
            conditions.update(condition)
        
        # after指定时间之后的tiems
        if after is not None:
            conditions.update({"metadata.createTime": { "$lt": after }})
        
        # limit
        if limit is None:
            limit = cls.LIMIT
        
        # compose aggregation
        aggregations = [
            {"$match": conditions},
            {"$sort": {"metadata.createTime": sort}},
        ]

        # limit aggregation,指定-1 表示不做limit限制
        if limit > 0:
            aggregations = aggregations + [{"$limit": limit},]

        # 加入自定义的aggregation
        if aggregation is not None:
            aggregations = aggregations + aggregation
        
        # perform aggregation operation
        for data in DB.aggregate(aggregations):
            if "_id" in data.keys():
                data["_id"] = str(data["_id"])
            datas.append(data)

        return datas
    
    @classmethod
    def aggregateGet(cls, id, aggregation = None):
        # 获取集合引用
        DB = getCollectRef(cls.NAME)
        aggregations = [
            {"$match": {"_id": bson.ObjectId(id)}}
        ]
        if aggregation is not None:
            aggregations = aggregations + aggregation
        # perform aggregation operation
        result = None
        datas = []
        for data in DB.aggregate(aggregations):
            if "_id" in data.keys():
                data["_id"] = str(data["_id"])
            datas.append(data)
        if len(datas) > 0:
            result = datas[0]

        return result
    
    @classmethod
    def exist(cls, condition):
        # 检查参数格式
        if condition is None:
            raise Exception("condition parameter is none")
        if type(condition) is not dict:
            raise Exception("condition parameter must be dict")
        # 获取集合引用
        DB = getCollectRef(cls.NAME)
        # 执行查询
        data = DB.find_one(condition)
        if data is None:
            return False
        else:
            return True

    @classmethod
    def findAndUpdate(cls, condition, updateData):
        pass



# class CollectionNew:
#     # 共有字段
#     # metadata = { createTime, updateTime, deleteTime,} 10位时间戳
#     # BASE_FIELDS = {
#     #     "_id": fields.StringField(name="_id",isRequired=False,isIndex=True,),
#     #     "metadata": fields.ObjectField(name="metadata", isReadOnly=True, isRequired=False),
#     #     "isDelete": fields.BoolField(name="isDelete", isReadOnly=True, isRequired=False)
#     # }
#     INDEX_FIELD     = fields.StringField(name="_id",isRequired=False,isIndex=True,)
#     METADATA_FIELD  = fields.ObjectField(name="metadata", isReadOnly=True, isRequired=False)
#     IS_DELETE_FIELD = fields.BoolField(name="isDelete", isReadOnly=True, isRequired=False)
    
#     # 集合名称
#     NAME:str = None

#     # 数据库实例
#     DB = None

#     # 所有字段
#     FIELDS:dict = {}

#     # 必须字段，create的时候，必须带入
#     #REQUIRED_FIELDS = []

#     # 隐藏字段集合，定义当调用toJson函数时，不含含的字段
#     #HIDDEN_FIELDS = []

#     # limit 最大查询返回items数量
#     LIMIT = 50
    
#     # 构建函数
#     def __init__(self):
#         pass

#     @classmethod
#     def create(cls, **kwargs):
#         # 获取集合引用
#         DB = getCollectRef(cls.NAME)

#         data = {}
        
#         # 是否提供index
#         if cls.INDEX_FIELD.name in kwargs.keys():
#             data[cls.INDEX_FIELD.name] = bson.ObjectId(
#                 kwargs[cls.INDEX_FIELD.name])
        
#         # 初始化基础字段
#         data[cls.METADATA_FIELD.name]  = fields.Metadata.createNow()
#         data[cls.IS_DELETE_FIELD.name] = cls.IS_DELETE_FIELD.default

#         # 自定义字段
#         for fieldObj in cls.FIELDS.values():
#             if fieldObj.isReadOnly:
#                 data[fieldObj.name] = fieldObj.default
#                 continue

#             fieldValue = kwargs.get(fieldObj.name, fieldObj.default)
#             if fieldValue is None and fieldObj.isRequired:
#                 raise CollectionRequireFieldNotProvideException(fieldObj.name)

#             data[fieldObj.name] = fieldValue

#         _insert_one_result = DB.insert_one(data)

#         return str(_insert_one_result.inserted_id)

#     @classmethod
#     def update(cls, _id, type="set", **kwargs):
#         # 支持三种类型的update
#         # set, inc, push, addToSet
#         # 获取集合引用
#         DB = getCollectRef(cls.NAME)

#         update_data = {}
#         for k,v in kwargs.items():
#             if k not in cls.FIELDS.keys():
#                 raise FieldNotSupportException(k)
#             if cls.FIELDS[k].isReadOnly:
#                 raise FieldNotSupportException(k)
            
#             update_data[k] = v

#         if type == CollectionUpdateType.SET:
#             update_data = {"$set": update_data}
#         elif type == CollectionUpdateType.INC:
#             update_data = {"$inc": update_data}
#         elif type == CollectionUpdateType.PUSH:
#             update_data = {"$push": update_data}
#         elif type == CollectionUpdateType.PULL:
#             update_data = {"$pull": update_data}
#         elif type == CollectionUpdateType.ADD_TO_SET:
#             update_data = {"$addToSet": update_data}
#         else:
#             update_data = {"$set": update_data}

#         if update_data:
#             update_data["$set"] = fields.Metadata.updateNow()
#             DB.update_one(
#                 { cls.INDEX_FIELD.name: bson.ObjectId(_id) },
#                 update_data
#             )

#     @classmethod
#     def delete(cls, id):
#         # 获取集合引用
#         DB = getCollectRef(cls.NAME)

#         DB.delete_one(
#             { cls.INDEX_FIELD.name: bson.ObjectId(id) }
#         )

#     @classmethod
#     def get(cls, id):
#         # 获取集合引用
#         DB = getCollectRef(cls.NAME)
#         # 执行查询
#         data = DB.find_one({cls.INDEX_FIELD.name: bson.ObjectId(id)})
#         if data is None:
#             raise DocumentNotExistException()
#         # 转换objectId对象 为 字符串
#         data[cls.INDEX_FIELD.name] = str(data[cls.INDEX_FIELD.name])
#         # 删除hidden字段
#         for fieldName in data.keys():
#             if fieldName not in cls.FIELDS.keys():
#                 continue
#             if not cls.FIELDS[fieldName].isHidden:
#                 continue
#             data.pop(fieldName)

#         return data

#     @classmethod
#     def list(cls, condition = None, 
#         after = None, limit = None, 
#         filter = None):
#         # 获取集合引用
#         DB = getCollectRef(cls.NAME)

#         datas = []

#         # condition
#         conditions = {}
#         if condition is not None:
#             conditions.update(condition)

#         # limit
#         if limit is None:
#             limit = cls.LIMIT
        
#         # after指定时间之后的tiems
#         if after is not None:
#             conditions.update({"metadata.createTime": { "$lt": after }})
        
#         # print(conditions)
#         for vd in DB.find(
#                 conditions, 
#                 filter
#             ).sort(
#                 "metadata.createTime", 
#                 pymongo.DESCENDING
#             ).limit(limit):
#             vd[cls.INDEX_FIELD.name] = str(vd[cls.INDEX_FIELD.name])
#             datas.append(vd)

#         return datas
    
#     @classmethod
#     def aggregate(cls, aggregation = None, 
#         condition = None, 
#         after = None, limit = None, 
#         filter = None):
#         # 获取集合引用
#         DB = getCollectRef(cls.NAME)

#         datas = []

#         # match condition
#         conditions = {}
#         if condition is not None:
#             conditions.update(condition)
        
#         # after指定时间之后的tiems
#         if after is None:
#             after = time.time() * 1000
#         conditions.update({"metadata.createTime": { "$lt": after }})
        
#         # limit
#         if limit is None:
#             limit = cls.LIMIT
        
#         # compose aggregation
#         aggregations = [
#             {"$match": conditions},
#             {"$sort": {"metadata.createTime": -1}},
#             {"$limit": limit},
#         ]
#         if aggregation is not None:
#             aggregations = aggregations + aggregation
        
#         # perform aggregation operation
#         for data in DB.aggregate(aggregations):
#             if cls.INDEX_FIELD.name in data.keys():
#                 data[cls.INDEX_FIELD.name] = str(data[cls.INDEX_FIELD.name])
#             datas.append(data)

#         return datas
    
#     @classmethod
#     def aggregateGet(cls, id, aggregation = None):
#         # 获取集合引用
#         DB = getCollectRef(cls.NAME)
#         aggregations = [
#             {"$match": {cls.INDEX_FIELD.name: bson.ObjectId(id)}}
#         ]
#         if aggregation is not None:
#             aggregations = aggregations + aggregation
#         # perform aggregation operation
#         result = None
#         datas = []
#         for data in DB.aggregate(aggregations):
#             if cls.INDEX_FIELD.name in data.keys():
#                 data[cls.INDEX_FIELD.name] = str(data[cls.INDEX_FIELD.name])
#             datas.append(data)
#         if len(datas) > 0:
#             result = datas[0]

#         return result

