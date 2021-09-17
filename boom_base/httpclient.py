import requests
from flask import request


def set_trace_id(kwargs):
    if kwargs.get('headers'):
        kwargs['headers']['Boom-TraceId'] = \
            request.headers.get('Boom-TraceId')
    else:
        kwargs['headers'] = {
            'Boom-TraceId': request.headers.get('Boom-TraceId')}


def get(*args, **kwargs):
    set_trace_id(kwargs)
    return requests.get(*args, **kwargs)


def post(*args, **kwargs):
    set_trace_id(kwargs)
    return requests.post(*args, **kwargs)


def put(*args, **kwargs):
    set_trace_id(kwargs)
    return requests.put(*args, **kwargs)


def delete(*args, **kwargs):
    set_trace_id(kwargs)
    return requests.delete(*args, **kwargs)
