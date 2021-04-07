class ParametersNotProvideException(Exception):
    def __init__(self, fieldName):
        self.fieldName = fieldName
    def __str__(self):
        print("parameter:" + self.fieldName  + " not found")

class VideoNotExistException(Exception):
    def __init__(self, videoId):
        self.videoId = videoId
    def __str__(self):
        print("videoId:" + self.videoId  + " not found")

class CommentNotExistException(Exception):
    def __init__(self, commentId):
        self.commentId = commentId
    def __str__(self):
        print("commentId:" + self.commentId  + " not found")

class VideoInboxNotExistException(Exception):
    def __init__(self, videoInboxId):
        self.videoInboxId = videoInboxId
    def __str__(self):
        print("videoInboxId:" + self.videoInboxId  + " not found")

class DocumentNotExistException(Exception):
    pass

class CollectionRequireFieldNotProvideException(Exception):
    def __init__(self, field):
        self.field = field
    def __str__(self):
        print("Field:" + self.field  + " not provide")