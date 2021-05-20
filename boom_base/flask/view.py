import json
from flask import request, Blueprint
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
            result = ResponseResult.failed(message=str(e))

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
            result = ResponseResult.failed(message=str(e))

        return result

    def get(self, _id):
        try:
            # 获取用户id
            #userId = auth.verifyToken()

            # 创建记录
            data = self.MODEL.get(_id)
            
            result = ResponseResult.success(data=data)

        except Exception as e:
            result = ResponseResult.failed(message=str(e))

        return result

    def delete(self, _id):
        try:
            # 获取用户id
            #userId = auth.verifyToken()

            # 创建记录
            data = self.MODEL.delete(_id)
            
            result = ResponseResult.success(data=data)

        except Exception as e:
            result = ResponseResult.failed(message=str(e))

        return result

    def list(self):
        try:
            # 获取用户id
            #userId = auth.verifyToken()

            # 获取body参数
            bodyPara = getBodyParaFromRequestInDict()
            
            # 获取指定字段参数值
            after = getParaFromBody("after", bodyPara, 
                raiseExceptionIfNone=False)
            limit = getParaFromBody("limit", bodyPara, 
                raiseExceptionIfNone=False)

            # 查询数据
            datas = self.MODEL.list(
                condition = None,
                after = after,
                limit = limit
            )
            
            result = ResponseResult.success(data=data)

        except Exception as e:
            result = ResponseResult.failed(message=str(e))

        return result
