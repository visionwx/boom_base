import requests
from functools import wraps, partial
from flask import request
from werkzeug.exceptions import Unauthorized
from boom_base.model.users import Tokens
from boom_base.exception import TokenNotProvideException
from boom_base.flask.response import ResponseResult


def verifyToken():
    _token = request.headers.get("authorization", None)
    if _token is None:
        raise TokenNotProvideException()
    userId = Tokens.verifyToken(_token)
    return userId


def loginRequired(func=None):
    if func is None:
        return partial(loginRequired)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print("verify user token")
            userId = verifyToken()
            kwargs["userId"] = userId
            return func(*args, **kwargs)
        except Exception as e:
            return ResponseResult.failed(message=str(e))
    return wrapper


def verifyUserToken(func=None, isLoginRequired=True):
    if func is None:
        return partial(verifyUserToken, isLoginRequired=isLoginRequired)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print("verify user token")
            userId = verifyToken()
            kwargs["userId"] = userId
            return func(*args, **kwargs)
        except Exception as e:
            if not isLoginRequired:
                kwargs["userId"] = None
                return func(*args, **kwargs)
            else:
                return ResponseResult.failed(message=str(e))
    return wrapper


class Authentication:
    """
    传入authenticationUrl则表示需要鉴权。默认不鉴
    Usage:
        tokenData = Authentication('http://your/authentication/path').authenticate()
    """
    
    _instance = None
    def __new__(cls, authenticationUrl: str=None):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls.authenticationUrl = authenticationUrl
        return cls._instance
    
    def authenticate(self):
        if self.authenticationUrl is None:
            return
        authorization = request.headers.get('Authorization')
        headers = {'authorization': authorization}

        response = requests.post(self.authenticationUrl, headers=headers)
        respData = response.json()
        if respData.get('status') != 1:
            raise Unauthorized('Token Invalid')
        userData = respData['data']
        return userData
