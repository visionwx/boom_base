import json
import time
import uuid
from boom_base.model.base import Collection
from boom_base.exception import TokenExpireException, RefreshTokenNotExistException

class Users(Collection):
    NAME = "users"
    
    FIELDS = [
        "name",
        "nickName",
        "password", 
        "avatarUrl",
        "email",
        "phone",
        "wechatProvider",
    ]

class Tokens(Collection):
    NAME = "tokens"

    FIELDS = [
        "token", 
        "expireTime", 
        "refreshToken",
        "userId"
    ]

    # 验证token是否有效，返回用户id
    @classmethod
    def verifyToken(cls, token):
        # 提取token
        _tokens = cls.list(condition={
            "token": token
        })
        if len(_tokens) <= 0:
            raise TokenExpireException()
        _tokens = _tokens[0]
        # 检查token
        expireTime = _tokens.get("expireTime", 0)
        if expireTime - time.time() * 1000 <= 0:
            raise TokenExpireException()
        # 提取user_id
        userId = _tokens.get("userId", None)
        if userId is None:
            raise TokenExpireException()
        return userId

    # 给指定用户随机生成token, 2592000=30天有效期
    @classmethod
    def generateToken(cls, userId, expireInSeconds=2592000):
        token = {
            "token": str(uuid.uuid1()),
            "refreshToken": str(uuid.uuid1()),
            "expireTime": (time.time() + expireInSeconds) * 1000,
            "userId": userId,
        }
        tokenId = cls.create(**token)
        return token

    # 根据给定的refreshToken刷新token
    @classmethod
    def refreshToken(cls, refreshToken, expireInSeconds=2592000):
        # 查找refreshToken
        _tokens = cls.list(condition={
            "refreshToken": refreshToken
        })
        if len(_tokens) <= 0:
            raise RefreshTokenNotExistException()
        # 更新token
        _tokens = _tokens[0]
        updateData = {
            "token": str(uuid.uuid1()),
            "refreshToken": str(uuid.uuid1()),
            "expireTime": (time.time() + expireInSeconds) * 1000,
        }
        # 执行更新
        cls.update(_tokens["_id"], **updateData)
        return updateData

    # 根据token获取用户信息
    @classmethod
    def getUserInfoByToken(cls, token):
        userId = cls.verifyToken(token)
        userData = Users.get(userId)
        return userData