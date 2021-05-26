import json
import traceback
from flask import request, Blueprint
from boom_base.flask import auth
from boom_base.model.base import Collection
from boom_base.flask.request_parser import (
    getBodyParaFromRequestInDict, 
    getParaFromBody)

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
    MODEL:Collection = None

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

    def create(self):
        try:
            # 获取用户id
            #userId = auth.verifyToken()

            # 获取body参数
            bodyPara = getBodyParaFromRequestInDict()
            
            # 获取指定字段参数值
            modelData = self.getParaForCreate(bodyPara)

            # 创建记录
            _id = self.MODEL.create(**modelData)
            
            result = ResponseResult.success(data=_id)

        except Exception as e:
            print(traceback.format_exc())
            result = ResponseResult.failed(message=type(e).__name__)

        return result

    def update(self, _id):
        try:
            # 获取用户id
            #userId = auth.verifyToken()

            # 获取body参数
            bodyPara = getBodyParaFromRequestInDict()
            
            # 获取指定字段参数值
            modelData = self.getParaForUpdate(bodyPara)

            # 创建记录
            self.MODEL.update(_id, **modelData)
            
            result = ResponseResult.success()

        except Exception as e:
            print(traceback.format_exc())
            result = ResponseResult.failed(message=type(e).__name__)

        return result

    def get(self, _id):
        try:
            # 获取用户id
            #userId = auth.verifyToken()

            # 创建记录
            data = self.MODEL.get(_id)
            
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

    def list(self, condition=None):
        try:
            # 获取body参数
            # bodyPara = getBodyParaFromRequestInDict()
            
            # 获取指定字段参数值
            listType = getParaFromBody("type", request.args, 
                defaultValue="0",
                raiseExceptionIfNone=False)
            after = getParaFromBody("after", request.args, 
                raiseExceptionIfNone=False)
            limit = getParaFromBody("limit", request.args, 
                raiseExceptionIfNone=False)

            # 检查是否有aggregation
            aggregation = self.AGGREGATIONS.get(listType, None)

            # 查询数据
            if aggregation is None:
                datas = self.MODEL.list(
                    condition = condition,
                    after = after,
                    limit = limit
                )
            else:
                datas = self.MODEL.aggregate(
                    aggregation = aggregation,
                    condition = condition,
                    after = after,
                    limit = limit
                )
            
            result = ResponseResult.success(data=datas)

        except Exception as e:
            print(traceback.format_exc())
            result = ResponseResult.failed(message=type(e).__name__)

        return result

# # 针对前端正常用户的model view, 要求用户必须登录
# # create/get/update/delete/list将检查 userId
# class LoginRequiredModelView(ModelView):
#     @auth.loginRequired()
#     def create(self, userId):
#         # 获取body参数
#         bodyPara = getBodyParaFromRequestInDict()
#         userIdPara = getParaFromBody("userId", bodyPara)
#         return super().create()