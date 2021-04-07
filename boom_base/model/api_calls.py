from .base import Collection

class ApiCallsCollection(Collection):
    NAME = "api_calls"
    FIELDS = [
        "path",
        "time",
        "extraData"
    ]
