from flask import request
from boom_base.model.users import Tokens
from boom_base.exception import TokenNotProvideException

def verifyToken():
    _token = request.headers.get("authorization", None)
    if _token is None:
        raise TokenNotProvideException()
    userId = Tokens.verifyToken(_token)
    return userId

# @wraps(func)
# def wrapper(*args, **kwargs):
#     try:
#         print(apiPath)
#         ApiCallsCollection.create(**{
#             "path": apiPath,
#             "time": time.time() * 1000,
#             "extraData": extraData
#         })
#         return func(*args, **kwargs)
#     except Exception as e:
#         print(str(e))
#         LOG.error("apiCallRecorder", str(e))
#         return func(*args, **kwargs)
# return wrapper