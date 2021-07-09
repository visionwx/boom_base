import json
import traceback
from flask import request, Blueprint
from boom_base.flask import auth
from boom_base.model.base import Collection
from boom_base.model.api_calls import apiCallRecord
from boom_base.flask.request_parser import (
    getBodyParaFromRequestInDict, 
    verifyPara,
    getParaFromBody)

from boom_base.model.fields import Field

from boom_base.exception import (CollectionFieldTypeException, FieldNotSupportException)

# from boom_base.logger import getLoggerInstance
# LOG = getLoggerInstance()

TAG = "boom_base.flask.view"

class EmptyParameter:
    pass

class ResponseResult():
    @staticmethod
    def success(status=1, message="success", data=None):
        return json.dumps({
            'status': status, 
            'message': message, 
            'data': data 
        })

    @staticmethod
    def failed(status=0, message="Failed", data=None):
        return json.dumps({
            'status': status, 
            'message': message, 
            'data': data 
        })

class ModelView():
    # 数据表操作客户端
    MODEL:Collection = None

    # 数据模型: {"fieldName": Field Object}
    DATA_MODEL:dict = None

    # 高级聚合查询语句，用于list接口
    AGGREGATIONS = {}
    def registerAggregation(self, listType, aggregationList):
        if listType == "0":
            raise Exception("listType 0 is not allowed")
        if type(aggregationList) is not list:
            raise Exception("aggregation type error, must be list")
        self.AGGREGATIONS[listType] = aggregationList
        
    def __init__(self, app:Blueprint):
        self.app = app
        self.registerView()

    def _collectionOperation(self):
        result = None
        if request.method == 'GET':
            result = self.list()
        elif request.method == 'POST':
            result = self.create()
        else:
            raise Exception("UnsupportMethod")
        return result
    
    def _documentOperation(self, _id):
        result = None
        if request.method == 'GET':
            result = self.get(_id)
        elif request.method == 'PUT' or request.method == 'PATCH' or request.method == 'POST':
            result = self.update(_id)
        elif request.method == 'DELETE':
            result = self.delete(_id)
        else:
            raise Exception("UnsupportMethod")
        return result

    def registerView(self):
        self.app.add_url_rule(
            '/', 
            view_func=self._collectionOperation, 
            methods=['GET', 'POST']
        )
        self.app.add_url_rule(
            '/<_id>', 
            view_func=self._documentOperation, 
            methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH']
        )
    
    def getParaForCreate(self, bodyData):
        data = {}
        for field in self.MODEL.FIELDS:
            if field in data.keys():
                continue
            if field in self.MODEL.REQUIRED_FIELDS:
                fieldValue = getParaFromBody(field, bodyData)
            else:
                fieldValue = getParaFromBody(field, bodyData, 
                    raiseExceptionIfNone=False)
            if fieldValue is not None:
                data.update({
                    field: fieldValue
                })
        if data == {}:
            raise Exception("no parameter provide")
        return data

    def getParaForUpdate(self, bodyData):
        data = {}
        for field in self.MODEL.FIELDS:
            if field in data.keys():
                continue
            fieldValue = getParaFromBody(field, bodyData, 
                    raiseExceptionIfNone=False)
            if fieldValue is not None:
                data.update({
                    field: fieldValue
                })
        if data == {}:
            raise Exception("no parameter provide")
        return data

    def parseCreatePara(self, paraDict):
        para = {}
        perField:Field = None
        for perField in self.DATA_MODEL.values():
            # 是否已经采集到
            if perField.name in para.keys():
                continue
            if perField.isRequired:
                # 必要字段
                fieldValue = getParaFromBody(perField.name, paraDict)
            else:
                # 可选字段
                fieldValue = getParaFromBody(perField.name, paraDict, 
                    defaultValue=perField.default,
                    raiseExceptionIfNone=False)
            # 验证参数值是否合规
            if not perField.verify(fieldValue):
                raise CollectionFieldTypeException(perField.name)
            # 更新参数字段
            para.update({
                perField.name: fieldValue
            })
        # 是否提供了_id
        _id = getParaFromBody("_id", paraDict, raiseExceptionIfNone=False)
        if _id is not None:
            para.update({
                "_id": _id,
            })
        if para == {}:
            raise Exception("no parameter provide")
        return para

    def parseUpdatePara(self, paraDict):
        para = {}
        perField:Field = None
        for perField in self.DATA_MODEL.values():
            # 是否已经采集到
            if perField.name in para.keys():
                continue
            # 用户是否提供了该参数值
            fieldValue = getParaFromBody(perField.name, paraDict,
                defaultValue=EmptyParameter, 
                raiseExceptionIfNone=False)
            if fieldValue is EmptyParameter:
                # 用户没有提供
                continue
            # 验证参数值是否可修改
            if perField.isReadOnly:
                raise FieldNotSupportException(perField.name)
            # 验证参数值是否合规
            if not perField.verify(fieldValue):
                raise CollectionFieldTypeException(perField.name)
            # 更新参数字段
            para.update({
                perField.name: fieldValue
            })
        if para == {}:
            raise Exception("no parameter provide")
        return para
    
    def parseListPara(self, paraDict):
        para = {}
        perField:Field = None
        for perField in self.DATA_MODEL.values():
            # 是否已经采集到
            if perField.name in para.keys():
                continue
            # 用户是否提供了该参数值
            fieldValue = getParaFromBody(perField.name, paraDict,
                defaultValue=EmptyParameter, 
                raiseExceptionIfNone=False)
            if fieldValue is EmptyParameter:
                # 用户没有提供
                continue
            # 验证参数值是否合规
            if not perField.verify(fieldValue):
                raise CollectionFieldTypeException(perField.name)
            # 更新参数字段
            para.update({
                perField.name: fieldValue
            })
        if para == {}:
            para = None
        return para
        
    def parseLimitPara(self):
        limit = getParaFromBody("_limit_", request.args,
            defaultValue=50, 
            raiseExceptionIfNone=False)
        if limit is not None:
            limit = int(limit)
        if limit <= 0:
            limit = 50
        return limit

    def parseAfterPara(self):
        after = getParaFromBody("_after_", request.args,
            raiseExceptionIfNone=False)
        if after is not None:
            after = int(after)
        if after and after <= 0:
            after = None
        return after

    def parseSortPara(self):
        sort = getParaFromBody("_sort_", request.args,
            defaultValue=-1,
            raiseExceptionIfNone=False)
        if sort is not None:
            sort = int(sort)
        if sort not in [-1,1]:
            sort = -1
        return sort

    def parseTypePara(self):
        listType = getParaFromBody("_type_", request.args,
            defaultValue="0",
            raiseExceptionIfNone=False)
        if listType is not None:
            listType = str(listType)
        if listType not in self.AGGREGATIONS.keys():
            listType = "0"
        return listType

    def create(self):
        try:
            # 获取用户id
            #userId = auth.verifyToken()

            # 获取body参数
            bodyPara = getBodyParaFromRequestInDict()
            
            # 获取指定字段参数值
            # modelData = self.getParaForCreate(bodyPara)
            modelData = self.parseCreatePara(bodyPara)

            # 创建记录
            _id = self.MODEL.create(**modelData)
            
            result = ResponseResult.success(data=_id)

        except Exception as e:
            print(traceback.format_exc())
            if type(e) == CollectionFieldTypeException:
                err = str(e)
            else:
                err = type(e).__name__
            result = ResponseResult.failed(message=err)

        return result

    def update(self, _id):
        try:
            # 获取用户id
            #userId = auth.verifyToken()

            # 获取body参数
            bodyPara = getBodyParaFromRequestInDict()
            
            # 获取指定字段参数值
            # modelData = self.getParaForUpdate(bodyPara)
            modelData = self.parseUpdatePara(bodyPara)

            # 提取高级查询参数
            updateType = getParaFromBody("type", request.args, 
                defaultValue="set",
                raiseExceptionIfNone=False)

            # 创建记录
            self.MODEL.update_v2(_id, updateType, **modelData)
            
            result = ResponseResult.success()

        except Exception as e:
            print(traceback.format_exc())
            result = ResponseResult.failed(message=type(e).__name__)

        return result

    def get(self, _id, aggregation=None):
        try:
            # 提取高级查询参数
            listType = getParaFromBody("_type_", request.args, 
                defaultValue="0",
                raiseExceptionIfNone=False)

            # 检查是否有aggregation
            if aggregation is None:
                aggregation = self.AGGREGATIONS.get(listType, None)

            # 查询记录
            if aggregation is None:
                data = self.MODEL.get(_id)
            else:
                data = self.MODEL.aggregateGet(
                    id = _id,
                    aggregation = aggregation,
                )
            
            result = ResponseResult.success(data=data)

        except Exception as e:
            print(traceback.format_exc())
            result = ResponseResult.failed(message=type(e).__name__)

        return result

    def delete(self, _id):
        try:
            # 获取用户id
            #userId = auth.verifyToken()

            # 创建记录
            data = self.MODEL.delete(_id)
            
            result = ResponseResult.success(data=data)

        except Exception as e:
            print(traceback.format_exc())
            result = ResponseResult.failed(message=type(e).__name__)

        return result

    def list(self, condition=None, aggregation=None):
        try:

            # 获取指定字段参数值
            listType = self.parseTypePara()
            after    = self.parseAfterPara()
            limit    = self.parseLimitPara()
            sort     = self.parseSortPara()
            
            # 检查是否有指定 condition, 否则从参数提取condition参数
            if condition is None:
                condition = self.parseListPara(request.args)

            # 检查是否有 指定aggregation
            if aggregation is None:
                aggregation = self.AGGREGATIONS.get(listType, None)

            # 查询数据
            if aggregation is None:
                datas = self.MODEL.list(
                    condition = condition,
                    after = after,
                    limit = limit,
                    sort  = sort,
                )
            else:
                datas = self.MODEL.aggregate(
                    aggregation = aggregation,
                    condition = condition,
                    after = after,
                    limit = limit,
                    sort  = sort,
                )
            
            result = ResponseResult.success(data=datas)

        except Exception as e:
            print(traceback.format_exc())
            result = ResponseResult.failed(message=type(e).__name__)

        return result

# # 针对前端正常用户的model view, 要求用户必须登录
# # create/get/update/delete/list将检查 userId
class RequireLoginModelView(ModelView):

    @apiCallRecord(apiPath="Create /")
    @auth.verifyUserToken(isLoginRequired=True)
    def create(self, userId):
        return super().create()
    
    @apiCallRecord(apiPath="Update /" )
    @auth.verifyUserToken(isLoginRequired=True)
    def update(self, _id, userId):
        return super().update(_id)
    
    @apiCallRecord(apiPath="Get /")
    @auth.verifyUserToken(isLoginRequired=True)
    def get(self, _id, userId):
        return super().get(_id)
    
    @apiCallRecord(apiPath="Delete /")
    @auth.verifyUserToken(isLoginRequired=True)
    def delete(self, _id, userId):
        return super().delete(_id)
    
    @apiCallRecord(apiPath="List /")
    @auth.verifyUserToken(isLoginRequired=True)
    def list(self, userId):
        return super().list()