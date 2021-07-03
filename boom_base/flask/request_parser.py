from flask import request
import json
from boom_base.exception import ParametersNotProvideException,ParametersIllegalException

def getBodyParaFromRequestInDict():
    rawData = request.get_data().decode("utf-8")
    dataInDict = json.loads(rawData)
    return dataInDict

def getParaFromBody(fieldName, bodyDataInDict, defaultValue=None, raiseExceptionIfNone=True):
    fieldValue = bodyDataInDict.get(fieldName, defaultValue)
    if fieldValue is None and raiseExceptionIfNone:
        raise ParametersNotProvideException(fieldName)
    return fieldValue
    
# 验证 request body参数中 的 指定字段值 是否 等于预期的值
# 目前该函数 主要应用于 验证 参数中userId 是否等于登录用户的userId
def verifyPara(fieldName, expectedValue, 
    raiseExceptionIfNotExpected=True):
    bodyPara = getBodyParaFromRequestInDict()
    if bodyPara.get(fieldName, "") != expectedValue:
        if raiseExceptionIfNotExpected:
            raise ParametersIllegalException(fieldName=fieldName)
        else:
            return False
    return True