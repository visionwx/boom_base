###
# ExceptionId = <typeId><numId>
# typeId定义：
# 0000: 认证相关
# 0001: 参数相关
# 0002: 数据库相关

class EXCEPTION_TYPE_ID:
    AUTH = "0000"
    PARAMETER = "0001"
    DB = "0002"

class ParametersNotProvideException(Exception):
    ID = EXCEPTION_TYPE_ID.PARAMETER + "0001"
    def __init__(self, fieldName):
        self.fieldName = fieldName
    def __str__(self):
        return "parameter:" + self.fieldName  + " not found"

class ParametersIllegalException(Exception):
    ID = EXCEPTION_TYPE_ID.PARAMETER + "0002"
    def __init__(self, fieldName):
        self.fieldName = fieldName
    def __str__(self):
        return "parameter:" + self.fieldName  + " illegal"

class VideoNotExistException(Exception):
    ID = EXCEPTION_TYPE_ID.DB + "0001"
    def __init__(self, videoId):
        self.videoId = videoId
    def __str__(self):
        return "videoId:" + self.videoId  + " not found"

class CommentNotExistException(Exception):
    ID = EXCEPTION_TYPE_ID.DB + "0002"
    def __init__(self, commentId):
        self.commentId = commentId
    def __str__(self):
        return "commentId:" + self.commentId  + " not found"

class VideoInboxNotExistException(Exception):
    ID = EXCEPTION_TYPE_ID.DB + "0003"
    def __init__(self, videoInboxId):
        self.videoInboxId = videoInboxId
    def __str__(self):
        return "videoInboxId:" + self.videoInboxId  + " not found"

class DocumentNotExistException(Exception):
    ID = EXCEPTION_TYPE_ID.DB + "0004"
    def __str__(self):
        return "DocumentNotExistException"

class CollectionRequireFieldNotProvideException(Exception):
    ID = EXCEPTION_TYPE_ID.DB + "0005"
    def __init__(self, field):
        self.field = field
    def __str__(self):
        return "Field:" + self.field  + " not provide"

class CollectionFieldTypeException(Exception):
    ID = EXCEPTION_TYPE_ID.DB + "0006"
    def __init__(self, field):
        self.field = field
    def __str__(self):
        return "Field:" + self.field  + " type mismatch"

class ShareTimeExpireException(Exception):
    ID = EXCEPTION_TYPE_ID.DB + "0007"
    def __str__(self):
        return "ShareTimeExpireException"

class ShareCodeNotMatchException(Exception):
    ID = EXCEPTION_TYPE_ID.DB + "0008"
    def __str__(self):
        return "ShareCodeNotMatchException"

class FieldNotSupportException(Exception):
    ID = EXCEPTION_TYPE_ID.DB + "0009"
    def __init__(self, field):
        self.field = field
    def __str__(self):
        return "Field:" + self.field  + " not support"



# 令牌超时
class TokenExpireException(Exception):
    ID = EXCEPTION_TYPE_ID.AUTH + "0001"
    def __str__(self):
        return "TokenExpireException"

# 刷新令牌不存在
class RefreshTokenNotExistException(Exception):
    ID = EXCEPTION_TYPE_ID.AUTH + "0002"
    def __str__(self):
        return "RefreshTokenNotExistException"

# 未提供令牌
class TokenNotProvideException(Exception):
    ID = EXCEPTION_TYPE_ID.AUTH + "0003"
    def __str__(self):
        return "RefreshTokenNotExistException"

class PhoneCodeVerifyFailedException(Exception):
    ID = EXCEPTION_TYPE_ID.AUTH + "0004"
    def __str__(self):
        return "PhoneCodeVerifyFailedException"

class SendSmsCodeFailedException(Exception):
    ID = EXCEPTION_TYPE_ID.AUTH + "0005"
    def __str__(self):
        return "SendSmsCodeFailedException"