from .base import Collection
from functools import wraps, partial
import time
# from boom_base.logger import getLoggerInstance

# LOG = getLoggerInstance()

class ApiCallsCollection(Collection):
    NAME = "apiCalls"
    FIELDS = [
        "path",
        "time",
        "extraData"
    ]

# 接口调用记录装饰器
def apiCallRecord(func=None, apiPath=None, extraData=None):
    if func is None:
        return partial(apiCallRecord, apiPath=apiPath, 
            extraData=extraData)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print(apiPath)
            ApiCallsCollection.create(**{
                "path": apiPath,
                "time": time.time() * 1000,
                "extraData": extraData
            })
            return func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            return func(*args, **kwargs)
    return wrapper

# def log2(func=None, msg1="msg1"):
#     if func is None:
#         return partial(log2, msg1=msg1)
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print("test:" + str(time.time()) + ", " + msg1)
#         return func(*args, **kwargs)
#     return wrapper

# @log2(msg1="hello")
# def test(p1, p2):
#     print(p1)
#     print(p2)
#     return p1 + p2


