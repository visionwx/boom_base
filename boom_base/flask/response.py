import json

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