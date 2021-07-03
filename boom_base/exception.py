class ParametersNotProvideException(Exception):
    def __init__(self, fieldName):
        self.fieldName = fieldName
    def __str__(self):
        return "parameter:" + self.fieldName  + " not found"

class ParametersIllegalException(Exception):
    def __init__(self, fieldName):
        self.fieldName = fieldName
    def __str__(self):
        return "parameter:" + self.fieldName  + " illegal"

class VideoNotExistException(Exception):
    def __init__(self, videoId):
        self.videoId = videoId
    def __str__(self):
        return "videoId:" + self.videoId  + " not found"

class CommentNotExistException(Exception):
    def __init__(self, commentId):
        self.commentId = commentId
    def __str__(self):
        return "commentId:" + self.commentId  + " not found"

class VideoInboxNotExistException(Exception):
    def __init__(self, videoInboxId):
        self.videoInboxId = videoInboxId
    def __str__(self):
        return "videoInboxId:" + self.videoInboxId  + " not found"

class DocumentNotExistException(Exception):
    def __str__(self):
        return "DocumentNotExistException"

class CollectionRequireFieldNotProvideException(Exception):
    def __init__(self, field):
        self.field = field
    def __str__(self):
        return "Field:" + self.field  + " not provide"

# 令牌超时
class TokenExpireException(Exception):
    def __str__(self):
        return "TokenExpireException"

# 刷新令牌不存在
class RefreshTokenNotExistException(Exception):
    def __str__(self):
        return "RefreshTokenNotExistException"

# 未提供令牌
class TokenNotProvideException(Exception):
    def __str__(self):
        return "RefreshTokenNotExistException"

class PhoneCodeVerifyFailedException(Exception):
    def __str__(self):
        return "PhoneCodeVerifyFailedException"

class SendSmsCodeFailedException(Exception):
    def __str__(self):
        return "SendSmsCodeFailedException"