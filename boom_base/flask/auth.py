from functools import wraps, partial
from flask import request
from boom_base.model.users import Tokens
from boom_base.exception import TokenNotProvideException

def verifyToken():
    _token = request.headers.get("authorization", None)
    if _token is None:
        raise TokenNotProvideException()
    userId = Tokens.verifyToken(_token)
    return userId

def loginRequired(func=None):
    if func is None:
        return partial(loginRequired)
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("verify user token")
        userId = verifyToken()
        kwargs["userId"] = userId
        return func(*args, **kwargs)
    return wrapper

# @loginRequired()
# def test(userId):
#     print("test")
#     print("userId=" + userId)

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