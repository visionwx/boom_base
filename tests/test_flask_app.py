import pytest
from boom_base.flask.flask_app import app as test_app
from flask import request


@test_app.route('/')
def home():
    trace_id = request.headers.get('Boom-TraceId')
    return trace_id


@pytest.fixture
def app():
    return test_app


def test_boom_trace_id(client):

    resp = client.get('http://localhost:5000/')
    pass