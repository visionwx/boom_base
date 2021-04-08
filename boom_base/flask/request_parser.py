from flask import request
import json
from boom_base.exception import ParametersNotProvideException

def getBodyParaFromRequestInDict():
    rawData = request.get_data().decode("utf-8")
    print(rawData)
    dataInDict = json.loads(rawData)
    return dataInDict

def getParaFromBody(fieldName, bodyDataInDict, defaultValue=None, raiseExceptionIfNone=True):
    fieldValue = bodyDataInDict.get(fieldName, defaultValue)
    if fieldValue is None and raiseExceptionIfNone:
        raise ParametersNotProvideException(fieldName)
    return fieldValue
    