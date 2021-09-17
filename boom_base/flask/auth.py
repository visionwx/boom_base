import os
from functools import wraps, partial

import requests
from flask import request
from werkzeug.exceptions import Unauthorized

from boom_base.model.users import Tokens
from boom_base.exception import TokenNotProvideException
from boom_base.flask.response import ResponseResult


auth_required = os.environ.get('AUTH_REQUIRED', 'True')
authentication_domain = os.environ.get('AUTHENTICATION_DOMAIN')
authentication_url = f"{authentication_domain}/users/verify_token"


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


def authentication(func):
    def wrapper(*args, **kwargs):
        if auth_required == 'True':
            authorization = request.headers.get('Authorization')
            headers = {'authorization': authorization}

            resp = requests.post(authentication_url, headers=headers)
            response = resp.json()
            if response.get('status') != 1:
                raise Unauthorized('Token Invalid')
        return func(*args, **kwargs)

    return wrapper
