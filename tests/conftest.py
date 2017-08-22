import json

import pytest
from flask import Response as BaseResponse
from flask.testing import FlaskClient

from main import app as _app
from models import db as _db


class Response(BaseResponse):
    """
    Добавляет к стандартному ответу .json() метод
        >>> resp = test_client.get(...)
        >>> resp.json()
        >>> {...}
    """
    def json(self):
        return json.loads(self.data.decode())


class TestClient(FlaskClient):
    """
    Модифицирует стандартный тестовый клиент, добавляя json-аргумент
        >>> resp = test_client.post(json={'my': 'json'})
    """
    def open(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        return super(TestClient, self).open(*args, **kwargs)


@pytest.yield_fixture
def app():
    ctx = _app.app_context()
    ctx.push()
    _app.test_client_class = TestClient
    _app.response_class = Response
    yield _app
    ctx.pop()


@pytest.yield_fixture
def db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    _db.init_app(app)
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture
def test_client(app):
    return app.test_client()
