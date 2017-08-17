import pytest
from models import db as _db
from main import app as _app


@pytest.yield_fixture
def app():
    ctx = _app.app_context()
    ctx.push()
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