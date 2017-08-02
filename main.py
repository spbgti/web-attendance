from models import db
from flask import Flask

app = Flask()

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'

db.init_app(app)
