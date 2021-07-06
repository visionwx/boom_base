import time

def timeStampNow():
    return int(time.time() * 1000)

""" 支持的所有字段类型
"""
class FIELD_TYPE:
    STRING = str
    INT    = int
    FLOAT  = float
    BOOL   = bool
    LIST   = list
    OBJECT = dict

class Metadata:
    createTime = None
    updateTime = None
    deleteTime = None
    def __init__(self, createTime, 
        updateTime=None, deleteTime=None):
        self.createTime = createTime
        self.updateTime = updateTime
        self.deleteTime = deleteTime

    def toDict(self):
        return {
            "metadata": {
                "createTime": self.createTime,
                "updateTime": self.updateTime,
                "deleteTime": self.deleteTime
            }
        }
        
    @classmethod
    def createNow(cls):
        return cls(createTime=timeStampNow()).toDict()
    
    @classmethod
    def updateNow(cls):
        return {"metadata.updateTime": timeStampNow()}
    
    @classmethod
    def deleteNow(cls):
        return {"metadata.deleteTime": timeStampNow()}

""" 字段基类
"""
class Field:
    # 字段类型
    type = None

    # 字段名称
    name = None
    # 字段描述
    description = ""
    # 是否必要字段，用于创建document的时候，判断
    isRequired = False
    # 默认值
    default = None
    # 是否隐藏字段，隐藏字段 在获取的时候，不会返回
    isHidden = False
    # 是否index字段
    isIndex = False
    # 是否只读, 表示只能在基类更改，不能由用户直接更改
    isReadOnly = False

    def __init__(self, name, 
        description = "", isRequired = False, 
        default = None, isHidden = False, 
        isIndex = False, isReadOnly = False):
        self.name = name
        self.description = description
        self.isRequired = isRequired
        self.default = default
        self.isHidden = isHidden
        self.isIndex = isIndex
        self.isReadOnly = isReadOnly
    
    # 检查输入的值 类型是否匹配
    def verify(self, fieldValue):
        return type(fieldValue) == self.type if fieldValue is not None else True
    
    # 将输入的值 转换成该字段的类型
    def parse(self, fieldValue):
        raise Exception("NotImpl")

class StringField(Field):
    type = FIELD_TYPE.STRING
    def parse(self, fieldValue):
        return str(fieldValue)

class IntField(Field):
    type = FIELD_TYPE.INT
    def parse(self, fieldValue):
        return int(fieldValue)
    
class FloatField(Field):
    type = FIELD_TYPE.FLOAT
    def parse(self, fieldValue):
        return float(fieldValue)

class BoolField(Field):
    type = FIELD_TYPE.BOOL
    def parse(self, fieldValue):
        return bool(fieldValue)

class ListField(Field):
    type = FIELD_TYPE.LIST
    def parse(self, fieldValue):
        return list(fieldValue)

class ObjectField(Field):
    type = FIELD_TYPE.OBJECT
    def parse(self, fieldValue):
        return dict(fieldValue)

